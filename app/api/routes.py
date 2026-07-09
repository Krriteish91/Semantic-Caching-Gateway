from fastapi import APIRouter
from app.models.request import ChatRequest
from app.models.response import ChatResponse

router = APIRouter()


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
def chat_completions(request: ChatRequest):
    return ChatResponse(
        response="Gateway is working!",
        cache_hit=False,
        cache_type=None,
        similarity_score=None,
    )