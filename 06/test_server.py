"""
This module tests server.py
"""

import json
import threading
import socket
from unittest.mock import patch, MagicMock
from threading import Lock
from queue import Queue
from server import Worker, MasterServer
import pytest


@pytest.fixture
def task_queue():
    """
    Fixture that creates a task queue for the worker threads.
    """
    return Queue()


@pytest.fixture
def result_lock():
    """
    Fixture that creates a lock for synchronizing access to shared resources.
    """
    return Lock()


@pytest.fixture
def mock_master_server():
    """
    Fixture that creates a mock master server with a processed URL counter.
    """
    class MockMasterServer:
        """
            Mocked master server for testing.
        """
        def __init__(self):
            self.processed_urls = 0

        def increment_processed_urls(self):
            """
                Increment the number of processed URLs
            """
            self.processed_urls += 1

    return MockMasterServer()


def test_fetch_url_success(task_queue, result_lock, mock_master_server):
    """
    Test that the fetch_url function successfully retrieves content.
    """
    worker = Worker(task_queue, result_lock, mock_master_server, k=3)
    response_text = "<html><body>Test content</body></html>"
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = response_text
        response = worker.fetch_url("http://example.com")
        assert response == response_text


def test_fetch_url_error(task_queue, result_lock, mock_master_server):
    """
    Test that the fetch_url function raises an error on connection failure.
    """
    worker = Worker(task_queue, result_lock, mock_master_server, k=3)
    with patch("requests.get", side_effect=ConnectionError()):
        with pytest.raises(ConnectionError):
            response = worker.fetch_url("http://example.com")
            assert response is None


def test_process_text(task_queue, result_lock, mock_master_server):
    """
    Test that the process_text function correctly counts word frequencies.
    """
    worker = Worker(task_queue, result_lock, mock_master_server, k=3)
    html_text = "<html><body>word1 word2 word2 word3 word3 word3</body></html>"
    result = worker.process_text(html_text)
    assert result == {"word3": 3, "word2": 2, "word1": 1}


def test_process_text_with_nullable_k(task_queue, result_lock, mock_master_server):
    """
    Test that the process_text function returns an empty dictionary when k is 0.
    """
    worker = Worker(task_queue, result_lock, mock_master_server, k=0)
    html_text = "<html><body>word1 word2 word2 word3 word3 word3</body></html>"
    result = worker.process_text(html_text)
    assert not result  # Simplified check, as an empty dict is falsy


def test_create_workers():
    """
    Test that the MasterServer creates the correct number of worker threads.
    """
    server = MasterServer("localhost", 8080, 3, 5)
    assert len(server.workers) == 3
    for worker in server.workers:
        assert isinstance(worker, threading.Thread)


def test_handle_client():
    """
    Test that the MasterServer correctly handles incoming client connections and adds tasks to the queue.
    """
    server = MasterServer("localhost", 8080, 3, 5)
    mock_socket = MagicMock()
    mock_socket.recv.return_value = b"http://example.com"
    server.handle_client(mock_socket)
    task = server.task_queue.get()
    assert task == (mock_socket, "http://example.com")


@pytest.fixture
def server():
    """
    Fixture that creates a MasterServer instance and starts it in a separate thread.
    """
    server = MasterServer("localhost", 8080, 2, 3)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    yield server
    server.stop_workers()


def test_server_interaction(server):
    """
    Test that the server correctly interacts with a client and sends back word frequency data.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(("localhost", 8080))
        client_socket.sendall(b"http://example.com")
        response = client_socket.recv(1024)
        assert isinstance(response, bytes)
        data = json.loads(response.decode())
        assert isinstance(data, dict)
