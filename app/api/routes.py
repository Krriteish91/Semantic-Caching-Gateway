from fastapi import APIRouter
from app.models.request import ChatRequest
from app.models.response import ChatResponse

from app.core.exceptions import ProviderException
from app.core.dependencies import get_chat_service
from app.core.logger import logger

router = APIRouter()
chat_service = get_chat_service()


@router.get("/")
def root():
    
    return {
        "status": "running",
        "service": "Semantic Cache Gateway"
    }


@router.get("/health")
def health():
    return {
        "api": "healthy",
        "redis": "not connected yet"
    }

@router.post("/v1/chat/completions",response_model=ChatResponse)
async def chat_completions(request: ChatRequest):
    
    return await chat_service.chat(request)