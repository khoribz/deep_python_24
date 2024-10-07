
from unittest.mock import patch

from src.hw2.task_2 import retry_deco


@retry_deco(3)
def add(a, b):
    return a + b


def test_add_success():
    with patch('builtins.print') as mock_print:
        result = add(4, 2)
        assert result == 6
        mock_print.assert_called_once_with('run "add" with positional args = (4, 2), attempt = 1, result = 6')

    with patch('builtins.print') as mock_print:
        result = add(4, b=3)
        assert result == 7
        mock_print.assert_called_once_with(
            'run "add" with positional args = (4,), keyword kwargs = {\'b\': 3}, attempt = 1, result = 7'
        )


@retry_deco(3)
def check_str(value=None):
    if value is None:
        raise ValueError()
    return isinstance(value, str)


def test_check_str_success():
    with patch('builtins.print') as mock_print:
        result = check_str(value="123")
        assert result is True
        mock_print.assert_called_once_with(
            'run "check_str" with keyword kwargs = {\'value\': \'123\'}, attempt = 1, result = True'
        )


def test_check_str_failure():
    with patch('builtins.print') as mock_print:
        result = check_str(value=1)
        assert result is False
        mock_print.assert_called_once_with(
            'run "check_str" with keyword kwargs = {\'value\': 1}, attempt = 1, result = False'
        )


def test_check_str_exception():
    with patch('builtins.print') as mock_print:
        check_str(value=None)
        assert mock_print.call_count == 3
        mock_print.assert_any_call(
            'run "check_str" with keyword kwargs = {\'value\': None}, attempt = 1, exception = ValueError'
        )
        mock_print.assert_any_call(
            'run "check_str" with keyword kwargs = {\'value\': None}, attempt = 2, exception = ValueError'
        )
        mock_print.assert_any_call(
            'run "check_str" with keyword kwargs = {\'value\': None}, attempt = 3, exception = ValueError'
        )


@retry_deco(2, [ValueError])
def check_int(value=None):
    if value is None:
        raise ValueError()
    return isinstance(value, int)


def test_check_int_success():
    with patch('builtins.print') as mock_print:
        result = check_int(value=1)
        assert result is True
        mock_print.assert_called_once_with(
            'run "check_int" with keyword kwargs = {\'value\': 1}, attempt = 1, result = True'
        )


def test_check_int_expected_exception():
    with patch('builtins.print') as mock_print:
        check_int(value=None)
        mock_print.assert_called_once_with(
            'run "check_int" with keyword kwargs = {\'value\': None}, attempt = 1, exception = ValueError'
        )
