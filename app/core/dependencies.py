from functools import lru_cache

from app.services.cache_service import CacheService
from app.services.chat_service import ChatService
from app.services.provider_service import ProviderService
from app.services.health_service import HealthService


@lru_cache
def get_cache_service():
    return CacheService()


@lru_cache
def get_provider_service():
    return ProviderService()


@lru_cache
def get_chat_service():

    return ChatService(
        cache_service=get_cache_service(),
        provider_service=get_provider_service(),
    )

@lru_cache
def get_health_service():
    return HealthService()