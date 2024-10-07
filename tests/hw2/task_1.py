from orjson import dumps

from src.hw2.task_1 import process_json
from tests.helpers import parametrize_with_dict


class Mocks:
    def __init__(self):
        self.called_args = []

    def callback(self, key: str, value: str) -> None:
        self.called_args.append((key, value))


@parametrize_with_dict(
    ['json_data', 'required_keys', 'tokens', 'callback_expected_called_args'],
    [
        {
            'test_name': 'There are match key with token, callback will be called',
            'json_data': dumps({'key': 'some value'}).decode('utf-8'),
            'required_keys': ['key'],
            'tokens': ['value'],
            'callback_expected_called_args': [('key', 'value')]
        },
        {
            'test_name': 'There are several matches of key with token, callbacks will be called',
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
    mocks = Mocks()
    process_json(
        json_data,
        required_keys=required_keys,
        tokens=tokens,
        callback=mocks.callback,
    )
    assert mocks.called_args == callback_expected_called_args


def test_process_json_callback_none():
    mocks = Mocks()
    mocks.callback = None
    process_json(
        dumps({'key': 'some value'}).decode('utf-8'),
        required_keys=[],
        tokens=[],
        callback=mocks.callback,
    )
    assert mocks.called_args == []
