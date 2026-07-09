from fastapi import APIRouter
from app.models.request import ChatRequest
from app.models.response import ChatResponse
from app.providers.ollama_provider import OllamaProvider

router = APIRouter()
provider = OllamaProvider()

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
    response = await provider.generate(request)

    return ChatResponse(
        response=response,
        cache_hit=False,
        cache_type=None,
        similarity_score=None,
    )