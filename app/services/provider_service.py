from app.providers.ollama_provider import OllamaProvider
from app.core.exceptions import ProviderException
from app.core.logger import logger
import time

class ProviderService:

    def __init__(self):

        self.provider = OllamaProvider()

    async def generate(self, request):

        try:

            logger.info(f"Calling provider | model={request.model}")

            start_time = time.perf_counter()

            response = await self.provider.generate(request)

            elapsed_ms = (time.perf_counter() - start_time) * 1000

            logger.info(
                f"Provider response received | latency={elapsed_ms:.2f} ms"
            )

            return response

        except Exception as e:

            logger.exception("Provider request failed")

            raise ProviderException(str(e))