from fastapi import APIRouter
from app.models.request import ChatRequest
from app.models.response import ChatResponse

from app.core.exceptions import ProviderException
from app.services.health_service import HealthService
from app.core.dependencies import get_chat_service, get_health_service
from app.core.logger import logger

router = APIRouter()
chat_service = get_chat_service()
health_service = get_health_service()

@router.get("/")
def root():
    
    return {
        "status": "running",
        "service": "Semantic Cache Gateway"
    }


@router.get("/health")
def health():

    return health_service.check_health()

@router.post("/v1/chat/completions",response_model=ChatResponse)
async def chat_completions(request: ChatRequest):
    
    return await chat_service.chat(request)