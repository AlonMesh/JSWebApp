import json
from fastapi import WebSocket
from websocket.manager import WebSocketManager
from utils.match import is_solution_match


async def handle_websocket_message(websocket: WebSocket, manager: WebSocketManager, room_id: str, raw: str):
    """
    Handles an incoming WebSocket message.
    Parses the message and delegates handling by type.
    """
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return  # Ignore invalid JSON

    msg_type = data.get("type")

    if msg_type == "code_update":
        await handle_code_update(websocket, manager, room_id, data)
    # TODO elif msg_type == "...": # Reset? chat? hint? etc.


async def handle_code_update(websocket: WebSocket, manager: WebSocketManager, room_id: str, data: dict):
    """
    Handles a code update message: updates the shared room code,
    broadcasts to other users, and checks if the solution is correct.
    """
    code = data.get("code")
    if code is None:
        return

    manager.update_room_code(room_id, code)

    for conn in manager.get_room_connections(room_id):
        if conn != websocket:
            await conn.send_json({
                "type": "code_update",
                "code": code
            })

    solution = manager.get_code_block_solution(room_id)
    if is_solution_match(code, solution):
        for conn in manager.get_room_connections(room_id):
            await conn.send_json({"type": "solved"})
