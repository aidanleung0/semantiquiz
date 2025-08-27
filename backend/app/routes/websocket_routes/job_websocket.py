from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect
from connection_manager import connection_manager

router = APIRouter()

@router.websocket("/ws/{job_id}")
async def LLM_request_websocket(websocket: WebSocket, job_id: str):
    # Accept connection from client
    await connection_manager.connect(job_id, websocket)

    try:
        while True:
            # Listen to any messages from the server
            await websocket.receive_text()

    except WebSocketDisconnect:
        print(f"Client disconnected from job {job_id}")
            
    finally:
        connection_manager.disconnect(job_id)
