"""
This module contains unit tests for the `predict_message_mood` function
from the `src.task_1` module. The tests mock the `SomeModel.predict`
method to provide controlled outputs for different scenarios.
"""
from unittest.mock import patch

import pytest

from predict_message import predict_message_mood, SomeModel


@pytest.mark.parametrize(
    'input_message, mocked_score, bad_threshold, good_threshold, expected_result',
    [
        # Тесты для точного совпадения с порогами
        ("Exactly bad threshold", 0.3, 0.3, 0.8, 'норм'),  # На границе bad_threshold
        ("Exactly good threshold", 0.8, 0.3, 0.8, 'норм'),  # На границе good_threshold

        # Тесты немного ниже порогов
        ("Just below bad threshold", 0.29, 0.3, 0.8, 'неуд'),  # Немного ниже bad_threshold
        ("Just below good threshold", 0.79, 0.3, 0.8, 'норм'),  # Немного ниже good_threshold

        # Тесты немного выше порогов
        ("Just above bad threshold", 0.31, 0.3, 0.8, 'норм'),  # Немного выше bad_threshold
        ("Just above good threshold", 0.81, 0.3, 0.8, 'отл'),  # Немного выше good_threshold

        # Тесты значительно ниже/выше порогов
        ("Far below bad threshold", 0.1, 0.3, 0.8, 'неуд'),  # Сильно ниже bad_threshold
        ("Far above good threshold", 0.9, 0.3, 0.8, 'отл'),  # Сильно выше good_threshold

        # Тесты с модифицированными порогами
        ("Custom thresholds - below bad", 0.25, 0.4, 0.85, 'неуд'),  # Ниже custom bad_threshold
        ("Custom thresholds - above good", 0.9, 0.4, 0.85, 'отл'),  # Выше custom good_threshold
        ("Custom thresholds - between", 0.5, 0.4, 0.85, 'норм'),  # Между custom thresholds

        # На границе с модифицированными порогами
        ("Custom thresholds - at bad", 0.4, 0.4, 0.85, 'норм'),  # На custom bad_threshold
        ("Custom thresholds - at good", 0.85, 0.4, 0.85, 'норм'),  # На custom good_threshold
    ]
)
def test_predict_message_mood_with_edge_cases(
    input_message, mocked_score, bad_threshold, good_threshold, expected_result
):
    """
    Test `predict_message_mood` for edge cases and threshold boundaries.

    Args:
        input_message (str): The message to analyze.
        mocked_score (float): The mocked score to return from the model.
        bad_threshold (float): The threshold below which the mood is considered bad.
        good_threshold (float): The threshold above which the mood is considered excellent.
        expected_result (str): The expected mood result based on the mocked score.
    """
    with patch.object(SomeModel, 'predict', return_value=mocked_score) as mock_predict:
        result = predict_message_mood(
            message=input_message,
            bad_threshold=bad_threshold,
            good_threshold=good_threshold,
        )
        assert result == expected_result
        mock_predict.assert_called_once_with(input_message)


@pytest.mark.parametrize(
    'message, expected_score',
    [
        ("12345", 0.0),  # Только цифры, нет букв
        ("abc", 1.0),  # Только буквы, доля = 1
        ("abc123", 0.5),  # Половина символов - буквы
        ("a b c", 0.6),  # 3 буквы из 5 символов
        ("a!b@c#123", 1 / 3),  # 3 буквы из 10 символов
        ("a" * 100, 1.0),  # Большая строка из букв, доля = 1
        (" ", 0.0),  # Только пробелы, результат должен быть 0
        ("MixedCASE123", 0.75),  # Разные регистры букв
    ]
)
def test_some_model_predict(message, expected_score):
    """
    Test `SomeModel.predict` for various inputs.

    Args:
        message (str): The input message to analyze.
        expected_score (float): The expected normalized score.
    """
    model = SomeModel()
    assert model.predict(message) == expected_score
