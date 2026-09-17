"""Pure ASGI middleware: request context (IDs + access log) and security headers.

Pure ASGI rather than ``BaseHTTPMiddleware``: it keeps streaming responses intact and adds no
per-request task overhead.
"""

import logging
import re
import secrets
import time
import uuid

from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.core.logging import request_id_var

access_logger = logging.getLogger("picxel.access")

REQUEST_ID_HEADER = "X-Request-ID"
_VALID_REQUEST_ID = re.compile(r"[A-Za-z0-9._-]{8,128}")

# FastAPI serves Swagger UI from a CDN with an inline bootstrap script, so it needs its own policy.
DOCS_PATHS = frozenset({"/api/docs", "/api/docs/oauth2-redirect"})

PERMISSIONS_POLICY = "camera=(), microphone=(), geolocation=(), payment=(), usb=()"
HSTS_POLICY = "max-age=63072000; includeSubDomains"


class RequestContextMiddleware:
    """Tags each request with an ID (echoed as ``X-Request-ID``) and writes one access-log line."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = _incoming_request_id(scope) or uuid.uuid4().hex
        # Also kept on request.state: error pages rendered outside this middleware still need it.
        scope.setdefault("state", {})["request_id"] = request_id
        token = request_id_var.set(request_id)
        started = time.perf_counter()
        status_code = 500

        async def send_with_request_id(message: Message) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
                MutableHeaders(scope=message)[REQUEST_ID_HEADER] = request_id
            await send(message)

        try:
            await self.app(scope, receive, send_with_request_id)
        finally:
            duration_ms = round((time.perf_counter() - started) * 1000, 1)
            access_logger.info(
                "%s %s %s %.1fms",
                scope["method"],
                scope["path"],
                status_code,
                duration_ms,
                extra={
                    "http_method": scope["method"],
                    "path": scope["path"],
                    "status": status_code,
                    "duration_ms": duration_ms,
                },
            )
            request_id_var.reset(token)


def _incoming_request_id(scope: Scope) -> str | None:
    for name, value in scope["headers"]:
        if name == b"x-request-id":
            candidate: str = value.decode("latin-1")
            return candidate if _VALID_REQUEST_ID.fullmatch(candidate) else None
    return None


class SecurityHeadersMiddleware:
    """Adds hardened response headers and a per-request CSP nonce (``request.state.csp_nonce``)."""

    def __init__(self, app: ASGIApp, *, hsts: bool) -> None:
        self.app = app
        self.hsts = hsts

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        nonce = secrets.token_urlsafe(16)
        scope.setdefault("state", {})["csp_nonce"] = nonce
        if scope["path"] in DOCS_PATHS:
            policy = docs_content_security_policy()
        else:
            policy = content_security_policy(nonce, upgrade_insecure_requests=self.hsts)

        async def send_with_security_headers(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers["Content-Security-Policy"] = policy
                headers["X-Content-Type-Options"] = "nosniff"
                headers["X-Frame-Options"] = "DENY"
                headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
                headers["Cross-Origin-Opener-Policy"] = "same-origin"
                headers["Permissions-Policy"] = PERMISSIONS_POLICY
                if self.hsts:
                    headers["Strict-Transport-Security"] = HSTS_POLICY
            await send(message)

        await self.app(scope, receive, send_with_security_headers)


def content_security_policy(nonce: str, *, upgrade_insecure_requests: bool) -> str:
    directives = [
        "default-src 'self'",
        f"script-src 'self' 'nonce-{nonce}'",
        "style-src 'self'",
        "img-src 'self' data: blob:",
        "font-src 'self'",
        "connect-src 'self'",
        "object-src 'none'",
        "base-uri 'self'",
        "form-action 'self'",
        "frame-ancestors 'none'",
    ]
    if upgrade_insecure_requests:
        directives.append("upgrade-insecure-requests")
    return "; ".join(directives)


def docs_content_security_policy() -> str:
    return "; ".join(
        [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net",
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net",
            "img-src 'self' data: https://fastapi.tiangolo.com",
            "object-src 'none'",
            "base-uri 'self'",
            "frame-ancestors 'none'",
        ]
    )
