"""
Unit tests for the `CustomClass` created using `CustomMeta`.
Tests cover custom attribute behavior, dynamic attribute creation, and reserved keyword handling.
"""

import pytest
from metaclass import CustomMeta


class CustomClass(metaclass=CustomMeta):  # pylint: disable=too-many-instance-attributes
    """
    A sample class using the `CustomMeta` metaclass to demonstrate custom attribute handling.
    """
    x = 50

    def __init__(self, val=99):
        self.val = val

    def line(self):
        """
        :return: 100
        """
        return 100

    def __str__(self):
        return 'Custom_by_metaclass'


def test_custom_class_attributes():
    """
    Test that class-level attributes are prefixed with 'custom_'.
    """
    assert CustomClass.custom_x == 50
    with pytest.raises(AttributeError):
        _ = CustomClass.x  # x should not exist, only custom_x should.


def test_custom_class_instance_attributes():
    """
    Test that instance attributes are correctly prefixed with 'custom_' and
    that attributes can be dynamically set and accessed.
    """
    inst = CustomClass()

    assert inst.custom_x == 50
    inst.custom_x = 51
    assert inst.custom_x == 51
    inst.x = 52
    assert inst.custom_x == 52
    with pytest.raises(AttributeError):
        _ = inst.x

    assert inst.custom_val == 99
    inst.custom_val = 98
    assert inst.custom_val == 98
    inst.val = 97
    assert inst.custom_val == 97
    with pytest.raises(AttributeError):
        _ = inst.val

    assert inst.custom_line() == 100
    inst.custom_line = lambda: 101
    assert inst.custom_line() == 101
    inst.line = lambda: 102
    assert inst.custom_line() == 102
    with pytest.raises(AttributeError):
        _ = inst.line()

    assert str(inst) == 'Custom_by_metaclass'

    with pytest.raises(AttributeError):
        _ = inst.unknown_attribute


def test_magic_like_attribute_names():
    """
    Test that magic-like attribute names (e.g., __magic_like__) are not prefixed with 'custom_'.
    """
    inst = CustomClass()

    inst.__magic_like__ = 'test value'

    assert inst.__magic_like__ == 'test value'
    with pytest.raises(AttributeError):
        _ = inst.custom___magic_like__


def test_reserved_keyword_as_attribute_name():
    """
    Test that reserved keywords can be used as attribute names and are prefixed with 'custom_'.
    """
    inst = CustomClass()
    setattr(inst, 'class', 'test value')
    assert inst.custom_class == 'test value'

    setattr(inst, 'def', 'another value')
    assert inst.custom_def == 'another value'


def test_dynamic_attributes():
    """
    Test that dynamic attributes added at runtime are correctly prefixed with 'custom_'.
    """
    inst = CustomClass()

    inst.dynamic = 'added later'
    assert inst.custom_dynamic == 'added later'

    inst.new_func = lambda: 100
    assert inst.custom_new_func() == 100

    with pytest.raises(AttributeError):
        _ = inst.dynamic


def test_with_initial_value():
    """
    Test that the class works with an initial value passed to the constructor.
    """
    inst = CustomClass(60)
    assert inst.custom_x == 50
    assert inst.custom_val == 60
    with pytest.raises(AttributeError):
        _ = inst.val
    with pytest.raises(AttributeError):
        _ = inst.x
