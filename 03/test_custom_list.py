"""
This module contains tests for the CustomList class, which verifies its
addition, subtraction, and comparison functionality, as well as its string
representation and behavior when interacting with lists and numbers.
"""

import pytest

from test_parametrize_with_dict import parametrize_with_dict
from custom_list import CustomList


def transform_to_list(value: CustomList | list | int) -> list:
    return list(value) if isinstance(value, (list, CustomList)) else [value]


@parametrize_with_dict(
    ['first_operand', 'second_operand', 'expected_result', 'expected_str_result'],
    [
        {
            'case_id': 0,
            'test_name': 'add: empty custom lists',
            'first_operand': CustomList(),
            'second_operand': CustomList(),
            'expected_result': CustomList(),
            'expected_str_result': '[], sum = 0',
        },
        {
            'case_id': 1,
            'test_name': 'add: non-empty custom list and empty custom list',
            'first_operand': CustomList([1]),
            'second_operand': CustomList(),
            'expected_result': CustomList([1]),
            'expected_str_result': '[1], sum = 1',
        },
        {
            'case_id': 2,
            'test_name': 'add: empty custom list and non-empty custom list',
            'first_operand': CustomList(),
            'second_operand': CustomList([-100]),
            'expected_result': CustomList([-100]),
            'expected_str_result': '[-100], sum = -100',
        },
        {
            'case_id': 3,
            'test_name': 'add: non-empty custom list and non-empty custom list with one sizes',
            'first_operand': CustomList([1]),
            'second_operand': CustomList([4]),
            'expected_result': CustomList([5]),
            'expected_str_result': '[5], sum = 5',
        },
        {
            'case_id': 4,
            'test_name': 'add: non-empty custom list and non-empty custom list with different sizes',
            'first_operand': CustomList([1]),
            'second_operand': CustomList([4, 5, 6]),
            'expected_result': CustomList([5, 5, 6]),
            'expected_str_result': '[5, 5, 6], sum = 16',
        },
        {
            'case_id': 5,
            'test_name': 'add: empty custom list and number',
            'first_operand': CustomList(),
            'second_operand': 5,
            'expected_result': CustomList([5]),
            'expected_str_result': '[5], sum = 5',
        },
        {
            'case_id': 6,
            'test_name': 'add: number and empty custom list',
            'first_operand': -5,
            'second_operand': CustomList(),
            'expected_result': CustomList([-5]),
            'expected_str_result': '[-5], sum = -5',
        },
        {
            'case_id': 7,
            'test_name': 'add: non-empty custom list and number',
            'first_operand': CustomList([5, 3, 1]),
            'second_operand': 5,
            'expected_result': CustomList([10, 8, 6]),
            'expected_str_result': '[10, 8, 6], sum = 24',
        },
        {
            'case_id': 8,
            'test_name': 'add: number and non-empty custom list',
            'first_operand': 5,
            'second_operand': CustomList([5, 3, 1]),
            'expected_result': CustomList([10, 8, 6]),
            'expected_str_result': '[10, 8, 6], sum = 24',
        },
        {
            'case_id': 9,
            'test_name': 'add: empty custom list and empty list',
            'first_operand': CustomList(),
            'second_operand': [],
            'expected_result': CustomList(),
            'expected_str_result': '[], sum = 0',
        },
        {
            'case_id': 10,
            'test_name': 'add: empty custom list and non-empty list',
            'first_operand': CustomList(),
            'second_operand': [1, 2, 3],
            'expected_result': CustomList([1, 2, 3]),
            'expected_str_result': '[1, 2, 3], sum = 6',
        },
        {
            'case_id': 11,
            'test_name': 'add: non-empty custom list and empty list',
            'first_operand': CustomList([-1, -2, 3]),
            'second_operand': [],
            'expected_result': CustomList([-1, -2, 3]),
            'expected_str_result': '[-1, -2, 3], sum = 0',
        },
        {
            'case_id': 11,
            'test_name': 'add: non-empty custom list and non-empty list with one sizes',
            'first_operand': CustomList([-1, -2, 3]),
            'second_operand': [5, 6, 3],
            'expected_result': CustomList([4, 4, 6]),
            'expected_str_result': '[4, 4, 6], sum = 14',
        },
        {
            'case_id': 12,
            'test_name': 'add: non-empty custom list and non-empty list with different sizes',
            'first_operand': CustomList([-1, -2, 3, 0, 1]),
            'second_operand': [5],
            'expected_result': CustomList([4, -2, 3, 0, 1]),
            'expected_str_result': '[4, -2, 3, 0, 1], sum = 6',
        },
        {
            'case_id': 13,
            'test_name': 'add: two large custom lists',
            'first_operand': CustomList(list(range(1000))),
            'second_operand': CustomList(list(range(1000))),
            'expected_result': CustomList([i * 2 for i in range(1000)]),
            'expected_str_result': f'[{", ".join(str(i * 2) for i in range(1000))}], sum = {999000}',
        }
    ]
)
def test_custom_list_add(first_operand, second_operand, expected_result, expected_str_result):
    """
        Test addition of CustomList instances and lists/numbers.
        Verifies the result and ensures immutability of the original lists.
    """
    first_operand_copy = transform_to_list(first_operand)
    second_operand_copy = transform_to_list(second_operand)
    result = first_operand + second_operand

    assert result == expected_result
    assert transform_to_list(result) == transform_to_list(expected_result)
    assert result is not first_operand
    assert result is not second_operand
    assert str(result) == expected_str_result

    assert first_operand_copy == transform_to_list(first_operand)
    assert second_operand_copy == transform_to_list(second_operand)


@parametrize_with_dict(
    ['first_operand', 'second_operand', 'expected_result', 'expected_str_result'],
    [
        {
            'case_id': 0,
            'test_name': 'sub: empty custom lists',
            'first_operand': CustomList(),
            'second_operand': CustomList(),
            'expected_result': CustomList(),
            'expected_str_result': '[], sum = 0',
        },
        {
            'case_id': 1,
            'test_name': 'sub: non-empty custom list and empty custom list',
            'first_operand': CustomList([1]),
            'second_operand': CustomList(),
            'expected_result': CustomList([1]),
            'expected_str_result': '[1], sum = 1',
        },
        {
            'case_id': 2,
            'test_name': 'sub: empty custom list and non-empty custom list',
            'first_operand': CustomList(),
            'second_operand': CustomList([-100]),
            'expected_result': CustomList([100]),
            'expected_str_result': '[100], sum = 100',
        },
        {
            'case_id': 3,
            'test_name': 'sub: non-empty custom list and non-empty custom list with one sizes',
            'first_operand': CustomList([1]),
            'second_operand': CustomList([4]),
            'expected_result': CustomList([-3]),
            'expected_str_result': '[-3], sum = -3',
        },
        {
            'case_id': 4,
            'test_name': 'sub: non-empty custom list and non-empty custom list with different sizes',
            'first_operand': CustomList([1]),
            'second_operand': CustomList([4, 5, 6]),
            'expected_result': CustomList([-3, -5, -6]),
            'expected_str_result': '[-3, -5, -6], sum = -14',
        },
        {
            'case_id': 5,
            'test_name': 'sub: non-empty custom list and non-empty custom list with different sizes',
            'first_operand': CustomList([4, 5, 6]),
            'second_operand': CustomList([-9, 8]),
            'expected_result': CustomList([13, -3, 6]),
            'expected_str_result': '[13, -3, 6], sum = 16',
        },
        {
            'case_id': 6,
            'test_name': 'sub: empty custom list and number',
            'first_operand': CustomList(),
            'second_operand': 5,
            'expected_result': CustomList([-5]),
            'expected_str_result': '[-5], sum = -5',
        },
        {
            'case_id': 7,
            'test_name': 'sub: number and empty custom list',
            'first_operand': -5,
            'second_operand': CustomList(),
            'expected_result': CustomList([-5]),
            'expected_str_result': '[-5], sum = -5',
        },
        {
            'case_id': 8,
            'test_name': 'sub: non-empty custom list and number',
            'first_operand': CustomList([5, 3, 1]),
            'second_operand': 5,
            'expected_result': CustomList([0, -2, -4]),
            'expected_str_result': '[0, -2, -4], sum = -6',
        },
        {
            'case_id': 9,
            'test_name': 'sub: number and non-empty custom list',
            'first_operand': 5,
            'second_operand': CustomList([5, 3, -1]),
            'expected_result': CustomList([0, 2, 6]),
            'expected_str_result': '[0, 2, 6], sum = 8',
        },
        {
            'case_id': 10,
            'test_name': 'sub: empty custom list and empty list',
            'first_operand': CustomList(),
            'second_operand': [],
            'expected_result': CustomList(),
            'expected_str_result': '[], sum = 0',
        },
        {
            'case_id': 11,
            'test_name': 'sub: empty custom list and non-empty list',
            'first_operand': CustomList(),
            'second_operand': [1, 2, -3],
            'expected_result': CustomList([-1, -2, 3]),
            'expected_str_result': '[-1, -2, 3], sum = 0',
        },
        {
            'case_id': 12,
            'test_name': 'sub: non-empty custom list and empty list',
            'first_operand': CustomList([-1, -2, 3]),
            'second_operand': [],
            'expected_result': CustomList([-1, -2, 3]),
            'expected_str_result': '[-1, -2, 3], sum = 0',
        },
        {
            'case_id': 13,
            'test_name': 'sub: non-empty custom list and non-empty list with one sizes',
            'first_operand': CustomList([-1, -2, 3]),
            'second_operand': [5, 6, 3],
            'expected_result': CustomList([-6, -8, 0]),
            'expected_str_result': '[-6, -8, 0], sum = -14',
        },
        {
            'case_id': 14,
            'test_name': 'sub: non-empty custom list and non-empty list with different sizes',
            'first_operand': CustomList([-1, -2, 3, 0, 1]),
            'second_operand': [5],
            'expected_result': CustomList([-6, -2, 3, 0, 1]),
            'expected_str_result': '[-6, -2, 3, 0, 1], sum = -4',
        },
        {
            'case_id': 15,
            'test_name': 'sub: two large custom lists',
            'first_operand': CustomList(list(range(1000))),
            'second_operand': CustomList(list(range(1000))),
            'expected_result': CustomList([0 for _ in range(1000)]),
            'expected_str_result': f'[{", ".join(str(0) for _ in range(1000))}], sum = {0}',
        }
    ]
)
def test_custom_list_sub(first_operand, second_operand, expected_result, expected_str_result):
    """
        Test subtraction of CustomList instances and lists/numbers.
        Verifies the result and ensures immutability of the original lists.
    """
    first_operand_copy = transform_to_list(first_operand)
    second_operand_copy = transform_to_list(second_operand)
    result = first_operand - second_operand

    assert result == expected_result
    assert transform_to_list(result) == transform_to_list(expected_result)

    assert result is not first_operand
    assert result is not second_operand
    assert str(result) == expected_str_result

    assert first_operand_copy == transform_to_list(first_operand)
    assert second_operand_copy == transform_to_list(second_operand)


def test_custom_list():
    """
       Simple tests for addition and subtraction of CustomList instances and lists/numbers.
       Includes both basic and reverse operations.
    """
    assert CustomList([5, 1, 3, 7]) + CustomList([1, 2, 7]) == CustomList([6, 3, 10, 7])
    assert CustomList([10]) + [2, 5] == CustomList([12, 5])
    assert [2, 5] + CustomList([10]) == CustomList([12, 5])
    assert CustomList([2, 5]) + 10 == CustomList([12, 15])
    assert 10 + CustomList([2, 5]) == CustomList([12, 15])

    assert CustomList([5, 1, 3, 7]) - CustomList([1, 2, 7]) == CustomList([4, -1, -4, 7])
    assert CustomList([10]) - [2, 5] == CustomList([8, -5])
    assert [2, 5] - CustomList([10]) == CustomList([-8, 5])
    assert CustomList([2, 5]) - 10 == CustomList([-8, -5])
    assert 10 - CustomList([2, 5]) == CustomList([8, 5])


@parametrize_with_dict(
    ['first_operand', 'second_operand', 'expected_result'],
    [
        {
            'case_id': 0,
            'test_name': 'eq: equal custom lists',
            'first_operand': CustomList([1, 2, 3]),
            'second_operand': CustomList([1, 2, 3]),
            'expected_result': True,
        },
        {
            'case_id': 1,
            'test_name': 'eq: unequal custom lists',
            'first_operand': CustomList([1, 2, 3]),
            'second_operand': CustomList([4, 5, 6]),
            'expected_result': False,
        },
        {
            'case_id': 2,
            'test_name': 'eq: empty custom lists',
            'first_operand': CustomList(),
            'second_operand': CustomList(),
            'expected_result': True,
        },
        {
            'case_id': 3,
            'test_name': 'eq: non-empty and empty custom list',
            'first_operand': CustomList([1, 2, 3]),
            'second_operand': CustomList(),
            'expected_result': False,
        },
        {
            'case_id': 4,
            'test_name': 'eq: equal sum, but different elements',
            'first_operand': CustomList([1, 2, 3]),
            'second_operand': CustomList([2, 2, 1, 1]),
            'expected_result': True,
        },
    ]
)
def test_custom_list_eq(first_operand, second_operand, expected_result):
    """
    Test equality comparison (==) between CustomList instances.
    """
    assert (first_operand == second_operand) == expected_result


@parametrize_with_dict(
    ['first_operand', 'second_operand', 'expected_result'],
    [
        {
            'case_id': 0,
            'test_name': 'ne: unequal custom lists',
            'first_operand': CustomList([1, 2, 3]),
            'second_operand': CustomList([4, 5, 6]),
            'expected_result': True,
        },
        {
            'case_id': 1,
            'test_name': 'ne: equal custom lists',
            'first_operand': CustomList([1, 2, 3]),
            'second_operand': CustomList([1, 2, 3]),
            'expected_result': False,
        },
        {
            'case_id': 2,
            'test_name': 'ne: empty custom lists',
            'first_operand': CustomList(),
            'second_operand': CustomList(),
            'expected_result': False,
        },
    ]
)
def test_custom_list_ne(first_operand, second_operand, expected_result):
    """
    Test inequality comparison (!=) between CustomList instances.
    """
    assert (first_operand != second_operand) == expected_result


@parametrize_with_dict(
    ['first_operand', 'second_operand', 'expected_result'],
    [
        {
            'case_id': 0,
            'test_name': 'lt: smaller custom list',
            'first_operand': CustomList([1, 2, 3]),
            'second_operand': CustomList([4, 5, 6]),
            'expected_result': True,
        },
        {
            'case_id': 1,
            'test_name': 'lt: larger custom list',
            'first_operand': CustomList([4, 5, 6]),
            'second_operand': CustomList([1, 2, 3]),
            'expected_result': False,
        },
        {
            'case_id': 2,
            'test_name': 'lt: equal custom lists',
            'first_operand': CustomList([1, 2, 3]),
            'second_operand': CustomList([1, 2, 3]),
            'expected_result': False,
        },
    ]
)
def test_custom_list_lt(first_operand, second_operand, expected_result):
    """
    Test less-than comparison (<) between CustomList instances.
    """
    assert (first_operand < second_operand) == expected_result


@parametrize_with_dict(
    ['first_operand', 'second_operand', 'expected_result'],
    [
        {
            'case_id': 0,
            'test_name': 'le: smaller or equal custom list',
            'first_operand': CustomList([1, 2, 3]),
            'second_operand': CustomList([4, 5, 6]),
            'expected_result': True,
        },
        {
            'case_id': 1,
            'test_name': 'le: equal custom lists',
            'first_operand': CustomList([1, 2, 3]),
            'second_operand': CustomList([1, 2, 3]),
            'expected_result': True,
        },
        {
            'case_id': 2,
            'test_name': 'le: larger custom list',
            'first_operand': CustomList([4, 5, 6]),
            'second_operand': CustomList([1, 2, 3]),
            'expected_result': False,
        },
    ]
)
def test_custom_list_le(first_operand, second_operand, expected_result):
    """
    Test less-than-or-equal comparison (<=) between CustomList instances.
    """
    assert (first_operand <= second_operand) == expected_result


@parametrize_with_dict(
    ['first_operand', 'second_operand', 'expected_result'],
    [
        {
            'case_id': 0,
            'test_name': 'gt: larger custom list',
            'first_operand': CustomList([4, 5, 6]),
            'second_operand': CustomList([1, 2, 3]),
            'expected_result': True,
        },
        {
            'case_id': 1,
            'test_name': 'gt: smaller custom list',
            'first_operand': CustomList([1, 2, 3]),
            'second_operand': CustomList([4, 5, 6]),
            'expected_result': False,
        },
        {
            'case_id': 2,
            'test_name': 'gt: equal custom lists',
            'first_operand': CustomList([1, 2, 3]),
            'second_operand': CustomList([1, 2, 3]),
            'expected_result': False,
        },
    ]
)
def test_custom_list_gt(first_operand, second_operand, expected_result):
    """
    Test greater-than comparison (>) between CustomList instances.
    """
    assert (first_operand > second_operand) == expected_result


@parametrize_with_dict(
    ['first_operand', 'second_operand', 'expected_result'],
    [
        {
            'case_id': 0,
            'test_name': 'ge: larger custom list',
            'first_operand': CustomList([4, 5, 6]),
            'second_operand': CustomList([1, 2, 3]),
            'expected_result': True,
        },
        {
            'case_id': 1,
            'test_name': 'ge: equal custom lists',
            'first_operand': CustomList([1, 2, 3]),
            'second_operand': CustomList([1, 2, 3]),
            'expected_result': True,
        },
        {
            'case_id': 2,
            'test_name': 'ge: smaller custom list',
            'first_operand': CustomList([1, 2, 3]),
            'second_operand': CustomList([4, 5, 6]),
            'expected_result': False,
        },
    ]
)
def test_custom_list_ge(first_operand, second_operand, expected_result):
    """
    Test greater-than-or-equal comparison (>=) between CustomList instances.
    """
    assert (first_operand >= second_operand) == expected_result


def test_custom_list_eq_with_wrong_type():
    """
    Test equality comparison (==) between CustomList and an unsupported type.

    This test verifies that attempting to compare a CustomList instance
    with a string raises a NotImplementedError.
    """
    with pytest.raises(NotImplementedError):
        assert CustomList([1, 2, 3]) == '[1, 2, 3]'


def test_custom_list_gt_with_wrong_type():
    """
    Test greater-than comparison (>) between CustomList and an unsupported type.

    This test ensures that attempting to compare a CustomList instance
    with a string raises a NotImplementedError.
    """
    with pytest.raises(NotImplementedError):
        assert CustomList([1, 2, 3]) > '[1, 2, 3]'


def test_custom_list_add_with_wrong_type():
    """
    Test addition of CustomList with an unsupported type.

    This test checks that attempting to add a CustomList instance to a string
    raises a NotImplementedError.
    """
    with pytest.raises(NotImplementedError):
        assert CustomList([1, 2, 3]) + '123'
