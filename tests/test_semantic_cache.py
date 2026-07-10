from app.services.semantic_cache import SemanticCache

cache = SemanticCache()

result = cache.search(
    "Explain semantic caching."
)

print(result)