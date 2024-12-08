"""
This module provides an LRUCache class, which implements a simple Least Recently Used (LRU) cache.
The cache stores a fixed number of items, evicting the least recently used item when capacity is exceeded.
"""

import logging
import sys
import argparse
from collections.abc import Hashable
from typing import TypeVar
from pydantic import BaseModel, field_validator, ValidationError


logger = logging.getLogger(__name__)

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
            raise ValidationError('Incorrect value')
        return value


class CustomWordFilter(logging.Filter):
    """Filter to exclude log records with an even number of words."""
    def filter(self, record: logging.LogRecord) -> bool:
        return len(record.msg.split()) % 2 != 0


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
        logger.debug("GET - Try to find: %s", str(key))

        if (value := self.__data.get(key)) is None:
            logger.info("GET - Key not found: %s", str(key))
            return None

        self.__data.pop(key)
        self.__data[key] = value
        logger.info("GET - Key accessed: %s", str(key))
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
        logger.debug("SET - Try to set: %s=%s", str(key), str(value))

        if not isinstance(key, Hashable):
            logger.error('SET - Key must be hashable')
            raise TypeError(f'Unhashable type: {type(key).__name__}')

        if self.__data.get(key) is not None:
            self.__data.pop(key)
            self.__data[key] = value
            logger.info("SET - Key updated: %s", str(key))
        else:
            self.__data[key] = value
            log_body = f"SET - Key added: {key}"
            if len(self.__data) > self.capacity:
                evicted_key = next(iter(self.__data))
                evicted_value = self.__data.pop(evicted_key)
                log_body += f', Evicted least recently used key: {evicted_key}, value: {evicted_value}'
            logger.info(log_body)


def configure_logging(to_stdout: bool, apply_filter: bool):
    """Configures logging based on command-line arguments."""
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("cache.log")
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if apply_filter:
        file_handler.addFilter(CustomWordFilter())

    if to_stdout:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_formatter = logging.Formatter("STDOUT: %(levelname)s - %(message)s")
        stdout_handler.setFormatter(stdout_formatter)
        logger.addHandler(stdout_handler)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LRU Cache with logging.")
    parser.add_argument("-s", action="store_true", help="Log to stdout.")
    parser.add_argument("-f", action="store_true", help="Apply custom filter to logs.")
    args = parser.parse_args()

    configure_logging(to_stdout=args.s, apply_filter=args.f)

    cache = LRUCache(capacity=3)
    cache.set("a", 1)
    cache.set("b", 2)
    cache.get("a")
    cache.set("c", 3)
    cache.set("d", 4)
    cache.get("b")
    cache.set("a", 5)
    cache.get("d")
