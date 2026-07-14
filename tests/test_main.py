import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


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
