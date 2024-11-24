"""
This module contains tests for the FileReader class, which reads the content
of a file and processes it into a list of stripped strings.
"""

from unittest.mock import mock_open, patch
import pytest
from file_reader import FileReader


def test_file_reader_valid_file():
    """
    Test FileReader with a valid file containing multiple lines.
    Verifies that the data is correctly read and stripped.
    """
    mock_file_content = "line 1\nline 2\nline 3\n"
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        reader = FileReader("dummy_path")
        assert reader.data == ["line 1", "line 2", "line 3"]


def test_file_reader_empty_file():
    """
    Test FileReader with an empty file.
    Verifies that the resulting data is an empty list.
    """
    mock_file_content = ""
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        reader = FileReader("dummy_path")
        assert reader.data == []


def test_file_reader_file_with_spaces():
    """
    Test FileReader with a file containing lines with leading/trailing spaces
    and blank lines. Verifies that the lines are stripped, but empty lines are retained.
    """
    mock_file_content = "  line 1  \n line 2\n\n line 3  \n"
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        reader = FileReader("dummy_path")
        assert reader.data == ["line 1", "line 2", "", "line 3"]


def test_file_reader_file_not_found():
    """
    Test FileReader when the specified file does not exist.
    Verifies that a FileNotFoundError is raised.
    """
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            FileReader("non_existent_file.txt")


def test_file_reader_permission_error():
    """
    Test FileReader when the specified file cannot be accessed due to
    permission restrictions. Verifies that a PermissionError is raised.
    """
    with patch("builtins.open", side_effect=PermissionError):
        with pytest.raises(PermissionError):
            FileReader("protected_file.txt")
