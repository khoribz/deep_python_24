"""
This module contains the CustomList class, which extends the functionality
of Python's built-in list. It allows addition and subtraction of CustomList
instances, integers, and regular lists, as well as element-wise operations.
It also includes comparison operations based on the sum of the list elements.
"""


from __future__ import annotations

from collections.abc import Callable


class CustomList(list):
    """
        CustomList class inherits from the built-in list class and allows addition
        and subtraction of lists, integers, and other CustomList instances.

        It also supports element-wise operations and compares the sum of elements
        between instances.
        """

    def __init__(self, values: list[int] | None = None):
        """
            Initializes the CustomList with the given values.
            If no values are provided, an empty list is initialized.
        """
        if values is None:
            values = []
        super().__init__(values)
        self.sum = sum(values)

    def _operate(self, other: list[int] | int, operator: Callable[[int, int], int]) -> CustomList:
        """
            A helper function for performing element-wise operations (addition or subtraction).

            :param other: A list of integers or a single integer.
            :param operator: A function defining the operation to be performed.
            :return: A new CustomList instance with the result of the operation.
        """
        if isinstance(other, int):
            if not self:
                result = [operator(0, other)]
            else:
                result = [operator(element, other) for element in self]
        elif isinstance(other, list):
            result_length = max(len(self), len(other))
            result = [
                operator(self[i] if i < len(self) else 0, other[i] if i < len(other) else 0)
                for i in range(result_length)
            ]
        else:
            raise NotImplementedError
        return CustomList(result)

    def __add__(self, other: list[int] | int) -> CustomList:
        """
            Adds either another list or an integer to the current CustomList instance.

            :param other: A list of integers or a single integer.
            :return: A new CustomList instance with the result of addition.
        """
        return self._operate(other, lambda x, y: x + y)

    def __radd__(self, other: list[int] | int) -> CustomList:
        """
            Handles the reverse addition case when CustomList is on the right-hand side of the `+`.

            :param other: A list of integers or a single integer.
            :return: A new CustomList instance with the result of addition.
        """
        return self.__add__(other)

    def __sub__(self, other: list[int] | int) -> CustomList:
        """
            Subtracts either another list or an integer from the current CustomList instance.

            :param other: A list of integers or a single integer.
            :return: A new CustomList instance with the result of subtraction.
        """
        return self._operate(other, lambda x, y: x - y)

    def __rsub__(self, other: list[int] | int) -> CustomList:
        """
            Handles the reverse subtraction case when CustomList is on the right-hand side of the `-`.

            :param other: A list of integers or a single integer.
            :return: A new CustomList instance with the result of subtraction.
        """
        return self._operate(other, lambda x, y: y - x)

    def __eq__(self, other: CustomList) -> bool:
        """
            Compares two CustomList instances by the sum of their elements.

            :param other: Another CustomList instance.
            :return: True if sums are equal, False otherwise.
        """
        if isinstance(other, CustomList):
            return self.sum == other.sum

        raise NotImplementedError

    def __ne__(self, other: CustomList) -> bool:
        """
            Checks if two CustomList instances are not equal based on the sum of their elements.

            :param other: Another CustomList instance.
            :return: True if sums are not equal, False otherwise.
        """
        return not self.__eq__(other)

    def __gt__(self, other: CustomList) -> bool:
        """
            Checks if the sum of the current CustomList is greater than another CustomList.

            :param other: Another CustomList instance.
            :return: True if current CustomList sum is greater, False otherwise.
        """
        if isinstance(other, CustomList):
            return self.sum > other.sum

        raise NotImplementedError

    def __ge__(self, other: CustomList) -> bool:
        """
            Checks if the sum of the current CustomList is greater than or equal to another CustomList.

            :param other: Another CustomList instance.
            :return: True if current CustomList sum is greater or equal, False otherwise.
        """
        return self.__eq__(other) or self.__gt__(other)

    def __le__(self, other: CustomList) -> bool:
        """
            Checks if the sum of the current CustomList is less than or equal to another CustomList.

            :param other: Another CustomList instance.
            :return: True if current CustomList sum is less or equal, False otherwise.
        """
        return not self.__gt__(other)

    def __lt__(self, other: CustomList) -> bool:
        """
            Checks if the sum of the current CustomList is less than another CustomList.

            :param other: Another CustomList instance.
            :return: True if current CustomList sum is less, False otherwise.
        """
        return not self.__ge__(other)

    def __str__(self) -> str:
        """
            Returns a string representation of the CustomList instance showing the elements and their sum.

            :return: String representation of the list and the sum of its elements.
        """
        return f'{list(self)}, sum = {sum(self)}'
