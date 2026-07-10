from fastapi import APIRouter
from app.models.request import ChatRequest
from app.models.response import ChatResponse
from app.providers.ollama_provider import OllamaProvider
from app.utils.hashing import generate_cache_key
from app.cache.redis_cache import RedisCache
from app.services.semantic_cache import SemanticCache

router = APIRouter()
provider = OllamaProvider()
cache = RedisCache()
semantic_cache = SemanticCache()

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

    query = " ".join(
        message.content
        for message in request.messages
        if message.role == "user"
    )

    semantic_result = semantic_cache.search(query)

    if semantic_result:

        payload = semantic_result["payload"]

        return ChatResponse(
            response=payload["response"],
            cache_hit=True,
            cache_type="semantic",
            similarity_score=semantic_result["score"],
        )

    
    response = await provider.generate(request)
    cache.set(
        key=cache_key,
        value={
            "response": response,
        },
        ttl=3600,  # 1 hour
    )
    embedding = semantic_cache.embedding_service.generate_embedding(query)

    semantic_cache.qdrant_service.store_embedding(
        embedding=embedding,
        query=query,
        response=response,
        cache_key=cache_key,
        model=request.model,
    )
    return ChatResponse(
        response=response,
        cache_hit=False,
        cache_type=None,
        similarity_score=None,
    )