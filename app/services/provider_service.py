from app.providers.ollama_provider import OllamaProvider


class ProviderService:

    def __init__(self):

        self.provider = OllamaProvider()

    async def generate(self, request):

        return await self.provider.generate(request)