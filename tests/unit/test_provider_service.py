from unittest.mock import AsyncMock

import pytest
from app.core.exceptions import ProviderException
from app.services.provider_service import ProviderService
from app.models.request import ChatRequest


@pytest.mark.asyncio
async def test_generate_calls_provider():

    provider_service = ProviderService()

    provider_service.provider = AsyncMock()

    provider_service.provider.generate.return_value = "Generated response"

    request = ChatRequest(
        model="qwen2.5:3b",
        messages=[
            {
                "role": "user",
                "content": "Explain semantic caching",
            }
        ],
    )

    response = await provider_service.generate(request)

    provider_service.provider.generate.assert_awaited_once_with(request)

    assert response == "Generated response"

@pytest.mark.asyncio
async def test_generate_raises_provider_exception():

    provider_service = ProviderService()

    provider_service.provider = AsyncMock()

    provider_service.provider.generate.side_effect = Exception(
        "Provider unavailable"
    )

    request = ChatRequest(
        model="qwen2.5:3b",
        messages=[
            {
                "role": "user",
                "content": "Explain semantic caching",
            }
        ],
    )

    with pytest.raises(ProviderException):
        await provider_service.generate(request)