from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from websocket_manager import ConnectionManager

app = FastAPI()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Write the code block to home page
@app.get("/")
def read_root():
    return {"message": "Welcome to the Code Blocks API!"}


# WebSocket connection manager
manager = ConnectionManager()

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    role = await manager.connect(websocket, room_id)
    await websocket.send_json({"type": "role", "role": role})  # Send the role to the connected WebSocket
    
    try:
        while True:
            # Keep the connection open and listen for messages
            await websocket.receive_text()  
    except WebSocketDisconnect:
        await manager.disconnect(websocket, room_id)