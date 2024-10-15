"""
This module provides utility functions to assist with test parameterization in pytest.

It includes:
- parametrize_with_dict: A decorator to parameterize a test
function with cases provided as dictionaries.
"""

from typing import Iterable, Any

import pytest


def parametrize_with_dict(argnames: list[str], cases: Iterable[dict[str, Any]]):
    """
        A decorator for parameterizing pytest test functions with cases defined as dictionaries.

        Args:
            argnames (list[str]): A list of argument names for the test function.

            cases (Iterable[dict[str, Any]]): An iterable of dictionaries where
            each dictionary represents a test case, with the keys being argument names.

        Returns:
            The test function decorated with pytest's parametrize decorator.
        """
    def decorator(func):
        return pytest.mark.parametrize(
            argnames,
            [
                pytest.param(
                    *[case[arg_name] for arg_name in argnames if arg_name != 'test_name'],
                    id=str(case.get('case_id') or idx)
                )
                for idx, case in enumerate(cases)
            ],
        )(func)

    return decorator
