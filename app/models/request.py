from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str

    messages: list[Message]

    temperature: float = Field(default=1.0)

    max_tokens: int = Field(default=512)

    metadata: dict = Field(default_factory=dict)