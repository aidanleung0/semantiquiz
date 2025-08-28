from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect
from connection_manager import connection_manager

router = APIRouter()

@router.websocket("/test")
async def test_websocket(websocket: WebSocket):
    # Accept connection from client
    await connection_manager.test_connect(websocket)

    try:
        while True:
            # Listen to any messages from the server
            await websocket.receive_text()

    except WebSocketDisconnect:
        print("WebSocket test successful")
            
    finally:
        connection_manager.disconnect(job_id)
