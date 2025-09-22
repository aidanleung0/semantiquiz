from fastapi import APIRouter

from routes.http_routes import evaluation, auth
from routes.websocket_routes import job_websocket
from routes.websocket_routes import test_websocket

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/api/auth", tags=["auth"])
api_router.include_router(evaluation.router, prefix="/api")
api_router.include_router(job_websocket.router, prefix="/api/ws")
api_router.include_router(test_websocket.router, prefix="/api/ws")