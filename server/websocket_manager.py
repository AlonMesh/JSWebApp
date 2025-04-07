from fastapi import WebSocket
from typing import List, Dict
from asyncio import create_task

class ConnectionManager:
    def __init__(self):
        # Store room data by room_id
        self.active_rooms: Dict[str, Dict] = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()

        room = self.active_rooms.setdefault(room_id, {
            "mentor": None,
            "students": [],
            "connections": [],
            "code": ""
        })

        if room["mentor"] is None:
            room["mentor"] = websocket
            role = "mentor"
        else:
            room["students"].append(websocket)
            role = "student"

        room["connections"].append(websocket)
        await self.broadcast_participants(room_id)
        return role

    async def disconnect(self, websocket: WebSocket, room_id: str):
        room = self.active_rooms.get(room_id)
        if not room:
            return

        if websocket in room["students"]:
            room["students"].remove(websocket)

        elif websocket == room["mentor"]:
            room["mentor"] = None
            for student in room["students"]:
                try:
                    create_task(student.send_json({"type": "redirect"}))
                except:
                    pass
            room["students"].clear()

        if websocket in room["connections"]:
            room["connections"].remove(websocket)

        if room["connections"]:
            create_task(self.broadcast_participants(room_id))
        else:
            del self.active_rooms[room_id]

    async def broadcast_participants(self, room_id: str):
        room = self.active_rooms.get(room_id)
        if not room:
            return

        data = {
            "type": "participants",
            "students_count": len(room["students"]),
            "mentor": room["mentor"] is not None
        }

        for conn in room["connections"]:
            try:
                await conn.send_json(data)
            except:
                pass
