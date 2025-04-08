from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from websocket.manager import WebSocketManager
from websocket.handlers import handle_websocket_message

app = FastAPI()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = WebSocketManager()

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    """
    WebSocket endpoint that manages real-time communication per room.
    Assigns roles, sends initial data, and routes incoming messages.
    """
    # Accept the connection and assign a role
    role = await manager.connect(websocket, room_id)
    await websocket.send_json({"type": "role", "role": role})

    # Send initial code
    await websocket.send_json({
        "type": "code_update",
        "code": manager.active_rooms[room_id]["code"]
    })
    
    try:
        while True:
            raw = await websocket.receive_text()
            await handle_websocket_message(websocket, manager, room_id, raw)
            
    except WebSocketDisconnect:
        await manager.disconnect(websocket, room_id)
    except Exception:
        await manager.disconnect(websocket, room_id)
