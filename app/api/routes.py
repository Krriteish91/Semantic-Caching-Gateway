from fastapi import APIRouter
from app.models.request import ChatRequest
from app.models.response import ChatResponse
from app.providers.ollama_provider import OllamaProvider
from app.utils.hashing import generate_cache_key
from app.cache.redis_cache import RedisCache
from app.services.semantic_cache import SemanticCache
from app.core.exceptions import ProviderException
from app.services.chat_service import ChatService

router = APIRouter()
chat_service = ChatService()
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
    
    cache_key, cached_response = chat_service.check_exact_cache(request)

    if cached_response:
        return cached_response

    query, semantic_response = chat_service.check_semantic_cache(
        request
    )

    if semantic_response:
        return semantic_response

    
    response = await chat_service.generate_response(request)
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