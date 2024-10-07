import functools
from typing import Type


def retry_deco(
    max_attempts: int | None = 1,
    expected_exceptions: list[Type[Exception]] | None = None
):
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
                    if expected_exceptions is not None and isinstance(e, tuple(expected_exceptions)):
                        return
                    attempt += 1
                    if attempt > max_attempts:
                        return
                else:
                    function_info += f'result = {result}'
                    print(function_info)
                    return result
        return wrapped
    return wrapper
