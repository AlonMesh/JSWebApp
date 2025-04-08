import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from server.database.models import CodeBlock
from server.database.db_config import Base, engine, AsyncSessionLocal
from server.database.crud import create_code_block, get_all_code_blocks


@pytest.fixture(scope="module")
async def initialized_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_create_code_block(initialized_db):
    new_block_data = CodeBlock(
        title="Test Block",
        initial_code="console.log('hello');",
        solution_code="console.log('hello');"
    )
    async with AsyncSessionLocal() as session:
        session.add(new_block_data)
        await session.commit()
        await session.refresh(new_block_data)

        assert new_block_data.id is not None
        assert new_block_data.title == "Test Block"


@pytest.mark.asyncio
async def test_get_all_code_blocks(initialized_db):
    block = CodeBlock(
        title="Retrieve Test",
        initial_code="let x = 1;",
        solution_code="let x = 1;"
    )
    async with AsyncSessionLocal() as session:
        session.add(block)
        await session.commit()

    blocks = await get_all_code_blocks()
    assert any(b.title == "Retrieve Test" for b in blocks)


@pytest.mark.asyncio
async def test_create_code_block_with_crud_function(initialized_db):
    class Dummy:
        title = "With CRUD"
        initial_code = "a = 2"
        solution_code = "a = 2"

    result = await create_code_block(Dummy())
    assert result.title == "With CRUD"
    assert result.id is not None