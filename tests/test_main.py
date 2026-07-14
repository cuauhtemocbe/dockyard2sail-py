from importlib.metadata import PackageNotFoundError

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import _get_version, app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_hello_default(client):
    response = await client.get("/api/v1/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, world!"}


async def test_hello_with_name(client):
    response = await client.get("/api/v1/hello?name=Claude")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Claude!"}


async def test_openapi_reports_installed_package_version(client):
    response = await client.get("/openapi.json")
    assert response.json()["info"]["version"] == _get_version()


def test_get_version_reads_installed_package_metadata(monkeypatch):
    monkeypatch.setattr("app.main.version", lambda name: "9.9.9")

    assert _get_version() == "9.9.9"


def test_get_version_falls_back_when_package_not_found(monkeypatch):
    def raise_not_found(name):
        raise PackageNotFoundError(name)

    monkeypatch.setattr("app.main.version", raise_not_found)

    assert _get_version() == "0.0.0-dev"
