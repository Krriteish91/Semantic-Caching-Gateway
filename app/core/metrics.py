from prometheus_client import Counter

# Request Metrics
REQUEST_COUNTER = Counter(
    "semantic_cache_requests_total",
    "Total number of chat requests",
)

# Cache Metrics
EXACT_CACHE_HITS = Counter(
    "semantic_cache_exact_hits_total",
    "Total number of exact cache hits",
)
SEMANTIC_CACHE_HITS = Counter(
    "semantic_cache_semantic_hits_total",
    "Total number of semantic cache hits",
)
CACHE_MISSES = Counter(
    "semantic_cache_misses_total",
    "Total number of cache misses",
)