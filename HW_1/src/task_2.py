"""
This module provides functionality for filtering lines
from a file based on search words and stop words.
"""

from typing import Generator, TextIO


def _process_lines(
    file: TextIO,
    search_words: set[str],
    stop_words: set[str]
) -> Generator[str, None, None]:
    """
    Обрабатывает строки из файла.

    Args:
        file: Файловый объект для чтения.
        search_words (set[str]): Набор слов для поиска.
        stop_words (set[str]): Набор стоп-слов.

    Yields:
        Строки, которые содержат хотя бы одно слово
        для поиска и не содержат стоп-слов.
    """
    for line in file:
        words = set(line.strip().lower().split())
        if words & stop_words:
            continue
        if words & search_words:
            yield line.strip()


def filter_file(
    file_name: str | None,
    file_object: TextIO | None,
    search_words: list[str],
    stop_words: list[str]
) -> Generator[str, None, None]:
    """
        Filters lines from a file or file-like object
        based on search and stop words.

        Args:
            file_name (str | None): The path to the file to read,
            or None if a file object is provided.

            file_object (io.StringIO | None): A file-like object to read
            from, or None if a file path is provided.

            search_words (list[str]): Words to search for in the file.

            stop_words (list[str]): Words that, if present, cause the
            line to be skipped.

        Returns:
            Generator[str, None, None]: A generator yielding lines
            that match the search criteria.
    """

    search_words = set(word.lower() for word in search_words)
    stop_words = set(word.lower() for word in stop_words)

    if file_name is not None:
        with open(file_name, 'r', encoding='utf-8') as file:
            yield from _process_lines(file, search_words, stop_words)
    elif file_object is not None:
        yield from _process_lines(file_object, search_words, stop_words)
    else:
        raise ValueError("Either file_name or file_object must be specified.")
