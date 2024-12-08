"""
    This module tests client.py
"""


from unittest.mock import patch, MagicMock

import pytest
from client import Client
from testdata import URLS


@pytest.fixture
def url_file(tmp_path):
    """
        Fixture to create a temporary file containing test URLs.
        The file is automatically cleaned up after the test.

        :param tmp_path: pytest fixture to provide a temporary directory.
        :return: Path to the temporary file with URLs.
    """
    file = tmp_path / "test-urls.txt"
    file.write_text(URLS.strip())
    return file


def test_stream_urls(url_file):
    """
    Test the stream_urls method.
    """
    client = Client(url_filename=url_file, num_threads=2)
    expected_urls = URLS.strip().split('\n')

    streamed_urls = list(client.stream_urls())
    assert streamed_urls == expected_urls


@patch("socket.socket")
def test_fetch_url(mock_socket):
    """
        Test the fetch_url method to ensure it correctly connects to the server,
        sends a URL, and receives a response.

        :param mock_socket: Mocked socket object to simulate server interaction.
    """
    mock_conn = MagicMock()
    mock_conn.recv.return_value = b"Success"
    mock_socket.return_value.__enter__.return_value = mock_conn

    url = 'http://example.com'
    client = Client(url_filename='06/urls.txt', num_threads=1)
    client.fetch_url(url)

    mock_conn.connect.assert_called_once_with((client.host, client.port))
    mock_conn.sendall.assert_called_once_with(url.encode())
    mock_conn.recv.assert_called_once_with(1024)
    mock_conn.recv.assert_called_once()


@patch("socket.socket")
def test_fetch_url_with_error(mock_socket):
    """
        Test the fetch_url method to ensure proper handling of exceptions
        when a connection error occurs.

        :param mock_socket: Mocked socket object to simulate a connection error.
    """
    mock_socket_instance = mock_socket.return_value.__enter__.return_value
    mock_socket_instance.connect.side_effect = ConnectionError("Connection failed")

    url = 'http://example.com'
    client = Client(url_filename='06/urls.txt', num_threads=1)

    with patch('builtins.print') as mock_print:
        client.fetch_url(url)
        mock_print.assert_called_with(f"Error processing {url}: Connection failed")


@patch("client.Client.fetch_url")
def test_run(mock_fetch_url, url_file):
    """
        Test the run method to ensure all URLs are processed by fetch_url in parallel.

        :param mock_fetch_url: Mocked fetch_url method to track calls.
        :param url_file: Temporary file containing test URLs.
    """

    mock_fetch_url.return_value = None

    client = Client(url_filename=str(url_file), num_threads=2)
    client.run()
    urls = URLS.strip().split('\n')

    assert mock_fetch_url.call_count == len(urls)
    for url in urls:
        mock_fetch_url.assert_any_call(url)


@patch("client.Client.fetch_url")
def test_run_with_error(mock_fetch_url, url_file):
    """
    Test the run method to ensure errors in fetch_url are handled properly.

    :param mock_fetch_url: Mocked fetch_url method to simulate an exception.
    :param url_file: Temporary file containing test URLs.
    """
    mock_fetch_url.side_effect = Exception("Test error")

    client = Client(url_filename=str(url_file), num_threads=2)

    with patch("builtins.print") as mock_print:
        client.run()

        urls = URLS.strip().split("\n")
        assert mock_fetch_url.call_count == len(urls)

        for _ in urls:
            mock_print.assert_any_call("Error: Test error")
