import builtins
import functools
import itertools
from collections.abc import Generator, Iterable
from typing import Callable, Protocol, TypeVar, cast, runtime_checkable

from .pipette import pipette

## Protocols and TypeVars


@runtime_checkable
class SupportsLessThan(Protocol):
    """
    Protocol to ensure that the object supports the less than operator.
    Used for sorting and comparisons in the `sort_by` function.
    """

    def __lt__(self, other: object) -> bool: ...


_T = TypeVar("_T")
_U = TypeVar("_U")
_COMPARABLE = TypeVar("_COMPARABLE", bound=SupportsLessThan)

## Core Functional Operations


@pipette
def select(iterable: Iterable[_T], selector: Callable[[_T], _U]) -> Iterable[_U]:
    """Applies the selector function to each element in the iterable."""
    return builtins.map(selector, iterable)


@pipette
def where(iterable: Iterable[_T], predicate: Callable[[_T], bool]) -> Iterable[_T]:
    """Filters the iterable based on the predicate function."""
    return builtins.filter(predicate, iterable)


@pipette
def into(iterable: Iterable[_T], typ: Callable[[Iterable[_T]], _U]) -> _U:
    """Converts the iterable into a specific type, such as list, set, or dict."""
    return typ(iterable)


## Iterable slicing and limiting


@pipette
def take(iterable: Iterable[_T], n: int) -> Iterable[_T]:
    """Takes the first n elements from the iterable."""
    return itertools.islice(iterable, n)


@pipette
def skip(iterable: Iterable[_T], n: int) -> Iterable[_T]:
    """Skips the first n elements of the iterable."""
    return itertools.islice(iterable, n, None)


@pipette
def fork(
    iterable: Iterable[_T], funcs: Iterable[Callable[[Iterable[_T]], _U]]
) -> list[_U]:
    """Forks the iterable into multiple outputs based on the provided functions."""
    return [func(iterable) for func in funcs]


@pipette
def zip_with(
    *iterables: Iterable[_T],
) -> Iterable[tuple[_T | None, ...]]:
    """Zips multiple iterables together into tuples."""
    return itertools.zip_longest(*iterables, fillvalue=None)


## Reducing and uniqueness


@pipette
def reduce(
    iterable: Iterable[_T], func: Callable[[_T, _T], _T], initial: _T | None = None
) -> _T:
    """Reduces the iterable to a single value using the provided function."""
    if initial is not None:
        return functools.reduce(func, iterable, initial)
    return functools.reduce(func, iterable)


@pipette
def distinct(iterable: Iterable[_T]) -> Iterable[_T]:
    """Returns an iterable with unique elements, preserving the order."""
    seen: set[_T] = set()
    return (x for x in iterable if x not in seen and not seen.add(x))


unique = distinct  # Alias for distinct


@pipette
def unique_by(iterable: Iterable[_T], key_fn: Callable[[_T], _U]) -> Iterable[_T]:
    """Returns an iterable with unique elements based on the key function."""
    seen: set[_U] = set()
    for item in iterable:
        key = key_fn(item)
        if key not in seen:
            seen.add(key)
            yield item


## Sorting and chunking


@pipette
def sort_by(
    iterable: Iterable[_T], key_fn: Callable[[_T], _COMPARABLE]
) -> Iterable[_T]:
    """Sorts the iterable based on the key function."""
    return sorted(iterable, key=key_fn)


@pipette
def chunk(iterable: Iterable[_T], size: int) -> Iterable[list[_T]]:
    """Splits the iterable into chunks of a specified size."""
    it = iter(iterable)
    while chunk := list(itertools.islice(it, size)):
        yield chunk


@pipette
def partition(
    iterable: Iterable[_T], predicate: Callable[[_T], bool]
) -> tuple[list[_T], list[_T]]:
    """Partitions the iterable into two lists based on the predicate."""
    true_list: list[_T] = []
    false_list: list[_T] = []
    for item in iterable:
        (true_list if predicate(item) else false_list).append(item)
    return true_list, false_list


@pipette
def group_by(iterable: Iterable[_T], key_fn: Callable[[_T], _U]) -> dict[_U, list[_T]]:
    """Groups the iterable by the key function."""
    grouped: dict[_U, list[_T]] = {}
    for item in iterable:
        key = key_fn(item)
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(item)
    return grouped


@pipette
def flatten(iterable: Iterable[_T | Iterable[_T]]) -> Iterable[_T]:
    """Flattens a nested iterable into a single iterable."""
    for item in iterable:
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            yield from item
        else:
            yield cast(_T, item)


@pipette
def interleave(*iterables: Iterable[_T]) -> Iterable[_T]:
    """Interleaves elements from multiple iterables."""
    iterators = [iter(it) for it in iterables]
    while iterators:
        for it in list(iterators):
            try:
                yield next(it)
            except StopIteration:
                iterators.remove(it)


@pipette
def intersperse(iterable: Iterable[_T], separator: _T) -> Iterable[_T]:
    """Inserts a separator between each element of the iterable."""
    it = iter(iterable)
    try:
        yield next(it)
    except StopIteration:
        return
    for item in it:
        yield separator
        yield item


@pipette
def repeat(iterable: Iterable[_T], times: int) -> Iterable[_T]:
    """Repeats each element of the iterable a specified number of times."""
    for item in iterable:
        for _ in range(times):
            yield item


## Accessing elements and counts


@pipette
def first(iterable: Iterable[_T]) -> _T | None:
    """Returns the first element of the iterable, or None if empty."""
    return next(iter(iterable), None)


@pipette
def last(iterable: Iterable[_T]) -> _T | None:
    """Returns the last element of the iterable, or None if empty."""
    result = None
    for result in iterable:
        pass
    return result


@pipette
def count(iterable: Iterable[_T]) -> int:
    """Counts the number of elements in the iterable."""
    return sum(1 for _ in iterable)


@pipette
def length(iterable: Iterable[_T]) -> int:
    """Returns the length of the iterable."""
    return len(tuple(iterable))


## Generators


@pipette
def traverse(
    iterable: Iterable[_T | Iterable[_T]],
) -> Generator[_T, None, None | int]:
    """Recursively traverses nested iterables and yields all elements."""
    for arg in iterable:
        if isinstance(arg, Iterable) and not isinstance(arg, (str, bytes)):
            yield from arg | traverse  # pyright: ignore[reportReturnType]
        else:
            yield arg  # pyright: ignore[reportReturnType]


@pipette
def repeat_forever(iterable: Iterable[_T]) -> Generator[_T, None, None]:
    """Repeats the iterable indefinitely."""
    continue_iter = itertools.cycle(iterable)
    while True:
        yield next(continue_iter)


@pipette
def rep(iterable: Iterable[_T], times: int) -> Generator[_T, None, None]:
    """Repeats the iterable a specified number of times."""
    for _ in range(times):
        yield from iterable
