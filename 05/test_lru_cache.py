"""
Test suite for the LRUCache class.

This module tests various functionalities of the LRUCache implementation,
including setting and getting values, eviction policy, capacity constraints,
and handling of edge cases.
"""

import pytest

from lru_cache import LRUCache


def test_default_capacity():
    """Test that the default capacity is set to 42."""
    cache = LRUCache()
    assert cache.capacity == 42
    with pytest.raises(AttributeError):
        _ = cache.__data  # pylint: disable=protected-access


def test_provided_capacity():
    """Test that the cache capacity is set correctly when provided."""
    cache = LRUCache(10)
    assert cache.capacity == 10


def test_incorrect_capacity():
    """Test that providing a negative capacity raises a TypeError."""
    with pytest.raises(TypeError):
        LRUCache(-1)


def test_capacity_zero():
    """Test that a cache with zero capacity cannot store items."""
    cache = LRUCache(0)
    cache.set(1, 'a')
    assert cache.get(1) is None


def test_capacity_one():
    """Test the behavior of a cache with a capacity of one."""
    cache = LRUCache(1)
    cache.set(1, 'a')
    cache.set(2, 'b')
    assert cache.get(1) is None
    assert cache.get(2) == 'b'


def test_set_and_get_single():
    """Test setting and retrieving a single item."""
    cache = LRUCache(2)
    cache.set(1, 'a')
    assert cache.get(1) == 'a'


def test_get_non_existent_key():
    """Test that getting a non-existent key returns None."""
    cache = LRUCache(2)
    assert cache.get(90) is None


def test_eviction_policy():
    """Test that the eviction policy removes the least recently used item."""
    cache = LRUCache(2)
    cache.set(1, 'a')
    cache.set(2, 'b')
    cache.set(3, 'c')  # This should evict key 1
    assert cache.get(1) is None
    assert cache.get(2) == 'b'
    assert cache.get(3) == 'c'


def test_update_existing_key():
    """Test updating the value of an existing key."""
    cache = LRUCache(2)
    cache.set(1, 'a')
    cache.set(1, 'b')  # Update key 1
    assert cache.get(1) == 'b'
    assert len(cache._LRUCache__data) == 1  # pylint: disable=protected-access


def test_re_adding_evicted_key():
    """Test re-adding a key that was previously evicted."""
    cache = LRUCache(2)
    cache.set(1, 'a')
    cache.set(2, 'b')
    cache.set(3, 'c')  # Evict key 1
    cache.set(1, 'd')  # Re-add key 1
    assert cache.get(1) == 'd'
    assert cache.get(3) == 'c'
    assert cache.get(2) is None


def test_duplicate_keys():
    """Test setting the same key multiple times and updating its value."""
    cache = LRUCache(3)
    cache.set(1, 'a')
    cache.set(1, 'b')  # Update key 1
    cache.set(2, 'c')
    cache.set(3, 'd')
    assert cache.get(1) == 'b'
    assert cache.get(2) == 'c'
    assert cache.get(3) == 'd'
    assert len(cache._LRUCache__data) == 3  # pylint: disable=protected-access


def test_overflow_set_conditions():
    """Test setting items beyond capacity and eviction of least recently used items."""
    cache = LRUCache(3)
    cache.set(1, 'a')
    cache.set(2, 'b')
    cache.set(3, 'c')
    cache.set(4, 'd')  # This should evict key 1
    assert cache.get(1) is None  # Key 1 should be evicted
    assert cache.get(2) == 'b'
    assert cache.get(3) == 'c'
    assert cache.get(4) == 'd'


def test_set_and_get_conditions():
    """Test combinations of setting and getting keys to verify LRU behavior."""
    cache = LRUCache(3)
    cache.set(1, 'a')
    cache.set(2, 'b')
    cache.set(3, 'c')
    cache.get(4)
    assert cache.get(1) == 'a'
    assert cache.get(2) == 'b'
    assert cache.get(3) == 'c'
    assert cache.get(4) is None

    cache.get(2)
    assert cache.get(1) == 'a'
    assert cache.get(2) == 'b'
    assert cache.get(3) == 'c'
    assert cache.get(4) is None

    cache.set(5, 'e')
    assert cache.get(1) is None
    assert cache.get(2) == 'b'
    assert cache.get(3) == 'c'
    assert cache.get(5) == 'e'


def test_data_types():
    """Test cache with various hashable key types like tuples, strings, and integers."""
    cache = LRUCache(3)
    cache.set((1, 2), 'tuple_key')
    cache.set('string_key', 'string_value')
    cache.set(42, 'int_key')
    assert cache.get((1, 2)) == 'tuple_key'
    assert cache.get('string_key') == 'string_value'
    assert cache.get(42) == 'int_key'


def test_set_unhashable_type():
    """Test that setting an unhashable key raises a TypeError."""
    cache = LRUCache(2)
    with pytest.raises(TypeError):
        cache.set([1], 'a')


def test_in_task():
    """Test that is provided in the task"""
    cache = LRUCache(2)

    cache.set("k1", "val1")
    cache.set("k2", "val2")

    assert cache.get("k3") is None
    assert cache.get("k2") == "val2"
    assert cache.get("k1") == "val1"

    cache.set("k3", "val3")

    assert cache.get("k3") == "val3"
    assert cache.get("k2") is None
    assert cache.get("k1") == "val1"


def test_set_and_get_none_value():
    """Test that None can be stored and retrieved as a valid value."""
    cache = LRUCache(2)
    cache.set(1, None)
    assert cache.get(1) is None
    assert cache.get(2) is None


def test_update_existing_key_and_eviction():
    """Test updating an existing key and its impact on eviction."""
    cache = LRUCache(2)
    cache.set(1, 'a')
    cache.set(2, 'b')
    cache.set(1, 'updated')
    cache.set(3, 'c')
    assert cache.get(1) == 'updated'
    assert cache.get(2) is None
    assert cache.get(3) == 'c'
