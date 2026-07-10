class SemanticCacheException(Exception):
    """
    Base exception for the Semantic Cache Gateway.
    """
    pass


class ProviderException(SemanticCacheException):
    pass


class RedisCacheException(SemanticCacheException):
    pass


class QdrantException(SemanticCacheException):
    pass


class EmbeddingException(SemanticCacheException):
    pass


class SemanticSearchException(SemanticCacheException):
    pass


class CachePolicyException(SemanticCacheException):
    pass