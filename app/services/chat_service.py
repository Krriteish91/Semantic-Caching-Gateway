from app.cache.redis_cache import RedisCache
from app.providers.ollama_provider import OllamaProvider
from app.services.semantic_cache import SemanticCache
from app.models.request import ChatRequest
from app.models.response import ChatResponse
from app.utils.hashing import generate_cache_key

class ChatService:

    def __init__(self):

        self.provider = OllamaProvider()

        self.cache = RedisCache()

        self.semantic_cache = SemanticCache()
    
    def check_exact_cache(
        self,
        request: ChatRequest,
    ) -> tuple[str, ChatResponse | None]:

        cache_key = generate_cache_key(request)

        cached = self.cache.get(cache_key)

        if cached:

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

    def check_semantic_cache(
        self,
        request: ChatRequest,
    ) -> tuple[str, ChatResponse | None]:

        query = " ".join(
            message.content
            for message in request.messages
            if message.role == "user"
        )

        semantic_result = self.semantic_cache.search(query)

        if semantic_result:

            payload = semantic_result["payload"]

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
    async def generate_response(
        self,
        request: ChatRequest,
    ) -> str:

        return await self.provider.generate(request)