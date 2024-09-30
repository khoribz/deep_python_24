"""
This module contains tests for the filter_file function.
It checks different cases with file-like objects and real file paths,
and validates whether the filtering of lines based on search and stop words works as expected.
"""

import io
import pytest
from src.task_2 import filter_file


@pytest.mark.parametrize(
    'file_name, file_object, search_words, stop_words, expected_result',
    [
        (
            None,
            io.StringIO(
                """
                Роза упала на лапу Азора
                В темном лесу медведь собирал ягоды
                Роза цвела в саду
                Бежит по лесу заяц
                """
            ),
            ['роза', 'упала'],
            ['азора', 'медведь'],
            [
                'Роза цвела в саду',
            ]
        ),
        (
            None,
            io.StringIO(
                """
                Роза упала на лапу Азора
                В темном лесу медведь собирал ягоды
                Роза цвела в саду
                Бежит по лесу заяц
                """
            ),
            ['роза', 'темном', 'цвела', 'заяц'],
            ['азора', 'медведь'],
            [
                'Роза цвела в саду',
                'Бежит по лесу заяц'
            ]
        ),
        (
            './tests/texts/task2_text.txt',
            None,
            ['роза', 'упала'],
            ['азора', 'медведь'],
            [
                'Роза цвела в саду',
            ]
        ),
        (
            './tests/texts/task2_text.txt',
            None,
            ['роза', 'темном', 'цвела', 'заяц'],
            ['азора', 'медведь'],
            [
                'Роза цвела в саду',
                'Бежит по лесу заяц'
            ]
        )
    ]
)
def test_filter_file(
    file_name, file_object, search_words, stop_words, expected_result
):
    """
        Test the filter_file function with different input sources (file_name or file_object),
        ensuring it returns the correct lines based on search and stop words.
    """
    result = list(
        filter_file(file_name, file_object, search_words, stop_words)
    )
    assert result == expected_result


def test_filter_file_with_incorrect_file_data():
    """
        Test the filter_file function with incorrect input, ensuring it raises a ValueError
        when both file_name and file_object are None.
    """
    with pytest.raises(ValueError):
        list(
            filter_file(None, None, [], [])
        )
