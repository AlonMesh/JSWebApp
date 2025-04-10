from sqlalchemy.future import select
from server.database.models import CodeBlock
from server.database.db_config import AsyncSessionLocal
from server.database.models import CodeBlock
from server.database.db_config import engine, Base

# Get all code blocks
async def get_all_code_blocks():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(CodeBlock))
        return result.scalars().all()

# Get single code block by ID
async def get_code_block_by_id(block_id: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(CodeBlock).where(CodeBlock.id == block_id)
        )
        return result.scalars().first()

# Get a single code block's original code by ID
async def get_code_block_original_code(block_id: str):
    code_block = await get_code_block_by_id(block_id)
    if code_block:
        return code_block.initial_code
    return None
       
# Create a new code block
async def create_code_block(block_data: CodeBlock):
    try:
        async with AsyncSessionLocal() as session:
            new_code_block = CodeBlock(
                title = block_data.title,
                initial_code = block_data.initial_code,
                solution_code = block_data.solution_code
            )
            session.add(new_code_block)
            await session.commit()
            await session.refresh(new_code_block)
            return new_code_block
    except Exception as e:
        print("DB Insert Error:", e)
        raise
    
    
# Create initial code blocks (I was allowed to add 4 blocks manually)
async def seed_code_blocks():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with AsyncSessionLocal() as session:
        # Check if any blocks already exist. If so, skip seeding to avoid duplicates.
        existing_blocks = await session.execute(select(CodeBlock))
        if existing_blocks.scalars().all():
            return


        initial_blocks = [
            CodeBlock(
                title="Arrow Function",
                initial_code="const sum = (a, b) => {\n  // TODO\n}",
                solution_code="const sum = (a, b) => {\n  return a + b;\n}"
            ),
            CodeBlock(
                title="Async Example",
                initial_code="async function fetchData() {\n  // TODO\n}",
                solution_code="async function fetchData() {\n  const res = await fetch('url');\n  return await res.json();\n}"
            ),
            CodeBlock(
                title="Promise.all with Multiple Requests",
                initial_code="const urls = ['url1', 'url2'];\n// TODO: let allData = ...\n// TODO: console.log(allData);",
                solution_code="const urls = ['url1', 'url2'];\nlet allData = await Promise.all(urls.map(url => fetch(url)));\nconsole.log(allData);"
            ),
            CodeBlock(
                title="Custom Promise Wrapper",
                initial_code="function wait(ms) {\n // TODO: return ...\n}\nwait(1000).then(() => console.log('1s passed'));",
                solution_code="function wait(ms) {\n return new Promise(resolve => setTimeout(resolve, ms));\n}\nwait(1000).then(() => console.log('1s passed'));"
            ),
        ]

        # Add initial blocks to the session
        session.add_all(initial_blocks)
        await session.commit()
