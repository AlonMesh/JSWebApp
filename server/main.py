from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from server.api.routes import router
from server.websocket.manager import WebSocketManager
from server.websocket.handlers import handle_websocket_message
from server.database.crud import get_all_code_blocks, seed_code_blocks
from server.database.db_config import engine, Base
from server.socket_manager import manager

app = FastAPI()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def load_code_blocks_from_db():
    # Step 1: Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    # # Step 2: Seed the database with initial code blocks
    # await seed_code_blocks()
    
    # Step 3: Load code blocks from the database into the WebSocket manager
    from server.database.crud import get_all_code_blocks
    code_blocks = await get_all_code_blocks()
    manager.load_code_blocks(code_blocks)

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    """
    WebSocket endpoint that manages real-time communication per room.
    Assigns roles, sends initial data, and routes incoming messages.
    """
    # Accept the connection and assign a role
    try:
        role = await manager.connect(websocket, room_id)
    except KeyError:
        await websocket.close(code=4001) # Room not found
        return
    
    await websocket.send_json({"type": "role", "role": role})

    # Send initial code
    await websocket.send_json({
        "type": "code_update",
        "code": manager.active_rooms[room_id]["code"],
    })
    
    try:
        while True:
            raw = await websocket.receive_text()
            await handle_websocket_message(websocket, manager, room_id, raw)
            
    except WebSocketDisconnect:
        await manager.disconnect(websocket, room_id)
    except Exception:
        await manager.disconnect(websocket, room_id)
