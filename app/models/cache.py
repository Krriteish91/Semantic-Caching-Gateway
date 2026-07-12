from pydantic import BaseModel
from uuid import uuid4
from time import time


class CacheEntry(BaseModel):

    id: str = Field(default_factory=lambda: str(uuid4()))

    query_hash: str

    query: str

    response: str

    created_at: float = Field(default_factory=time)

    ttl: int

    model: str

    embedding: list[float] | None = None

    metadata: dict = Field(default_factory=dict)