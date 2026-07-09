from app.cache.redis_cache import RedisCache

cache = RedisCache()

cache.set(
    key="test",
    value={
        "message": "Redis is working!"
    },
    ttl=60,
)

result = cache.get("test")

print(result)