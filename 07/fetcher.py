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

# Constants
REQUEST_TIMEOUT = 1
URL_BATCH_SIZE = 100


class Fetcher:
    """
    A class for asynchronously fetching data from multiple URLs with
    concurrency control for simultaneous requests.
    """
    def __init__(self, concurrency: int, url_file: str):
        """
        Initializes the Fetcher with the specified concurrency level
        and file path to URLs.

        :param concurrency: The number of simultaneous requests to allow.
        :param url_file: The file containing the list of URLs to fetch data from.
        """
        self.concurrency = concurrency
        self.url_file = url_file
        self.semaphore = asyncio.Semaphore(concurrency)

    async def fetch(self, session: ClientSession, url: str) -> str:
        """
        Asynchronously fetches data from a single URL with a semaphore
        limiting the number of concurrent requests.

        :param session: The HTTP session used for making requests.
        :param url: The URL to fetch data from.
        :return: The response text from the HTTP request.
        """
        async with self.semaphore:
            try:
                async with session.get(url, timeout=REQUEST_TIMEOUT) as response:
                    print(f'Got response: {response.status} from {url}')
                    text = await response.text()
                    return text
            except asyncio.TimeoutError:
                print(f'Timeout error occurred for {url}.')
                raise
            except Exception as e:
                print(f"Error while fetching {url}: {e}")
                raise

    async def fetch_urls_in_batches(self):
        """
        Reads the URL file lazily, processes it in batches, and fetches data.
        """
        async with aiohttp.ClientSession() as session:
            async for batch in self.read_urls_in_batches():
                tasks = [self.fetch(session, url) for url in batch]
                responses = await asyncio.gather(*tasks, return_exceptions=True)
                for response in responses:
                    if isinstance(response, Exception):
                        print('exception occurred')
                    else:
                        print(response)

    async def read_urls_in_batches(self):
        """
        Lazy URL reading in batches, yielding a batch of URLs at a time.
        """
        batch = []
        with open(self.url_file, 'r', encoding='utf-8') as file:
            for line in file:
                url = line.strip()
                if url:
                    batch.append(url)
                if len(batch) == URL_BATCH_SIZE:
                    yield batch
                    batch = []
            if batch:
                yield batch


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Asynchronous URL Fetcher")
    parser.add_argument('-c', '--concurrency', type=int, help="Number of concurrent requests", required=True)
    parser.add_argument('url_file', type=str, help="File containing the list of URLs")
    args = parser.parse_args()

    fetcher = Fetcher(concurrency=args.concurrency, url_file=args.url_file)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetcher.fetch_urls_in_batches())
