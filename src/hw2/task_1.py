"""
This module provides functionality for processing JSON strings
by looking for required keys and tokens within their values.
A callback function can be triggered when matching tokens are found.
"""
from typing import Callable

import orjson


def process_json(
    json_str: str,
    required_keys: list[str] | None = None,
    tokens: list[str] | None = None,
    callback: Callable[[str, str], None] | None = None,
) -> None:
    """
        Processes a JSON string by looking for required keys and tokens
        in their corresponding values. If a token is found, a callback
        is invoked with the matching key and token.

        Args:
            json_str (str): The JSON string to process.
            required_keys (list[str] | None): A list of required keys to look for.
            tokens (list[str] | None): A list of tokens to search for in the values.
            callback (Callable[[str, str], None] | None): A callback function to be
            called when a token is found.
    """
    data = orjson.loads(json_str) # pylint: disable=maybe-no-member
    required_keys = required_keys or []
    tokens = tokens or []
    if callback is None:
        return None

    for key, value in data.items():
        if key in required_keys:
            for token in tokens:
                if token.lower() in value.lower():
                    callback(key, token)
