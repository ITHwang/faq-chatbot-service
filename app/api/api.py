from fastapi import APIRouter
from app.api.endpoints import conversation, health

api_router = APIRouter()
api_router.include_router(conversation.router, prefix="/conversation", tags=["conversation"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
