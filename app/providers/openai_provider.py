from openai import AsyncOpenAI

from app.core.config import settings
from app.models.request import ChatRequest
from app.providers.base import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):

    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    async def generate(self, request: ChatRequest) -> str:

        response = await self.client.chat.completions.create(
            model=request.model,
            messages=[
                {
                    "role": message.role,
                    "content": message.content,
                }
                for message in request.messages
            ],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        return response.choices[0].message.content