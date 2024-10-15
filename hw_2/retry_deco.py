"""
This module provides a decorator `retry_deco` that allows a function to
be retried a specified number of times in the event of an exception.

The decorator takes two arguments:
1. `max_attempts`: The maximum number of attempts before giving up.
2. `expected_exceptions`: A list of exceptions that will stop the retry attempts if encountered.

If an exception is not in `expected_exceptions`, the function will retry until
the maximum number of attempts is reached.
"""

import functools
from typing import Type


def retry_deco(
    max_attempts: int | None = 1,
    expected_exceptions: list[Type[Exception]] | None = None
):
    """
        A decorator to retry a function up to `max_attempts` if it raises
        any of the exceptions in `expected_exceptions`. If an expected exception
        occurs, the function will not retry further.

        Args:
            max_attempts (int | None): Maximum number of attempts to retry the function.

            expected_exceptions (list[Type[Exception]] | None):
            List of exceptions to handle without retrying.

        Returns:
            Decorated function with retry mechanism.
        """
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            attempt = 1
            while attempt <= max_attempts:
                function_info = f'run "{func.__name__}" with '
                if args:
                    function_info += f'positional args = {args}, '
                if kwargs:
                    function_info += f'keyword kwargs = {kwargs}, '
                function_info += f'attempt = {attempt}, '

                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    function_info += f'exception = {type(e).__name__}'
                    print(function_info)
                    if (
                        expected_exceptions is not None
                        and isinstance(e, tuple(expected_exceptions))
                    ):
                        return None
                    attempt += 1
                    if attempt > max_attempts:
                        return None
                else:
                    function_info += f'result = {result}'
                    print(function_info)
                    return result
            return None
        return wrapped
    return wrapper


@retry_deco(3)
def add(a, b):
    """
    Simple addition function used to test the retry_deco decorator.
    """
    return a + b


@retry_deco(3)
def check_str(value=None):
    """
    Function that checks if the input value is a string.
    Raises a ValueError if the value is None.
    """
    if value is None:
        raise ValueError()
    return isinstance(value, str)


@retry_deco(2, [ValueError])
def check_int(value=None):
    """
    Function that checks if the input value is an integer.
    Raises a ValueError if the value is None.
    """
    if value is None:
        raise ValueError()
    return isinstance(value, int)
