from typing import Callable, TypeVar, final, Generic
from typing_extensions import override

_T = TypeVar("_T")
_U = TypeVar("_U")
_V = TypeVar("_V")


@final
class Pipette(Generic[_T, _U]):
    def __init__(
        self, func: Callable[..., _U], *args: object, **kwargs: object
    ) -> None:
        self.args: tuple[object, ...] = args
        self.kwargs: dict[str, object] = kwargs
        self.func: Callable[..., _U] = func

    def __ror__(self, other: _T) -> _U:
        return self.func(other, *self.args, **self.kwargs)

    def __call__(self, *args: object, **kwargs: object) -> "Pipette[_T, _U]":
        return Pipette(
            self.func,
            *self.args,
            *args,
            **self.kwargs,
            **kwargs,
        )

    @override
    def __repr__(self) -> str:
        name = getattr(self.func, "__name__", self.func.__class__.__name__)
        return f"piped::<{name}>(*{self.args}, **{self.kwargs})"

    def __get__(self, instance: object, owner: type | None = None) -> "Pipette[_T, _U]":
        bound_func = self.func.__get__(instance, owner)  # type: ignore
        return Pipette(bound_func, *self.args, **self.kwargs)


def pipette(func: Callable[..., _U]) -> Pipette[object, _U]:
    return Pipette(func)
