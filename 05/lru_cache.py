"""
This module provides an LRUCache class, which implements a simple Least Recently Used (LRU) cache.
The cache stores a fixed number of items, evicting the least recently used item when capacity is exceeded.
"""
from collections.abc import Hashable
from typing import TypeVar
from venv import logger

from pydantic import BaseModel, field_validator, ValidationError

K = TypeVar('K')
V = TypeVar('V')


class Capacity(BaseModel):
    """Represents the capacity of an LRU cache with validation to ensure it's non-negative."""
    value: int

    @field_validator('value')
    @classmethod
    def validate_value(cls, value: int) -> int:
        """Validates that the capacity is non-negative."""
        if value < 0:
            logger.error('Capacity must be non-negative')
            raise ValidationError('Incorrect value')
        return value


class LRUCache:
    """A Least Recently Used (LRU) cache implementation with a fixed capacity."""

    def __init__(self, capacity: int = 42):
        """
            Initializes the LRUCache with a specified capacity.

            Args:
                capacity (int): Maximum number of items that can be stored in the cache.
                                If exceeded, the least recently used item is evicted.
        """
        self.__capacity = Capacity(value=capacity)
        self.__data = {}

    @property
    def capacity(self) -> int:
        """Returns the capacity of the cache."""
        return self.__capacity.value

    def get(self, key: K) -> V | None:
        """
            Retrieves the value associated with the given key.
            Moves the accessed key to the end to mark it as recently used.

            Args:
                key (K): The key to retrieve from the cache.

            Returns:
                V | None: The associated value if the key exists, or None if not.
        """
        if (value := self.__data.get(key)) is None:
            return None

        self.__data.pop(key)
        self.__data[key] = value
        return value

    def set(self, key: K, value: V) -> None:
        """
            Sets the value for a key in the cache. If the cache is full, evicts the

            least recently used item before adding the new key-value pair.

            Args:
                key (K): The key to set in the cache.
                value (V): The value to associate with the key.

            Raises:
                TypeError: If the key is not hashable.
        """
        if not isinstance(key, Hashable):
            raise TypeError(f'Unhashable type: {type(key).__name__}')

        if self.__data.get(key) is not None:
            self.__data.pop(key)
            self.__data[key] = value
        else:
            self.__data[key] = value
            if len(self.__data) > self.capacity:
                self.__data.pop(next(iter(self.__data)))
