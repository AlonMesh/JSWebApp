# server/tests/test_routes.py
import pytest
from httpx import AsyncClient
from server.main import app

@pytest.mark.asyncio
async def test_get_code_blocks():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/code-blocks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_add_code_block():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        new_block = {
            "title": "Multiply",
            "initial_code": "function multiply(a, b) {\n  // TODO\n}",
            "solution_code": "function multiply(a, b) {\n  return a * b;\n}"
        }
        response = await ac.post("/code-blocks", json=new_block)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Multiply"
    assert "id" in data

@pytest.mark.asyncio
async def test_add_invalid_code_block():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        incomplete_block = {
            "title": "Broken"
        }
        response = await ac.post("/code-blocks", json=incomplete_block)
    assert response.status_code == 422  # Unprocessable Entity due to missing fields

@pytest.mark.asyncio
async def test_code_block_persistence():
    # Add
    async with AsyncClient(app=app, base_url="http://test") as ac:
        block = {
            "title": "Check",
            "initial_code": "function check() {}",
            "solution_code": "function check() { return true; }"
        }
        await ac.post("/code-blocks", json=block)

    # Fetch
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/code-blocks")
        titles = [b["title"] for b in response.json()]
        assert "Check" in titles
