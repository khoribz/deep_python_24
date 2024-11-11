"""
This module defines a TCP client that sends a list of URLs to a server and receives
word frequency statistics for each URL. The client reads URLs from a file, sends each
URL in a separate thread to the server, and prints the server's response.

Usage:
    python client.py <num_threads> <url_file>
"""

import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed


class Client:
    """
    TCP client to send a list of URLs to the server and receive word frequency statistics.
    Loads URLs from a file and initiates multiple threads for parallel processing.
    """

    def __init__(self, url_filename, num_threads, host="localhost", port=8080):
        """
        Initializes the client.

        :param url_filename: Name of the file containing URLs for processing
        :param num_threads: Number of threads for parallel processing
        :param host: Server host (default is localhost)
        :param port: Server port (default is 8080)
        """
        self.host = host
        self.port = port
        self.urls = self.load_urls(url_filename)
        self.num_threads = num_threads

    def load_urls(self, filename):
        """
        Loads URLs from a file.

        :param filename: The filename containing URLs
        :return: List of URLs
        """
        with open(filename, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file.readlines()]

    def fetch_url(self, url):
        """
        Establishes a TCP connection to the server, sends a URL, and receives the response.

        :param url: URL to be processed
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((self.host, self.port))
                sock.sendall(url.encode())
                response = sock.recv(1024)
                print(f"{url}: {response.decode()}")
            except Exception as e:
                print(f"Error processing {url}: {e}")

    def run(self):
        """
        Initiates a ThreadPoolExecutor to manage concurrent URL requests.
        Submits each URL request as a separate task and waits for all to complete.
        """
        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            futures = [executor.submit(self.fetch_url, url) for url in self.urls]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error: {e}")


if __name__ == "__main__":
    num_threads = int(sys.argv[1])
    url_file = sys.argv[2]
    client = Client(url_filename=url_file, num_threads=num_threads)
    client.run()
