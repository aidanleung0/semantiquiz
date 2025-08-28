from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect, Depends, Request
from schemas.compare import CompareRequest, CompareResponse
from services.compare_request import compare_request
from message_queue.producers.message_producer import MessageProducer

router = APIRouter()

def get_publisher(request: Request) -> MessageProducer:
    return request.app.state.producer

@router.post("/compare-definition", response_model=CompareResponse)
async def compare_definition(payload: CompareRequest, producer: MessageProducer=Depends(get_publisher)):
    return compare_request(producer=producer, payload=payload)
