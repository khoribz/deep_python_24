"""
This module defines a custom metaclass `CustomMeta` which modifies class attribute names
by adding a 'custom_' prefix, unless the attribute is a magic method or already has the prefix.
"""

from typing import Any


class CustomMeta(type):
    """
        A metaclass that prefixes all non-magic attributes of a class with 'custom_'.
        Also modifies the `__setattr__` method to ensure attributes are set with the same prefix.
    """
    def __new__(mcs, name: str, bases: tuple, class_dict: dict[str, Any]) -> Any:
        """
            Create a new class by prefixing non-magic attributes with 'custom_'.
            Overrides the `__setattr__` method to ensure attributes are set with the 'custom_' prefix.

            :param mcs: The metaclass (CustomMeta).
            :param name: The name of the class being created.
            :param bases: The base classes of the class being created.
            :param class_dict: The class's attribute dictionary.
            :return: The newly created class.
        """
        custom_class_dict = mcs.add_custom_prefix_to_attributes(class_dict)

        def custom_setattr(self, key: str, value: Any) -> None:
            """
                A custom `__setattr__` method that prefixes attribute names with 'custom_'
                when setting a value, unless it's a magic attribute or already has the prefix
                :param self: The instance of the class.
                :param key: The attribute name being set.
                :param value: The value being set to the attribute.
            """
            if not mcs.is_magic_attr(key) and not key.startswith('custom_'):
                key = f'custom_{key}'
            super(type(self), self).__setattr__(key, value)

        custom_class_dict['__setattr__'] = custom_setattr

        return super().__new__(mcs, name, bases, custom_class_dict)

    @staticmethod
    def is_magic_attr(attr_name: str) -> bool:
        """
            Checks if an attribute is a magic method (e.g., starts and ends with '__').

            :param attr_name: The name of the attribute.
            :return: True if it's a magic method, False otherwise.
        """
        return attr_name.startswith('__') and attr_name.endswith('__')

    @staticmethod
    def add_custom_prefix_to_attributes(class_dict: dict[str, Any]) -> dict[str, Any]:
        """
            Prefixes all non-magic attributes in the given class dictionary with 'custom_'.

            :param class_dict: The class's attribute dictionary.
            :return: A new dictionary with prefixed attribute names for non-magic attributes.
        """
        prefixed_class_dict = {}

        for attr_name, attr_value in class_dict.items():
            if CustomMeta.is_magic_attr(attr_name):
                prefixed_class_dict[attr_name] = attr_value
            else:
                prefixed_class_dict[f'custom_{attr_name}'] = attr_value

        return prefixed_class_dict
