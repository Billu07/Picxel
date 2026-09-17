"""Exception handlers: RFC 9457 problem details for the API, branded HTML pages for the website."""

from collections.abc import Mapping
from typing import Any

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import Response

from app.core.problems import problem_response, status_phrase
from app.web.templating import templates

API_PATH_PREFIX = "/api/"

_PAGE_MESSAGES = {
    404: "We couldn't find that page.",
    500: "Something went wrong on our side. Please try again in a moment.",
}
_DEFAULT_PAGE_MESSAGE = "That request didn't work."


def _is_api_request(request: Request) -> bool:
    return request.url.path.startswith(API_PATH_PREFIX)


def render_error_page(
    request: Request, status_code: int, headers: Mapping[str, str] | None = None
) -> Response:
    return templates.TemplateResponse(
        request,
        "errors/error.html",
        {
            "status_code": status_code,
            "title": status_phrase(status_code),
            "message": _PAGE_MESSAGES.get(status_code, _DEFAULT_PAGE_MESSAGE),
        },
        status_code=status_code,
        headers=headers,
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> Response:
    if not _is_api_request(request):
        return render_error_page(request, exc.status_code, exc.headers)
    custom_detail = isinstance(exc.detail, str) and exc.detail != status_phrase(exc.status_code)
    return problem_response(
        exc.status_code,
        detail=exc.detail if custom_detail else None,
        instance=request.url.path,
        headers=exc.headers,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> Response:
    if not _is_api_request(request):
        return render_error_page(request, 422)
    return problem_response(
        422,
        detail="The request is invalid.",
        instance=request.url.path,
        extensions={"errors": jsonable_encoder(exc.errors())},
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> Response:
    """Last-resort 500 that hides internals; Starlette re-raises, so the error is still logged."""
    if not _is_api_request(request):
        return render_error_page(request, 500)
    return problem_response(500, instance=request.url.path)


EXCEPTION_HANDLERS: dict[int | type[Exception], Any] = {
    StarletteHTTPException: http_exception_handler,
    RequestValidationError: validation_exception_handler,
    Exception: unhandled_exception_handler,
}
