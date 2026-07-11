import pytest
from unittest.mock import Mock,AsyncMock

from app.services.chat_service import ChatService
from app.models.request import ChatRequest
from app.models.response import ChatResponse

class FakeCacheService:

    pass


class FakeProviderService:

    async def generate(self, request):
        pass

def test_check_exact_cache_returns_cached_response(mocker):

    chat_service = ChatService(
        cache_service=FakeCacheService(),
        provider_service=FakeProviderService(),
    )

    request = ChatRequest(
        model="qwen2.5:3b",
        messages=[{
            "role": "user",
            "content": "What is semantic caching?"
        }],

    )

    expected_response = {
        "response": "Semantic caching stores similar responses."
    }

    chat_service.check_exact = Mock(
        return_value=(
            "dummy-cache-key",
            ChatResponse(
                response=expected_response["response"],
                cache_hit=True,
                cache_type="exact",
                similarity_score=None,
            ),
        )
    )

    _, response = chat_service.check_exact(request)

    assert isinstance(response, ChatResponse)

    assert response.cache_hit is True

    assert response.cache_type == "exact"

    assert (
        response.response
        == expected_response["response"]
    )

@pytest.mark.asyncio
async def test_chat_calls_provider_on_cache_miss(mocker):

    cache_service = Mock()
    provider_service = FakeProviderService()

    provider_service.generate = AsyncMock(
        return_value="Generated response"
    )

    cache_service.check_exact_cache.return_value = (None, None)
    cache_service.check_semantic_cache.return_value = (None, None)

    chat_service = ChatService(
        cache_service=cache_service,
        provider_service=provider_service,
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

    await chat_service.chat(request)

    provider_service.generate.assert_awaited_once()

@pytest.mark.asyncio
async def test_chat_cache_miss_flow():

    chat_service = ChatService(
        cache_service=FakeCacheService(),
        provider_service=FakeProviderService(),
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

    chat_service.check_exact = Mock(
        return_value=("cache-key", None)
    )

    chat_service.check_semantic = Mock(
        return_value=("Explain semantic caching", None)
    )

    chat_service.generate_response = AsyncMock(
        return_value="Generated response"
    )

    chat_service.store_exact = Mock()

    chat_service.store_semantic = Mock()

    response = await chat_service.chat(request)

    chat_service.generate_response.assert_awaited_once_with(request)

    chat_service.store_exact.assert_called_once()

    chat_service.store_semantic.assert_called_once()

    assert response.cache_hit is False

@pytest.mark.asyncio
async def test_chat_exact_cache_hit():

    chat_service = ChatService(
        cache_service=FakeCacheService(),
        provider_service=FakeProviderService(),
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

    cached_response = ChatResponse(
        response="Cached response",
        cache_hit=True,
        cache_type="exact",
        similarity_score=None,
    )

    chat_service.check_exact = Mock(
        return_value=("cache-key", cached_response)
    )

    chat_service.check_semantic = Mock()

    chat_service.generate_response = AsyncMock()

    chat_service.store_exact = Mock()

    chat_service.store_semantic = Mock()

    response = await chat_service.chat(request)

    chat_service.generate_response.assert_not_called()

    chat_service.store_exact.assert_not_called()

    chat_service.store_semantic.assert_not_called()

    assert response == cached_response

@pytest.mark.asyncio
async def test_chat_semantic_cache_hit():

    chat_service = ChatService(
        cache_service=FakeCacheService(),
        provider_service=FakeProviderService(),
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

    semantic_response = ChatResponse(
        response="Semantic cached response",
        cache_hit=True,
        cache_type="semantic",
        similarity_score=0.94,
    )

    chat_service.check_exact = Mock(
        return_value=("cache-key", None)
    )

    chat_service.check_semantic = Mock(
        return_value=("Explain semantic caching", semantic_response)
    )

    chat_service.generate_response = AsyncMock()

    chat_service.store_exact = Mock()

    chat_service.store_semantic = Mock()

    response = await chat_service.chat(request)

    chat_service.generate_response.assert_not_called()

    chat_service.store_exact.assert_not_called()

    chat_service.store_semantic.assert_not_called()

    assert response == semantic_response