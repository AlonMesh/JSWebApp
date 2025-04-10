from server.database.db_config import engine, Base
from server.database.crud import seed_code_blocks, get_all_code_blocks
from server.socket_manager import manager

async def initialize_app():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await seed_code_blocks()
    code_blocks = await get_all_code_blocks()
    manager.load_code_blocks(code_blocks)
