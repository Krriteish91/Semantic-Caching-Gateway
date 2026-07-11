from prometheus_client import Counter


REQUEST_COUNTER = Counter(
    "semantic_cache_requests_total",
    "Total number of chat requests",
)