    
from app.models.request import ChatRequest
from app.models.response import ChatResponse
from app.utils.hashing import generate_cache_key
from app.services.cache_service import CacheService
from app.services.provider_service import ProviderService
from app.core.logger import logger
from app.core.metrics import (
    REQUEST_COUNTER,
    EXACT_CACHE_HITS,
    SEMANTIC_CACHE_HITS,
    CACHE_MISSES,
)

class ChatService:

    def __init__(
        self,
        cache_service: CacheService,
        provider_service: ProviderService,
    ):

        self.cache_service = cache_service
        self.provider_service = provider_service

    
    def check_exact(
        self,
        request: ChatRequest,
    ) -> tuple[str, ChatResponse | None]:

        cache_key = generate_cache_key(request)

        cached = self.cache_service.redis.get(cache_key)
       
        if cached:
            EXACT_CACHE_HITS.inc()
            logger.info("Exact cache hit")
            return (
                cache_key,
                ChatResponse(
                    response=cached["response"],
                    cache_hit=True,
                    cache_type="exact",
                    similarity_score=1.0,
                ),
            )
        
        return cache_key, None

    def check_semantic(
        self,
        request: ChatRequest,
    ) -> tuple[str, ChatResponse | None]:

        query = " ".join(
            message.content
            for message in request.messages
            if message.role == "user"
        )

        semantic_result = self.cache_service.semantic.search(query)

        if semantic_result:

            payload = semantic_result["payload"]

            SEMANTIC_CACHE_HITS.inc()

            logger.info(
                f"Semantic cache hit | score={semantic_result['score']:.4f}"
            )
            return (
                query,
                ChatResponse(
                    response=payload["response"],
                    cache_hit=True,
                    cache_type="semantic",
                    similarity_score=semantic_result["score"],
                ),
            )

        return query, None
    
    def store_semantic(
        self,
        query: str,
        response: str,
        cache_key: str,
        model: str,
    ):
        self.cache_service.store_semantic(
            query=query,
            response=response,
            cache_key=cache_key,
            model=model,
        )
    
    def store_exact(
        self,
        cache_key: str,
        response: str,
    ):
        self.cache_service.store_exact(
            cache_key=cache_key,
            response=response,
        )
    
    async def generate_response(
        self,
        request: ChatRequest,
    ) -> str:

        return await self.provider_service.generate(request)

    def build_response(
            self,
            response: str,
        ) -> ChatResponse:

            return ChatResponse(
                response=response,
                cache_hit=False,
                cache_type=None,
                similarity_score=None,
            )
    async def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:

        REQUEST_COUNTER.inc()
        logger.info("ChatService.chat() called")
        cache_key, cached_response = self.check_exact(request)

        if cached_response:
            return cached_response

        query, semantic_response = self.check_semantic(request)

        if semantic_response:
            return semantic_response

        CACHE_MISSES.inc()

        logger.info("Cache miss")
        
        response = await self.generate_response(request)

        self.store_exact(
            cache_key=cache_key,
            response=response,
        )

        self.store_semantic(
            query=query,
            response=response,
            cache_key=cache_key,
            model=request.model,
        )

        return self.build_response(response)