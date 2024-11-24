"""
This module provides functionality to fetch data asynchronously from a list of URLs.

The Fetcher class is designed to handle multiple concurrent HTTP requests with a semaphore to limit
the number of simultaneous requests. It uses aiohttp for making asynchronous HTTP requests.

Usage:
    The script accepts two command-line arguments:
    - '-c' or '--concurrency' specifies the number of concurrent requests.
    - A file containing the list of URLs to fetch.

Example:
    python fetcher.py -c 10 urls.txt
"""

import asyncio
import argparse
import aiohttp
from aiohttp import ClientSession
from file_reader import FileReader

# Constants
REQUEST_TIMEOUT = 1


class Fetcher:
    """
    A class for asynchronously fetching data from multiple URLs with
    concurrency control for simultaneous requests.
    """
    def __init__(self, concurrency: int, urls: list):
        """
        Initializes the Fetcher with the specified concurrency level
        and list of URLs.

        :param concurrency: The number of simultaneous requests to allow.
        :param urls: The list of URLs to fetch data from.
        """
        self.concurrency = concurrency
        self.urls = urls
        self.semaphore = asyncio.Semaphore(concurrency)

    async def fetch(self, session: ClientSession, url: str) -> aiohttp.ClientResponse:
        """
        Asynchronously fetches data from a single URL with a semaphore
        limiting the number of concurrent requests.

        :param session: The HTTP session used for making requests.
        :param url: The URL to fetch data from.
        :return: The response object from the HTTP request.
        """
        async with self.semaphore:
            try:
                async with session.get(url, timeout=REQUEST_TIMEOUT) as response:
                    print(f'Got response: {response.status}')
                    return response
            except asyncio.TimeoutError:
                print('Timeout error occurred.')
                raise
            except Exception as e:
                print(f"Error while fetching {url}: {e}")
                raise

    async def fetch_all(self) -> list[aiohttp.ClientResponse]:
        """
        Asynchronously fetches data from all URLs in the list with
        a limit on the number of concurrent requests.

        :return: A list of responses from the HTTP requests.
        """
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(session, url) for url in self.urls]
            return await asyncio.gather(*tasks)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Asynchronous URL Fetcher")
    parser.add_argument('-c', '--concurrency', type=int, help="Number of concurrent requests", required=True)
    parser.add_argument('url_file', type=str, help="File containing the list of URLs")
    args = parser.parse_args()

    urls = FileReader(args.url_file).data
    fetcher = Fetcher(concurrency=args.concurrency, urls=urls)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetcher.fetch_all())
