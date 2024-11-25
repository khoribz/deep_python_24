"""
This script benchmarks the performance of three different class types in Python:
1. RegularClass: A standard class with regular attribute storage.
2. SlotsClass: A class optimized with `__slots__` for memory efficiency.
3. WeakRefClass: A class using weak references for attribute storage.

The script measures:
- Creation time for a large number of instances.
- Access and modification time for attributes of these instances.

It demonstrates how design choices affect performance.
"""

import time
import weakref

from memory_profiler import profile


class RegularClass:
    """
    A class with a standard definition, using regular attributes for storage.
    """

    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b


class SlotsClass:
    """
    A class optimized with `__slots__` to restrict attribute storage.
    """

    __slots__ = ('a', 'b')

    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b


class WeakRefValue:
    """
    A helper class to represent objects referenced weakly in `WeakRefClass`.
    """

    def __init__(self, a: int):
        self.a = a


class WeakRefClass:
    """
    A class storing attributes as weak references to objects.
    """

    def __init__(self, a: int, b: int):
        self.a = weakref.ref(WeakRefValue(a))
        self.b = weakref.ref(WeakRefValue(b))


def benchmark_class_creation(cls, n: int):
    """
    Measure the time required to create `n` instances of a class.

    Args:
        cls: The class to be instantiated.
        n: Number of instances to create.

    Returns:
        A tuple containing the list of instances and the elapsed time.
    """
    start_time = time.time()
    instances = [cls(i, i + 1) for i in range(n)]
    end_time = time.time()
    return instances, end_time - start_time


def benchmark_attribute_access_and_modification(instances):
    """
        Measure the time required to access and modify attributes of instances.

        Args:
            instances: List of instances whose attributes are to be accessed.

        Returns:
            The elapsed time for accessing and modifying attributes.
    """
    start_time = time.time()
    for instance in instances:
        _ = instance.a
        _ = instance.b
        instance.a = 2
        instance.b = 3
    end_time = time.time()
    return end_time - start_time


@profile
def main():
    """
        Provides benchmarks
    """
    n = 10_000_000

    regular_instances, regular_creation_time = benchmark_class_creation(RegularClass, n)
    regular_access_time = benchmark_attribute_access_and_modification(regular_instances)

    slots_instances, slots_creation_time = benchmark_class_creation(SlotsClass, n)
    slots_access_time = benchmark_attribute_access_and_modification(slots_instances)

    weakref_instances, weakref_creation_time = benchmark_class_creation(WeakRefClass, n)
    weakref_access_time = benchmark_attribute_access_and_modification(weakref_instances)

    print(
        f"RegularClass: Creation Time: {regular_creation_time:.5f}s, "
        f"Access/Modification Time: {regular_access_time:.5f}s"
    )
    print(
        f"SlotsClass: Creation Time: {slots_creation_time:.5f}s, "
        f"Access/Modification Time: {slots_access_time:.5f}s"
    )
    print(
        f"WeakRefClass: Creation Time: {weakref_creation_time:.5f}s, "
        f"Access/Modification Time: {weakref_access_time:.5f}s"
    )


if __name__ == '__main__':
    main()
