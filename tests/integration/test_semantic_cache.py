from app.services.semantic_cache_service import SemanticCache

cache = SemanticCache()

result = cache.search(
    "Explain semantic caching."
)

print(result)