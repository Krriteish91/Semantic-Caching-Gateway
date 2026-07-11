from app.cache.redis_cache import RedisCache
from app.services.qdrant_service import QdrantService


class HealthService:

    def __init__(self):

        self.redis = RedisCache()

        self.qdrant = QdrantService()
        
    def check_health(self) -> dict:

        redis_status = "up" if self.redis.ping() else "down"

        qdrant_status = "up" if self.qdrant.ping() else "down"

        overall_status = (
            "healthy"
            if redis_status == "up" and qdrant_status == "up"
            else "unhealthy"
        )

        return {
            "status": overall_status,
            "services": {
                "redis": redis_status,
                "qdrant": qdrant_status,
            },
        }