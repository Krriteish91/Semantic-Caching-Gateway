from app.cache.redis_cache import RedisCache
from app.services.semantic_cache import SemanticCache


class CacheService:

    def __init__(self):

        self.redis = RedisCache()

        self.semantic = SemanticCache()