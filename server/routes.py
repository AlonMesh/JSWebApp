from fastapi import APIRouter
from database import code_blocks

router = APIRouter()

@router.get("/code-blocks")
def get_code_blocks():
    return code_blocks
