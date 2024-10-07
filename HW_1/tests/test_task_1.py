"""
This module contains unit tests for the `predict_message_mood` function
from the `src.task_1` module. The tests mock the `SomeModel.predict`
method to provide controlled outputs for different scenarios.
"""

from unittest.mock import patch

import pytest

from HW_1.src.task_1 import predict_message_mood


@pytest.mark.parametrize(
    'message, bad_threshold, good_threshold, predict_value, expected_result',
    [
        (
            'Чапаев и пустота',
            None,
            None,
            0.9,
            'отл',
        ),
        (
            'Чапаев и пустота',
            0.8,
            0.99,
            0.85,
            'норм',
        ),
        (
            'Вулкан',
            None,
            None,
            0.1,
            'неуд',
        ),
    ]
)
def test_predict_message_mood(
    message, bad_threshold, good_threshold, predict_value, expected_result
):
    """
    Test the `predict_message_mood` function with mocked predictions.

    Args:
        message (str): The message to analyze.

        bad_threshold (float): The threshold below which the
        mood is considered bad.

        good_threshold (float): The threshold above which the
        mood is considered excellent.

        predict_value (float): The mocked value returned by
        `SomeModel.predict`.

        expected_result (str): The expected mood result based
        on the prediction and thresholds.
    """
    with patch('src.task_1.SomeModel.predict', return_value=predict_value):
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
