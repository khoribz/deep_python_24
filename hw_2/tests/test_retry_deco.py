"""
This module contains unit tests for testing the retry_deco decorator.

The tests cover:
- Successful function execution with retries.
- Function behavior when exceptions are raised and retries are triggered.
- Handling of expected and unexpected exceptions.
"""


from unittest.mock import patch

from hw_2.src.retry_deco import add, check_str, check_int


def test_add_success():
    """
    Test that the add function returns the correct sum and that retry_deco
    prints the correct output on success.
    """
    with patch('builtins.print') as mock_print:
        result = add(4, 2)
        assert result == 6
        mock_print.assert_called_once_with(
            'run "add" with positional args = (4, 2), attempt = 1, result = 6'
        )

    with patch('builtins.print') as mock_print:
        result = add(4, b=3)
        assert result == 7
        mock_print.assert_called_once_with(
            'run "add" with positional args = (4,), keyword kwargs = {\'b\': 3}, '
            'attempt = 1, result = 7'
        )


def test_check_str_success():
    """
    Test that check_str returns True when a valid string is provided
    and that retry_deco prints the correct output on success.
    """
    with patch('builtins.print') as mock_print:
        result = check_str(value="123")
        assert result is True
        mock_print.assert_called_once_with(
            'run "check_str" with keyword kwargs = {\'value\': \'123\'}, '
            'attempt = 1, result = True'
        )


def test_check_str_failure():
    """
    Test that check_str returns False when the input is not a string
    and that retry_deco prints the correct output.
    """
    with patch('builtins.print') as mock_print:
        result = check_str(value=1)
        assert result is False
        mock_print.assert_called_once_with(
            'run "check_str" with keyword kwargs = {\'value\': 1}, '
            'attempt = 1, result = False'
        )


def test_check_str_exception():
    """
    Test that check_str raises a ValueError when the value is None,
    and that retry_deco retries the function 3 times, printing the correct output.
    """
    with patch('builtins.print') as mock_print:
        check_str(value=None)
        assert mock_print.call_count == 3
        mock_print.assert_any_call(
            'run "check_str" with keyword kwargs = {\'value\': None}, '
            'attempt = 1, exception = ValueError'
        )
        mock_print.assert_any_call(
            'run "check_str" with keyword kwargs = {\'value\': None}, '
            'attempt = 2, exception = ValueError'
        )
        mock_print.assert_any_call(
            'run "check_str" with keyword kwargs = {\'value\': None}, '
            'attempt = 3, exception = ValueError'
        )


def test_check_int_success():
    """
    Test that check_int returns True when a valid integer is provided
    and that retry_deco prints the correct output on success.
    """
    with patch('builtins.print') as mock_print:
        result = check_int(value=1)
        assert result is True
        mock_print.assert_called_once_with(
            'run "check_int" with keyword kwargs = {\'value\': 1}, '
            'attempt = 1, result = True'
        )


def test_check_int_expected_exception():
    """
    Test that check_int raises a ValueError and stops retrying after the first attempt,
    printing the correct output when an expected exception occurs.
    """
    with patch('builtins.print') as mock_print:
        check_int(value=None)
        mock_print.assert_called_once_with(
            'run "check_int" with keyword kwargs = {\'value\': None}, '
            'attempt = 1, exception = ValueError'
        )
