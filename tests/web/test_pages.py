from fastapi.testclient import TestClient

from app.factory import create_app
from tests.factories import make_settings


def test_home_page_renders(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "really in your pixels" in response.text


def test_non_production_pages_are_hidden_from_search_engines(client: TestClient) -> None:
    assert '<meta name="robots" content="noindex, nofollow">' in client.get("/").text


def test_production_pages_are_indexable_with_canonical_urls() -> None:
    settings = make_settings(env="production", public_url="https://picxel.autolinium.com")

    with TestClient(create_app(settings)) as client:
        html = client.get("/").text

    assert '<link rel="canonical" href="https://picxel.autolinium.com/">' in html
    assert "noindex" not in html


def test_static_assets_are_served(client: TestClient) -> None:
    response = client.get("/static/css/tokens.css")

    assert response.status_code == 200
    assert "--color-signal-500" in response.text
