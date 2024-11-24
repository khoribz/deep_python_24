"""
This module provides a class for reading a file and extracting its lines as a list of strings.

The FileReader class reads the contents of a file specified by the file path,
removes any leading/trailing whitespace from each line, and stores the lines as a list.
"""


class FileReader:
    """
    A class to read a file and store its lines in a list.

    The FileReader reads the file line by line, strips each line of leading and trailing
    whitespace, and stores the cleaned lines in a list.
    """

    def __init__(self, file_path: str):
        """
        Initializes the FileReader instance with the content of the specified file.

        :param file_path: The path to the file to be read.
        """
        self.data = self._read_file(file_path)

    def _read_file(self, file_path: str) -> list[str]:
        """
        Reads the file at the given path and returns its lines as a list of strings,
        with leading and trailing whitespace removed from each line.

        :param file_path: The path to the file to be read.
        :return: A list of lines from the file.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file.readlines()]
