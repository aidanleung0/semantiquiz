from fastapi import WebSocket
import threading

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        self.lock = threading.Lock()

    async def test_connect(self, websocket: WebSocket):
        await websocket.accept()

    async def connect(self, key: str, websocket: WebSocket):
        """
        Accepts and stores a new WebSocket connection.
        """
        await websocket.accept()
        with self.lock:
            self.active_connections[key] = websocket

    def disconnect(self, key: str):
        with self.lock:
            if key in self.active_connections:
                del self.active_connections[key]

    async def send_message(self, key: str, message: dict):
        with self.lock:
            websocket = self.active_connections.get(key)

        if websocket:
            await websocket.send_json(message)

connection_manager = ConnectionManager()
