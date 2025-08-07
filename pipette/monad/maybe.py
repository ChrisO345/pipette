from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Callable, cast, final
from typing_extensions import override

T = TypeVar("T")
U = TypeVar("U")


class Maybe(Generic[T], ABC):
    @abstractmethod
    def map(self, func: Callable[[T], U]) -> "Maybe[U]":
        raise NotImplementedError

    @abstractmethod
    def bind(self, func: Callable[[T], "Maybe[U]"]) -> "Maybe[U]":
        raise NotImplementedError

    def __rshift__(self, fn: Callable[[T], "Maybe[U]"]) -> "Maybe[U]":
        """Alias for bind: monadic chaining with >>."""
        return self.bind(fn)

    def __or__(self, func: Callable[[T], U]) -> "Maybe[U]":
        """Alias for map, allowing transformation of the value."""
        return self.map(func)

    @abstractmethod
    def get_or_else(self, default: U) -> T | U:
        raise NotImplementedError


@final
class Some(Maybe[T]):
    def __init__(self, value: T):
        self.value = value

    @override
    def map(self, func: Callable[[T], U]) -> "Maybe[U]":
        return Some(func(self.value))

    @override
    def bind(self, func: Callable[[T], Maybe[U]]) -> Maybe[U]:
        return func(self.value)

    @override
    def get_or_else(self, default: U) -> T | U:
        return self.value

    @override
    def __repr__(self) -> str:
        return f"Some({self.value})"


class Nothing(Maybe[T]):
    @override
    def map(self, func: Callable[[T], U]) -> "Maybe[U]":
        return cast(Maybe[U], self)

    @override
    def bind(self, func: Callable[[T], Maybe[U]]) -> "Maybe[U]":
        return cast(Maybe[U], self)

    @override
    def get_or_else(self, default: U) -> T | U:
        return default

    @override
    def __repr__(self) -> str:
        return "Nothing"
