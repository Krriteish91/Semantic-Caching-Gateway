from unittest.mock import Mock

from app.services.cache_service import CacheService

def test_store_exact_calls_redis_set():

    cache_service = CacheService()

    cache_service.redis = Mock()

    cache_service.store_exact(
        cache_key="test-key",
        response="Test response",
    )

    cache_service.redis.set.assert_called_once()

def test_store_semantic_generates_embedding():

    cache_service = CacheService()

    cache_service.embedding_service = Mock()

    cache_service.qdrant_service = Mock()

    cache_service.embedding_service.generate_embedding.return_value = [0.1, 0.2, 0.3]

    cache_service.store_semantic(
        query="What is semantic caching?",
        response="Semantic caching stores similar responses.",
        cache_key="test-key",
        model="qwen2.5:3b",
    )

    cache_service.embedding_service.generate_embedding.assert_called_once_with(
        "What is semantic caching?"
    )

def test_store_semantic_stores_embedding_in_qdrant():

    cache_service = CacheService()

    cache_service.embedding_service = Mock()
    cache_service.qdrant_service = Mock()

    embedding = [0.1, 0.2, 0.3]

    cache_service.embedding_service.generate_embedding.return_value = embedding

    cache_service.store_semantic(
        query="What is semantic caching?",
        response="Semantic caching stores similar responses.",
        cache_key="test-key",
        model="qwen2.5:3b",
    )

    cache_service.qdrant_service.store_embedding.assert_called_once_with(
        embedding=embedding,
        query="What is semantic caching?",
        response="Semantic caching stores similar responses.",
        cache_key="test-key",
        model="qwen2.5:3b",
    )