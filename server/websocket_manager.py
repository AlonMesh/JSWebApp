from fastapi import WebSocket
from typing import List, Dict
from asyncio import create_task

class ConnectionManager:
    def __init__(self):
        self.active_rooms: Dict[str, Dict] = {}  # Dictionary to hold active rooms and their connections
        
    # Method to connect a WebSocket to a room
    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()  # Accept the WebSocket connection
        
        room = self.active_rooms.setdefault(room_id, {
            "mentor": None,
            "students": [],
            "connections": []
        })
        
        # Assign the mentor if not already assigned
        if room["mentor"] is None:
            room["mentor"] = websocket
            role = "mentor"
        else:
            room["students"].append(websocket)
            role = "student"
            
        room["connections"].append(websocket)  # Add the WebSocket to the room's connections
        await self.broadcast_participants(room_id)  # Notify all participants of the new connection
        
        return role  # Return the role of the connected WebSocket (mentor or student)
    
    # Method to disconnect a WebSocket from a room
    async def disconnect(self, websocket: WebSocket, room_id: str):
        room = self.active_rooms.get(room_id)
        if not room:
            return  # Room does not exist
        
        # If the WebSocket is a student, simply remove it from the list of students
        if websocket in room["students"]:
            room["students"].remove(websocket)
            
            # Notify remaining participants of the updated list
            create_task(self.broadcast_participants(room_id))
            
        # If the WebSocket is the mentor, remove it and close the room
        elif websocket == room["mentor"]:
            room["mentor"] = None
            
            # Redirect all students to lobby
            for student in room["students"]:
                try: 
                    # Notify student to redirect to lobby
                    create_task(student.send_json({"type": "redirect"}))  
                except:
                    pass
            # Clear the list of students after redirecting
            room["students"].clear()  
            
            if websocket in room["connections"]:
                room["connections"].remove(websocket)
                
                # Notify remaining participants of the updated list
                create_task(self.broadcast_participants(room_id))
                
            # Update the room's connections if someone is still connected
            if room["connections"]:
                # Notify remaining participants of the updated list
                create_task(self.broadcast_participants(room_id))
            else:
                del self.active_rooms[room_id]
                

    async def broadcast_participants(self, room_id: str):
        room = self.active_rooms.get(room_id)
        if not room:
            return  # Room does not exist
        
        data = {
            "type": "participants",
            "students_count": len(room["students"]),
            "mentor": room["mentor"] is not None
        }
        for conn in room["connections"]:
            try:
                await conn.send_json(data)  # Send the participant data to all connections in the room
            except:
                pass