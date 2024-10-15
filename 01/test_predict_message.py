"""
This module contains unit tests for the `predict_message_mood` function
from the `src.task_1` module. The tests mock the `SomeModel.predict`
method to provide controlled outputs for different scenarios.
"""

import pytest
import sys
sys.path.append('.')

from predict_message import predict_message_mood


@pytest.mark.parametrize(
    'message, bad_threshold, good_threshold, expected_result',
    [
        (
            'Здесь будет отл1',
            None,
            None,
            'отл',
        ),
        (
            'Тест норм1',  # check upper exact border 0.8
            None,
            None,
            'норм',
        ),
        (
            'фиф3030302',  # check lower exact border 0.3
            None,
            None,
            'норм',
        ),
        (
            'Отлично должно тут быть, доля чисел чуть больше верхнего порога 1',
            0.3,
            0.81,
            'отл',
        ),
        (
            'Нормально должно тут быть, доля чисел чуть больше верхнего порога 1',
            0.3,
            0.83,
            'норм',
        ),
        (
            'Чапаев и пустота399393204893939333322211',  # a bit more than lower border
            0.35,
            0.99,
            'норм',
        ),
        (
            'Чапаев и пустота39939320489393933332221132',  # a bit less than lower border
            0.35,
            0.99,
            'неуд',
        ),
        (
            'Ву39929001202020202020911991919191',
            None,
            None,
            'неуд',
        ),
    ]
)
def test_predict_message_mood(
    message, bad_threshold, good_threshold, expected_result
):
    """
    Test the `predict_message_mood` function with mocked predictions.

    Args:
        message (str): The message to analyze.

        bad_threshold (float): The threshold below which the
        mood is considered bad.

        good_threshold (float): The threshold above which the
        mood is considered excellent.

        expected_result (str): The expected mood result based
        on the prediction and thresholds.
    """
    assert predict_message_mood(
        message=message,
        **(
            {} if bad_threshold is None else
            {'bad_threshold': bad_threshold}
        ),
        **(
            {} if good_threshold is None else
            {'good_threshold': good_threshold}
        )
    ) == expected_result
