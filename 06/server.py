"""
This module implements a multithreaded TCP server that processes URLs received from clients.
Each URL is fetched and its top-k word frequencies are calculated, then sent back to the client.

Usage:
    python server.py <host> <num_workers> <port> <top_k>
"""

import socket
import threading
import json
from queue import Queue
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import requests


class Worker(threading.Thread):
    """
    Worker thread to fetch URLs, process word frequency, and send results back to clients.
    """
    def __init__(self, task_queue, result_lock, master_server, k):
        """
        Initializes the worker.

        :param task_queue: Queue with tasks containing client socket and URL
        :param result_lock: Lock to manage shared resource access for results
        :param master_server: Reference to the master server for shared stats
        :param k: Number of top words to return in frequency count
        """
        super().__init__()
        self.task_queue = task_queue
        self.result_lock = result_lock
        self.master_server = master_server
        self.k = k

    def fetch_url(self, url):
        """
        Fetches the content of the given URL.

        :param url: URL to be fetched
        :return: Text content of the URL, or None if an error occurs
        """
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def process_text(self, text):
        """
        Processes text to extract top-k frequent words.

        :param text: HTML text content of a webpage
        :return: Dictionary of top-k words and their frequencies
        """
        soup = BeautifulSoup(text, "html.parser")
        words = soup.get_text().lower().split()
        counter = Counter(words)
        return dict(counter.most_common(self.k))

    def run(self):
        """
        Processes tasks from the queue by fetching and analyzing URLs,
        then sends results to clients.
        """
        while True:
            client_socket, url = self.task_queue.get()
            if client_socket is None:
                break
            try:
                html_text = self.fetch_url(url)
                if html_text:
                    word_counts = self.process_text(html_text)
                    client_socket.sendall(json.dumps(word_counts).encode())
                    self.master_server.increment_processed_urls()
                else:
                    client_socket.sendall(b'not found')
            except Exception as e:
                print(f"Error occurred while processing {url=}: {e}")
                client_socket.sendall(b'error')
            finally:
                client_socket.close()
                self.task_queue.task_done()


class MasterServer:
    """
    Master server to handle incoming connections and distribute tasks to workers.
    """
    def __init__(self, host, port, worker_count, k):
        """
        Initializes the master server.

        :param host: Server hostname
        :param port: Server port
        :param worker_count: Number of worker threads to handle URL processing
        :param k: Number of top words to return in frequency count
        """
        self.host = host
        self.port = port
        self.k = k
        self.task_queue = Queue()
        self.result_lock = threading.Lock()
        self.total_processed_urls = 0
        self.workers = self._create_workers(worker_count)

    def _create_workers(self, worker_count):
        """
        Helper function to initialize worker threads.

        :param worker_count: Number of workers to initialize
        :return: List of initialized worker threads
        """
        return [
            Worker(self.task_queue, self.result_lock, self, self.k) for _ in range(worker_count)
        ]

    def start_workers(self):
        """
        Starts worker threads to handle URL processing.
        """
        for worker in self.workers:
            worker.start()

    def handle_client(self, client_socket):
        """
        Handles incoming client connections, adding each URL task to the queue.

        :param client_socket: Client socket for communication
        """
        url = client_socket.recv(1024).decode().strip()
        self.task_queue.put((client_socket, url))

    def run(self):
        """
        Runs the server, accepting connections and submitting tasks to the worker pool.
        """
        self.start_workers()
        with ThreadPoolExecutor(max_workers=len(self.workers)) as executor:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.bind((self.host, self.port))
                server_socket.listen()
                print(f"Server listening on {self.host}:{self.port}")
                while True:
                    client_socket, _ = server_socket.accept()
                    executor.submit(self.handle_client, client_socket)

    def stop_workers(self):
        """
        Stops all worker threads by sending termination signals through the task queue.
        """
        for _ in range(len(self.workers)):
            self.task_queue.put((None, None))
        for worker in self.workers:
            worker.join()

    def increment_processed_urls(self):
        """
        Thread-safe method to increment the count of processed URLs.
        """
        with self.result_lock:
            self.total_processed_urls += 1
            print(f"Processed URLs: {self.total_processed_urls}")


if __name__ == "__main__":
    import sys
    worker_count = int(sys.argv[2])
    top_k = int(sys.argv[4])
    server = MasterServer("localhost", 8080, worker_count, top_k)
    try:
        server.run()
    except KeyboardInterrupt:
        print("Shutting down server...")
        server.stop_workers()
