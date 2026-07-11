import redis
import json
from app.core.config import settings


class RedisCache:

    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True,
        )
    def set(self, key: str, value: dict, ttl: int):

        self.client.set(
            key,
            json.dumps(value),
            ex=ttl
        )
    def get(self, key: str):

        value = self.client.get(key)

        if value is None:
            return None

        return json.loads(value)
    def ping(self) -> bool:

        try:

            return self.client.ping()

        except Exception:

            return False