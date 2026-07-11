from app.cache.redis_cache import RedisCache
from app.services.semantic_cache import SemanticCache
from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService
from app.core.logger import logger

class CacheService:

    def __init__(self):

        self.redis = RedisCache()

        self.semantic = SemanticCache()
        self.embedding_service = EmbeddingService()

        self.qdrant_service = QdrantService()

    def store_exact(
        self,
        cache_key: str,
        response: str,
    ):
        self.redis.set(
            key=cache_key,
            value={
                "response": response,
            },
            ttl=3600,
        )
        logger.info("Stored response in Redis")


    def store_semantic(
        self,
        query: str,
        response: str,
        cache_key: str,
        model: str,
    ):

        embedding = self.embedding_service.generate_embedding(query)

        self.qdrant_service.store_embedding(
            embedding=embedding,
            query=query,
            response=response,
            cache_key=cache_key,
            model=model,
        )
        logger.info("Stored semantic embedding in Qdrant")