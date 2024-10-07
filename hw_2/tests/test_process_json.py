"""
This module tests the functionality of the process_json function using various
test cases and mock callbacks to ensure expected behavior.
"""

from orjson import dumps
from hw_2.src.process_json import process_json
from hw_2.tests.helpers import parametrize_with_dict


class Mocks:  # pylint: disable=too-few-public-methods
    """
    A mock class to capture the arguments passed to the callback function.
    It stores the arguments in `called_args` for later verification.
    """

    def __init__(self):
        self.called_args = []

    def callback(self, key: str, value: str) -> None:
        """
        A callback function that captures key-value pairs and stores them
        in the called_args list.

        Args:
            key (str): The key from the JSON data.
            value (str): The value from the JSON data.
        """
        self.called_args.append((key, value))


@parametrize_with_dict(
    ['json_data', 'required_keys', 'tokens', 'callback_expected_called_args'],
    [
        {
            'test_name': 'There is a match between key and token, callback will be called',
            'json_data': dumps({'key': 'some value'}).decode('utf-8'),
            'required_keys': ['key'],
            'tokens': ['value'],
            'callback_expected_called_args': [('key', 'value')]
        },
        {
            'test_name': 'There are several matches between keys and tokens, '
                         'callbacks will be called',
            'json_data': dumps(
                {'key1': 'some value', 'key2': 'other extra mega new car', 'key3': 'oops'}
            ).decode('utf-8'),
            'required_keys': ['key1', 'key2'],
            'tokens': ['value', 'new', 'oops'],
            'callback_expected_called_args': [('key1', 'value'), ('key2', 'new')]
        },
        {
            'test_name': 'No key matches',
            'json_data': dumps({'key': 'some value'}).decode('utf-8'),
            'required_keys': ['unknown_key'],
            'tokens': ['value'],
            'callback_expected_called_args': [],
        },
        {
            'test_name': 'No token matches',
            'json_data': dumps({'key': 'some value'}).decode('utf-8'),
            'required_keys': ['key'],
            'tokens': ['strange_value'],
            'callback_expected_called_args': [],
        },
    ]
)
def test_process_json(json_data, required_keys, tokens, callback_expected_called_args):
    """
    Test the process_json function with different sets of JSON data, required keys,
    and tokens, and verify that the callback is called with the correct arguments.
    """
    mocks = Mocks()
    process_json(
        json_data,
        required_keys=required_keys,
        tokens=tokens,
        callback=mocks.callback,
    )
    assert mocks.called_args == callback_expected_called_args


def test_process_json_callback_none():
    """
    Test the process_json function when the callback is set to None.
    The callback should not be called, and no arguments should be stored.
    """
    mocks = Mocks()
    mocks.callback = None
    process_json(
        dumps({'key': 'some value'}).decode('utf-8'),
        required_keys=[],
        tokens=[],
        callback=mocks.callback,
    )
    assert not mocks.called_args  # Simplified comparison
