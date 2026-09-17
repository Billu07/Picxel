import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

PROBLEM_JSON = "application/problem+json"


@pytest.fixture
def app_with_test_routes(app: FastAPI) -> FastAPI:
    async def explode() -> None:
        raise RuntimeError("secret internal detail")

    async def echo(n: int) -> dict[str, int]:
        return {"n": n}

    app.add_api_route("/api/v1/_test/explode", explode)
    app.add_api_route("/api/v1/_test/echo", echo)
    app.add_api_route("/_test/explode", explode)
    return app


def test_unknown_api_route_returns_problem_details(client: TestClient) -> None:
    response = client.get("/api/v1/does-not-exist")

    assert response.status_code == 404
    assert response.headers["content-type"] == PROBLEM_JSON
    assert response.json() == {
        "type": "about:blank",
        "title": "Not Found",
        "status": 404,
        "instance": "/api/v1/does-not-exist",
    }


def test_wrong_method_keeps_the_allow_header(client: TestClient) -> None:
    response = client.post("/api/v1/health")

    assert response.status_code == 405
    assert response.headers["content-type"] == PROBLEM_JSON
    assert "GET" in response.headers["allow"]


def test_validation_errors_list_the_invalid_fields(app_with_test_routes: FastAPI) -> None:
    with TestClient(app_with_test_routes) as client:
        response = client.get("/api/v1/_test/echo", params={"n": "not-a-number"})

    assert response.status_code == 422
    assert response.headers["content-type"] == PROBLEM_JSON
    body = response.json()
    assert body["status"] == 422
    assert body["errors"][0]["loc"] == ["query", "n"]


def test_unhandled_api_errors_do_not_leak_internals(app_with_test_routes: FastAPI) -> None:
    with TestClient(app_with_test_routes, raise_server_exceptions=False) as client:
        response = client.get("/api/v1/_test/explode")

    assert response.status_code == 500
    assert response.headers["content-type"] == PROBLEM_JSON
    assert "secret internal detail" not in response.text


def test_unknown_page_renders_the_branded_404(client: TestClient) -> None:
    response = client.get("/does-not-exist")

    assert response.status_code == 404
    assert response.headers["content-type"].startswith("text/html")
    assert "find that page" in response.text


def test_unhandled_page_errors_render_the_branded_500_with_request_id(
    app_with_test_routes: FastAPI,
) -> None:
    with TestClient(app_with_test_routes, raise_server_exceptions=False) as client:
        response = client.get("/_test/explode", headers={"X-Request-ID": "trace-00000001"})

    assert response.status_code == 500
    assert "secret internal detail" not in response.text
    assert "trace-00000001" in response.text
