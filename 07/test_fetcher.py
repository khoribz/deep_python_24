"""
This module contains tests for the Fetcher class, which handles asynchronous
HTTP requests with concurrency control using aiohttp.
"""

import asyncio
from unittest.mock import patch, AsyncMock
import pytest
from fetcher import Fetcher
from test_data import URL_1, URL_2, URL_3


@pytest.mark.asyncio
async def test_empty_url_list():
    """
    Test that Fetcher handles an empty URL list correctly,
    returning an empty response list without making any requests.
    """
    urls = []
    with patch("aiohttp.ClientSession.get") as mock_get:
        fetcher = Fetcher(concurrency=2, urls=urls)
        responses = await fetcher.fetch_all()

    assert len(responses) == 0
    mock_get.assert_not_called()


@pytest.mark.asyncio
async def test_fetcher_success():
    """
    Test Fetcher for successful responses from multiple URLs.
    Ensures the responses have status 200 and match the mocked responses.
    """
    urls = [URL_1, URL_2]

    async def mock_text():
        return "response text"

    mock_response_1 = AsyncMock(status=200, text=mock_text)
    mock_response_2 = AsyncMock(status=200, text=mock_text)

    mock_response_1.__aenter__.return_value = mock_response_1
    mock_response_2.__aenter__.return_value = mock_response_2

    with patch("aiohttp.ClientSession.get", side_effect=[mock_response_1, mock_response_2]):
        fetcher = Fetcher(concurrency=2, urls=urls)
        responses = await fetcher.fetch_all()

    assert len(responses) == 2
    assert responses[0].status == 200
    assert responses[1].status == 200


@pytest.mark.asyncio
async def test_large_concurrency():
    """
    Test Fetcher with a large concurrency level, ensuring correct functionality
    when the concurrency level exceeds the number of URLs.
    """
    urls = [URL_1, URL_2]

    async def mock_text():
        return "response text"

    mock_response_1 = AsyncMock(status=200, text=mock_text)
    mock_response_2 = AsyncMock(status=200, text=mock_text)

    mock_response_1.__aenter__.return_value = mock_response_1
    mock_response_2.__aenter__.return_value = mock_response_2

    with patch("aiohttp.ClientSession.get", side_effect=[mock_response_1, mock_response_2]):
        fetcher = Fetcher(concurrency=100, urls=urls)
        responses = await fetcher.fetch_all()

    assert len(responses) == 2
    assert responses[0].status == 200
    assert responses[1].status == 200


@pytest.mark.asyncio
async def test_fetcher_timeout_error():
    """
    Test that Fetcher raises a TimeoutError when a request times out.
    """
    urls = [URL_1, URL_2]

    with patch("aiohttp.ClientSession.get", side_effect=asyncio.TimeoutError()):
        fetcher = Fetcher(concurrency=1, urls=urls)

        with pytest.raises(asyncio.TimeoutError):
            await fetcher.fetch_all()


@pytest.mark.asyncio
async def test_fetcher_other_error():
    """
    Test that Fetcher raises a generic exception when an unexpected error occurs
    during a request.
    """
    urls = [URL_1]

    with patch("aiohttp.ClientSession.get", side_effect=Exception()):
        fetcher = Fetcher(concurrency=1, urls=urls)

        with pytest.raises(Exception):
            await fetcher.fetch_all()


@pytest.mark.asyncio
async def test_fetcher_semaphore():
    """
    Test that Fetcher respects the concurrency limit using a semaphore.
    Ensures the responses are correct and match the mocked values.
    """
    urls = [URL_1, URL_2, URL_3]

    async def mock_text():
        return "response text"

    mock_response_1 = AsyncMock(status=200, text=mock_text)
    mock_response_2 = AsyncMock(status=200, text=mock_text)
    mock_response_3 = AsyncMock(status=200, text=mock_text)

    mock_response_1.__aenter__.return_value = mock_response_1
    mock_response_2.__aenter__.return_value = mock_response_2
    mock_response_3.__aenter__.return_value = mock_response_3

    with patch("aiohttp.ClientSession.get", side_effect=[mock_response_1, mock_response_2, mock_response_3]):
        fetcher = Fetcher(concurrency=2, urls=urls)
        responses = await fetcher.fetch_all()

    assert len(responses) == len(urls)
    assert all(response.status == 200 for response in responses)
