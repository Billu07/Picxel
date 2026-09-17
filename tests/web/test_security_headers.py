import re

from fastapi.testclient import TestClient

from app.factory import create_app
from tests.factories import make_settings

NONCE = re.compile(r"script-src 'self' 'nonce-([A-Za-z0-9_-]{16,})'")


def test_every_response_gets_a_fresh_csp_nonce(client: TestClient) -> None:
    first = NONCE.search(client.get("/").headers["content-security-policy"])
    second = NONCE.search(client.get("/").headers["content-security-policy"])

    assert first is not None
    assert second is not None
    assert first.group(1) != second.group(1)


def test_hardening_headers_are_present(client: TestClient) -> None:
    headers = client.get("/api/v1/health").headers

    assert "frame-ancestors 'none'" in headers["content-security-policy"]
    assert headers["x-content-type-options"] == "nosniff"
    assert headers["x-frame-options"] == "DENY"
    assert headers["referrer-policy"] == "strict-origin-when-cross-origin"
    assert "camera=()" in headers["permissions-policy"]
    assert "strict-transport-security" not in headers


def test_deployed_environments_enforce_https() -> None:
    with TestClient(create_app(make_settings(env="staging"))) as client:
        headers = client.get("/api/v1/health").headers

    assert headers["strict-transport-security"].startswith("max-age=")
    assert "upgrade-insecure-requests" in headers["content-security-policy"]


def test_api_docs_get_a_policy_that_allows_swagger_ui(client: TestClient) -> None:
    response = client.get("/api/docs")

    assert response.status_code == 200
    assert "https://cdn.jsdelivr.net" in response.headers["content-security-policy"]


def test_request_ids_are_generated(client: TestClient) -> None:
    request_id = client.get("/api/v1/health").headers["x-request-id"]

    assert re.fullmatch(r"[0-9a-f]{32}", request_id)


def test_valid_incoming_request_ids_are_kept(client: TestClient) -> None:
    response = client.get("/api/v1/health", headers={"X-Request-ID": "trace-abc-12345"})

    assert response.headers["x-request-id"] == "trace-abc-12345"


def test_malformed_incoming_request_ids_are_replaced(client: TestClient) -> None:
    response = client.get("/api/v1/health", headers={"X-Request-ID": "not valid!"})

    assert re.fullmatch(r"[0-9a-f]{32}", response.headers["x-request-id"])
