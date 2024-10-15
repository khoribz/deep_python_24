"""
This module contains tests for the filter_file function.
It checks different cases with file-like objects and real file paths,
and validates whether the filtering of lines based on search
and stop words works as expected.
"""

import io
import pytest
from file_generator import filter_file


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
            './01/predict_message_text.txt',
            None,
            ['роза', 'упала'],
            ['азора', 'медведь'],
            [
                'Роза цвела в саду',
            ]
        ),
        (
            './01/predict_message_text.txt',
            None,
            ['роза', 'темном', 'цвела', 'заяц'],
            ['азора', 'медведь'],
            [
                'Роза цвела в саду',
                'Бежит по лесу заяц'
            ]
        ),
        (
            None,
            io.StringIO(
                """
                роза
                медведь
                зайц
                лапа
                """
            ),
            ['роза'],
            ['медведь'],
            [
                'роза',
            ]
        ),
        (
            None,
            io.StringIO(
                """
                В темном лесу медведь собирал ягоды
                Роза цвела в саду
                """
            ),
            ['роза'],
            [],
            [
                'Роза цвела в саду',
            ]
        ),
        (
            None,
            io.StringIO(
                """
                В темном лесу медведь собирал ягоды
                Роза упала на лапу Азора
                """
            ),
            [],
            ['медведь'],
            []
        ),
        (
            None,
            io.StringIO(
                """
                В темном лесу медведь собирал ягоды
                Роза упала на лапу Азора
                """
            ),
            ['роза', 'медведь'],
            ['роза'],
            ['В темном лесу медведь собирал ягоды']
        ),
        (
            None,
            io.StringIO(
                """
                Роза упала на лапу Азора
                роза цветет
                """
            ),
            ['роза'],
            ['азора'],
            [
                'роза цветет',
            ]
        ),
        (
            None,
            io.StringIO(
                """

                Роза упала на лапу Азора
                """
            ),
            ['роза'],
            ['азора'],
            []
        ),
        (
            None,
            io.StringIO(
                """
                Розетка упала на стол
                Медведь сидел в розарии
                """
            ),
            ['роза'],
            ['медведь'],
            []
        ),
        (
            None,
            io.StringIO(
                """
                Роза и медведь сидели на поляне
                """
            ),
            ['роза', 'поляна'],
            ['медведь'],
            []
        ),
        (
            None,
            io.StringIO(
                """
                Роза и заяц сидели на поляне
                """
            ),
            ['роза', 'поляна'],
            [],
            [
                'Роза и заяц сидели на поляне',
            ]
        ),
    ]
)
def test_filter_file(
    file_name, file_object, search_words, stop_words, expected_result
):
    """
        Test the filter_file function with different input
        sources (file_name or file_object),
        ensuring it returns the correct lines based on search and stop words.
    """
    result = list(
        filter_file(file_name, file_object, search_words, stop_words)
    )
    assert result == expected_result


def test_filter_file_with_incorrect_file_data():
    """
        Test the filter_file function with incorrect input, ensuring
        it raises a ValueError when both file_name and file_object are None.
    """
    with pytest.raises(ValueError):
        list(
            filter_file(None, None, [], [])
        )
