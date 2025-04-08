import asyncio
from database.crud import seed_code_blocks

async def main():
    await seed_code_blocks()
    print("✅ Database initialized and seeded!")

asyncio.run(main())
