import re

import pytest
from httpx import ASGITransport, AsyncClient

from app.config import Environment, settings
from app.main import _get_version, app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


async def test_landing_page_returns_html(client):
    response = await client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


async def test_landing_page_includes_version_and_environment(client):
    response = await client.get("/")

    assert _get_version() in response.text
    assert settings.environment.value in response.text


async def test_landing_page_in_production_shows_production_badge_only(
    client, monkeypatch
):
    monkeypatch.setattr(settings, "environment", Environment.PRODUCTION)

    response = await client.get("/")

    assert re.search(r'<span class="badge">\s*production\s*</span>', response.text)
    assert "development" not in response.text.lower()


async def test_landing_page_css_asset_is_served(client):
    response = await client.get("/static/css/landing.css")

    assert response.status_code == 200
    assert "text/css" in response.headers["content-type"]


async def test_landing_page_js_asset_is_served(client):
    response = await client.get("/static/js/landing.js")

    assert response.status_code == 200
    assert "javascript" in response.headers["content-type"]
