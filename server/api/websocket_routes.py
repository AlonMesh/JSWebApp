"""
WebSocket route for real-time collaboration (code editing, students count...)
"""
from fastapi import WebSocket, WebSocketDisconnect
from server.socket_manager import manager
from server.websocket.handlers import handle_websocket_message

async def websocket_endpoint(websocket: WebSocket, room_id: str):
    """WebSocket endpoint for handling connections to a specific room.
    This function manages the connection lifecycle, including joining and leaving rooms,
    and sending/receiving messages.
    """
    try:
        # Connect the WebSocket to the room (this will also return the role of the user)
        role = await manager.connect(websocket, room_id)
    except KeyError:
        await websocket.close(code=4001)  # Room not found
        return

    # Send the role of the user to the client 
    await websocket.send_json({"type": "role", "role": role})
    await websocket.send_json({
        "type": "code_update",
        "code": manager.active_rooms[room_id]["code"],
    })

    try:
        while True:
            # Wait for a message from the client
            raw = await websocket.receive_text()
            await handle_websocket_message(websocket, manager, room_id, raw)
    except (WebSocketDisconnect, Exception):
        # Handle disconnection or other exceptions 
        await manager.disconnect(websocket, room_id)
