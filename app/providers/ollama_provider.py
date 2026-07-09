import httpx

from app.models.request import ChatRequest
from app.providers.base import BaseLLMProvider


class OllamaProvider(BaseLLMProvider):

    def __init__(self):
        self.base_url = "http://host.docker.internal:11434"
        # Linux users may change this later if needed.

    async def generate(self, request: ChatRequest) -> str:

        prompt = "\n".join(
            f"{message.role}: {message.content}"
            for message in request.messages
        )

        async with httpx.AsyncClient(timeout=120) as client:

            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": request.model,
                    "prompt": prompt,
                    "stream": False,
                },
            )

            response.raise_for_status()

            data = response.json()

            return data["response"]