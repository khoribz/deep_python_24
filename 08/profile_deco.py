"""
    This module provides profile decorator
"""

import cProfile
import pstats
import io
from functools import wraps


def profile_deco(func):
    """
        Profile decorator for functions
    """
    profiler = cProfile.Profile()
    stats_stream = io.StringIO()

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal profiler
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        return result

    def print_stat():
        nonlocal profiler, stats_stream
        sortby = "cumulative"
        stats = pstats.Stats(profiler, stream=stats_stream)
        stats.strip_dirs().sort_stats(sortby).print_stats()
        print(stats_stream.getvalue())

    wrapper.print_stat = print_stat
    return wrapper


@profile_deco
def add(a, b):
    """
        Add two numbers together with profiler
    """
    return a + b


@profile_deco
def sub(a, b):
    """
        Sub two numbers together with profiler
    """
    return a - b


if __name__ == '__main__':
    for i in range(1000):
        add(i, i + 1)

    for i in range(3000):
        sub(i, i + 1)

    add.print_stat()
    sub.print_stat()
