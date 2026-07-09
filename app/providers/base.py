from abc import ABC, abstractmethod

from app.models.request import ChatRequest


class BaseLLMProvider(ABC):

    @abstractmethod
    async def generate(self, request: ChatRequest) -> str:
        """
        Generate a response from an LLM provider.
        """
        pass