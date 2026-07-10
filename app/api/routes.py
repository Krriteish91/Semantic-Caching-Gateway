from fastapi import APIRouter
from app.models.request import ChatRequest
from app.models.response import ChatResponse
from app.providers.ollama_provider import OllamaProvider
from app.utils.hashing import generate_cache_key
from app.cache.redis_cache import RedisCache


router = APIRouter()
provider = OllamaProvider()
cache = RedisCache()


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
    cache_key = generate_cache_key(request)

    cached = cache.get(cache_key)

    if cached:

        return ChatResponse(
            response=cached["response"],
            cache_hit=True,
            cache_type="exact",
            similarity_score=1.0,
        )
    response = await provider.generate(request)
    cache.set(
        key=cache_key,
        value={
            "response": response,
        },
        ttl=3600,  # 1 hour
    )

    return ChatResponse(
        response=response,
        cache_hit=False,
        cache_type=None,
        similarity_score=None,
    )