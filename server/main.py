# === Built-in ===
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

# === Internal ===
from server.config import CORS_CONFIG
from server.api.routes import router
from server.utils.init_db import initialize_app
from server.api.websocket_routes import websocket_endpoint

# === App init ===
app = FastAPI()
app.include_router(router)

# === CORS ===
app.add_middleware(CORSMiddleware, **CORS_CONFIG)

# === WebSocket manager ===
@app.on_event("startup")
async def startup():
    await initialize_app()

# === WebSocket routes ===
@app.websocket("/ws/{room_id}")
async def ws_route(websocket: WebSocket, room_id: str):
    await websocket_endpoint(websocket, room_id)
