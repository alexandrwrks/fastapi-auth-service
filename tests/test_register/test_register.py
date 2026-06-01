import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register(async_client: AsyncClient):
    response = await async_client.post(
        "/auth_service/register", json={"username": "string", "password": "string"}
    )

    assert response.status_code == 400

    data = response.json()

    print(data)
    # assert data["username"] == "string"
