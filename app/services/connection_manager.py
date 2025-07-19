from typing import List, Dict
from fastapi import WebSocket
from datetime import datetime
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[Dict] = []

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections.append({
            "websocket": websocket,
            "client_id": client_id,
            "connected_at": datetime.now().isoformat()
        })
        print(f"New client connected: {client_id}")
        await self.broadcast_system_message(f"Client {client_id} connected")

    async def disconnect(self, websocket: WebSocket):
        for connection in self.active_connections:
            if connection["websocket"] == websocket:
                self.active_connections.remove(connection)
                print(f"Client disconnected: {connection['client_id']}")
                await self.broadcast_system_message(f"Client {connection['client_id']} disconnected")
                break

    async def send_message(self, websocket: WebSocket, message: str):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection["websocket"].send_text(message)

    async def broadcast_system_message(self, message: str):
        system_msg = {
            "type": "system",
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast(json.dumps(system_msg))

manager = ConnectionManager()
