"""
Main application entry point.
- Serves FastAPI API routes
- WebSocket endpoint for real-time communication
- Serves React frontend in production (via client/build)
"""
import os
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from server.config import CORS_CONFIG
from server.api.routes import router
from server.utils.init_db import initialize_app
from server.api.websocket_routes import websocket_endpoint

app = FastAPI()

# Include REST API routes
app.include_router(router)

# Allow CORS for development
app.add_middleware(CORSMiddleware, **CORS_CONFIG)

# Initialize database and code blocks
@app.on_event("startup")
async def startup():
    await initialize_app()

# WebSocket endpoint
@app.websocket("/ws/{room_id}")
async def ws_route(websocket: WebSocket, room_id: str):
    await websocket_endpoint(websocket, room_id)

# Serve React frontend in production (only if client/build exists)
if os.getenv("RAILWAY_STATIC") or os.path.exists("client/build"):
    app.mount("/static", StaticFiles(directory="client/build/static"), name="static")

    @app.get("/")
    async def serve_index():
        return FileResponse("client/build/index.html")

    @app.get("/{full_path:path}")
    async def serve_react_routes(full_path: str):
        # React handles its own routing – this ensures direct links to /code/:id work
        return FileResponse("client/build/index.html")
