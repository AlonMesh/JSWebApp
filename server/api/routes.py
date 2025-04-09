from fastapi import APIRouter
from server.database.crud import get_all_code_blocks, create_code_block, get_code_block_by_id
from pydantic import BaseModel
from server.socket_manager import manager

router = APIRouter()

class CodeBlockCreate(BaseModel):
    """Model for creating a new code block"""
    title: str
    initial_code: str
    solution_code: str

@router.get("/code-blocks")
async def get_code_blocks():
    print("Fetching all code blocks...")
    """Fetch all block codes (concretly - id and title) from the database"""
    blocks = await get_all_code_blocks()
    return blocks

@router.post("/code-blocks")
async def add_code_block(block_data: CodeBlockCreate):
    # Create a new code block in the database
    new_block = await create_code_block(block_data)
    
    # Add the new block to the WebSocket manager
    manager.code_blocks[str(new_block.id)] = {
                "title": new_block.title,
        "initial_code": new_block.initial_code,
        "solution_code": new_block.solution_code
    }
    
    # Return the newly created block
    return new_block
    
@router.get("/code-blocks/{block_id}")
async def get_code_block(block_id: str):
    """Fetch a specific code block by its ID"""
    block = await get_code_block_by_id(block_id)
    if not block:
        return {"error": "Code block not found"}
    return block