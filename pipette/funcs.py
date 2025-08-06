import builtins
import functools
import itertools
from collections.abc import Generator, Iterable
from typing import Callable, Protocol, TypeVar, runtime_checkable

from .pipette import pipette

## Protocols and TypeVars


@runtime_checkable
class SupportsLessThan(Protocol):
    def __lt__(self, other: object) -> bool: ...


_T = TypeVar("_T")
_U = TypeVar("_U")
_COMPARABLE = TypeVar("_COMPARABLE", bound=SupportsLessThan)

## Core Functional Operations


@pipette
def select(iterable: Iterable[_T], selector: Callable[[_T], _U]) -> Iterable[_U]:
    return builtins.map(selector, iterable)


@pipette
def where(iterable: Iterable[_T], predicate: Callable[[_T], bool]) -> Iterable[_T]:
    return builtins.filter(predicate, iterable)


@pipette
def into(iterable: Iterable[_T], typ: Callable[[Iterable[_T]], _U]) -> _U:
    return typ(iterable)


## Iterable slicing and limiting


@pipette
def take(iterable: Iterable[_T], n: int) -> Iterable[_T]:
    return itertools.islice(iterable, n)


@pipette
def skip(iterable: Iterable[_T], n: int) -> Iterable[_T]:
    return itertools.islice(iterable, n, None)


## Reducing and uniqueness


@pipette
def reduce(
    iterable: Iterable[_T], func: Callable[[_T, _T], _T], initial: _T | None = None
) -> _T:
    if initial is not None:
        return functools.reduce(func, iterable, initial)
    return functools.reduce(func, iterable)


@pipette
def distinct(iterable: Iterable[_T]) -> Iterable[_T]:
    seen: set[_T] = set()
    return (x for x in iterable if x not in seen and not seen.add(x))


## Sorting and chunking


@pipette
def sort_by(
    iterable: Iterable[_T], key_fn: Callable[[_T], _COMPARABLE]
) -> Iterable[_T]:
    return sorted(iterable, key=key_fn)


@pipette
def chunk(iterable: Iterable[_T], size: int) -> Iterable[list[_T]]:
    it = iter(iterable)
    while chunk := list(itertools.islice(it, size)):
        yield chunk


## Accessing elements and counts


@pipette
def first(iterable: Iterable[_T]) -> _T | None:
    return next(iter(iterable), None)


@pipette
def last(iterable: Iterable[_T]) -> _T | None:
    result = None
    for result in iterable:
        pass
    return result


@pipette
def count(iterable: Iterable[_T]) -> int:
    return sum(1 for _ in iterable)


@pipette
def length(iterable: Iterable[_T]) -> int:
    return len(tuple(iterable))


@pipette
def traverse(
    iterable: Iterable[_T | Iterable[_T]],
) -> Generator[_T, None, None | int]:
    for arg in iterable:
        if isinstance(arg, Iterable) and not isinstance(arg, (str, bytes)):
            yield from arg | traverse  # pyright: ignore[reportReturnType]
        else:
            yield arg  # pyright: ignore[reportReturnType]
