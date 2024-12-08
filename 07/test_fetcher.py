"""
This module contains tests for the Fetcher class, which handles asynchronous
HTTP requests with concurrency control using aiohttp.
"""
from unittest.mock import patch, MagicMock, call

import asyncio
import pytest
from aiohttp import ClientSession
from aioresponses import aioresponses
from yarl import URL

from fetcher import Fetcher


@pytest.mark.asyncio
async def test_fetch_single_url():
    """ Test the fetch method with a single URL """
    fetcher = Fetcher(concurrency=1, url_file="urls.txt")

    with aioresponses() as m:
        m.get('http://google.com', status=200, body="Response from google.com")

        async with ClientSession() as session:
            result = await fetcher.fetch(session, 'http://google.com')
            assert result == "Response from google.com"


@pytest.mark.asyncio
async def test_fetch_timeout():
    """ Test the fetch method when a timeout occurs """
    fetcher = Fetcher(concurrency=1, url_file="urls.txt")

    with aioresponses() as m:
        m.get('http://example.com', exception=asyncio.TimeoutError)

        async with ClientSession() as session:
            with pytest.raises(asyncio.TimeoutError):
                await fetcher.fetch(session, 'http://example.com')


@pytest.mark.asyncio
async def test_fetch_urls_in_batches():
    """ Test if the URLs are being read and fetched in batches correctly """
    fetcher = Fetcher(concurrency=3, url_file="urls.txt")

    urls = ['http://example.com', 'http://example.org', 'http://example.net']

    with aioresponses() as m:
        m.get('http://example.com', status=200, body="Response from example.com")
        m.get('http://example.org', status=200, body="Response from example.org")
        m.get('http://example.net', status=200, body="Response from example.net")

        mock_file = MagicMock()
        mock_file.__enter__.return_value = iter(urls)
        mock_file.__exit__.return_value = None

        with patch('builtins.open', return_value=mock_file):
            await fetcher.fetch_urls_in_batches()

            for (key, _), expected_url in zip(m.requests.items(), urls):
                assert key[0] == 'GET'
                assert key[1] == URL(expected_url)


@pytest.mark.asyncio
async def test_fetch_with_multiple_workers():
    """ Test with multiple workers/concurrent requests """
    fetcher = Fetcher(concurrency=2, url_file="urls.txt")

    urls = ['http://example.com', 'http://example.org', 'http://example.net']

    with aioresponses() as m:
        m.get('http://example.com', status=200, body="Response from example.com")
        m.get('http://example.org', status=200, body="Response from example.org")
        m.get('http://example.net', status=200, body="Response from example.net")

        mock_file = MagicMock()
        mock_file.__enter__.return_value = iter(urls)
        mock_file.__exit__.return_value = None

        with patch('builtins.open', return_value=mock_file):
            await fetcher.fetch_urls_in_batches()

            for (key, _), expected_url in zip(m.requests.items(), urls):
                assert key[0] == 'GET'
                assert key[1] == URL(expected_url)


@pytest.mark.asyncio
async def test_fetch_urls_in_batches_with_error_handling():
    """ Test one of two URL with an error handling """
    fetcher = Fetcher(concurrency=2, url_file="urls.txt")

    urls = ['http://example.com', 'http://example.org']

    with aioresponses() as m:
        m.get('http://example.com', status=200, body="Response from example.com")
        m.get('http://example.org', exception=Exception("Something went wrong"))

        mock_file = MagicMock()
        mock_file.__enter__.return_value = iter(urls)
        mock_file.__exit__.return_value = None

        with patch('builtins.open', return_value=mock_file):
            with patch('builtins.print') as mock_print:
                await fetcher.fetch_urls_in_batches()
                assert mock_print.call_args_list == [
                    call('Got response: 200 from http://example.com'),
                    call('Error while fetching http://example.org: Something went wrong'),
                    call('Response from example.com'),
                    call('exception occurred')
                ]

            for (key, _), expected_url in zip(m.requests.items(), urls):
                assert key[0] == 'GET'
                assert key[1] == URL(expected_url)


@pytest.mark.asyncio
async def test_read_urls_in_batches():
    """ Test the batching logic """
    fetcher = Fetcher(concurrency=2, url_file="urls.txt")

    urls = ['http://example.com', 'http://example.org', 'http://example.net', 'http://example.edu']

    mock_file = MagicMock()
    mock_file.__enter__.return_value = iter(urls)
    mock_file.__exit__.return_value = None

    with patch('fetcher.URL_BATCH_SIZE', 2), patch('builtins.open', return_value=mock_file):
        batches = [batch async for batch in fetcher.read_urls_in_batches()]

    assert batches == [
        ['http://example.com', 'http://example.org'],
        ['http://example.net', 'http://example.edu']
    ]
