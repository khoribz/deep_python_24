from typing import Iterable, Any

import pytest


def parametrize_with_dict(argnames: list[str], cases: Iterable[dict[str, Any]]):
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
