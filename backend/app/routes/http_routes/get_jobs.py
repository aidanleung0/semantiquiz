from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect, Depends, Request
from schemas.get_jobs import GetJobsRequest

router = APIRouter()

@router.get("/get-jobs", response_model=CompareResponse)
async def get_jobs():
    return 
