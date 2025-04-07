from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from websocket_manager import ConnectionManager
import json

app = FastAPI()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = ConnectionManager()

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
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
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                continue  # Ignore malformed messages

            if data.get("type") == "code_update":
                manager.active_rooms[room_id]["code"] = data["code"]
                for conn in manager.active_rooms[room_id]["connections"]:
                    if conn != websocket:
                        await conn.send_json({
                            "type": "code_update",
                            "code": data["code"]
                        })
    except WebSocketDisconnect:
        await manager.disconnect(websocket, room_id)
    except Exception:
        await manager.disconnect(websocket, room_id)
