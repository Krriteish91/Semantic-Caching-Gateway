from pydantic import BaseModel


class ChatResponse(BaseModel):
    response: str

    cache_hit: bool

    cache_type: str | None = None

    similarity_score: float | None = None