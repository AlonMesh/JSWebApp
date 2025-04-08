from fastapi import WebSocket
from typing import List, Dict
from asyncio import create_task

class WebSocketManager:
    """
    Manages WebSocket connections, rooms, and real-time interactions
    between mentors and students.
    """

    def __init__(self):
        # Active rooms mapped by room_id
        self.active_rooms: Dict[str, Dict] = {}
        
        # Preloaded code blocks with their solutions
        self.code_blocks = {}
        
    def load_code_blocks(self, code_blocks_list):
        self.code_blocks = {
            str(cb.id): {
                "id": cb.id,
                "title": cb.title,
                "initial_code": cb.initial_code,
                "solution_code": cb.solution_code
            } for cb in code_blocks_list
        }


    async def connect(self, websocket: WebSocket, room_id: str) -> str:
        """
        Accepts a new WebSocket connection and
        Initializes the room if it doesn't exist.
        """
        await websocket.accept()

        room = self.initialize_room(room_id)
        role = self.assign_role(websocket, room)

        # Add the connection to the list of active connections 
        room["connections"].append(websocket)
        await self.broadcast_participants(room_id)
        
        # Return the assigned role
        return role

    async def disconnect(self, websocket: WebSocket, room_id: str):
        """
        Handles the disconnection of a WebSocket from a room.
        Removes the connection and broadcasts updated participant data.
        """
        room = self.active_rooms.get(room_id)
        
        # If the room doesn't exist, do nothing (might happen if the room was deleted while a user was connected)
        if not room:
            return

        # Check if the disconnected user is a mentor or a student and handle accordingly
        if websocket == room.get("mentor"):
            self.handle_mentor_disconnect(room)
        elif websocket in room.get("students", []):
            self.handle_student_disconnect(websocket, room)

        # Remove the connection from the list of active connections
        if websocket in room["connections"]:
            room["connections"].remove(websocket)

        if room["connections"]:
            create_task(self.broadcast_participants(room_id))
            
        else:
            del self.active_rooms[room_id]

    async def broadcast_participants(self, room_id: str):
        """
        Sends an update to all clients in the room with the current
        number of students
        """
        room = self.active_rooms.get(room_id)
        
        # If the room doesn't exist, do nothing
        if not room:
            return

        data = {
            "type": "participants",
            "students_count": len(room["students"]),
            "mentor": room["mentor"] is not None
        }

        # Send the data to all connections in the room
        for conn in room["connections"]:
            try:
                await conn.send_json(data)
            except:
                pass

    def initialize_room(self, room_id: str):
        """
        Creates a new room with initial fields.
        """
        return self.active_rooms.setdefault(room_id, {
            "mentor": None,
            "students": [],
            "connections": [],
            "code": self.code_blocks[room_id]["initial_code"]
        })
        
    def assign_role(self, websocket: WebSocket, room: Dict) -> str:
        """
        Assigns a role to the new connection based on room state.
        """
        if room["mentor"] is None:
            room["mentor"] = websocket
            return "mentor"
        else:
            room["students"].append(websocket)
            return "student"

    def handle_mentor_disconnect(self, room: Dict):
        """
        Removes the mentor from the room and clears all students + notifies them.
        """
        room["mentor"] = None
        for student in room["students"]:
            try:
                create_task(student.send_json({"type": "redirect"}))
            except:
                pass
        room["students"].clear()

    def handle_student_disconnect(self, websocket: WebSocket, room: Dict):
        """
        Removes a student from the room.
        """
        if websocket in room["students"]:
            room["students"].remove(websocket)

    def get_room_code(self, room_id: str) -> str:
        """
        Returns the current code of a room.
        """
        return self.active_rooms[room_id]["code"]

    def update_room_code(self, room_id: str, new_code: str):
        """
        Updates the code in the specified room.
        """
        self.active_rooms[room_id]["code"] = new_code

    def get_room_connections(self, room_id: str):
        """
        Returns all WebSocket connections for a room.
        """
        return self.active_rooms[room_id]["connections"]

    def get_code_block_solution(self, room_id: str) -> str:
        """
        Retrieves the solution code for a specific code block.
        """
        return self.code_blocks[room_id]["solution_code"]