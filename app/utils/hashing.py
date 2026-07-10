import hashlib

from app.models.request import ChatRequest


def generate_cache_key(request: ChatRequest) -> str:
    """
    Generate a deterministic cache key for an LLM request.
    """

    content = "|".join(
        [
            request.model,
            str(request.temperature),
            str(request.max_tokens),
            "".join(
                f"{message.role}:{message.content}"
                for message in request.messages
            ),
        ]
    )

    return hashlib.sha256(content.encode()).hexdigest()