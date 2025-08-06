from collections.abc import Iterable
from pipette import where, into, select, distinct, sort_by, take, pipette, traverse
from dataclasses import dataclass


@dataclass
class Item:
    id: int
    value: int
    active: bool


@pipette
def first(iterable: Iterable[int]) -> int | None:
    return next(iter(iterable), None)


def main():
    print([1, 2, 3] | where(lambda x: x % 2 == 0) | into(tuple))

    data = [
        Item(id=1, value=50, active=True),
        Item(id=2, value=20, active=False),
        Item(id=3, value=50, active=True),
        Item(id=4, value=10, active=True),
        Item(id=5, value=90, active=False),
        Item(id=6, value=90, active=True),
        Item(id=7, value=20, active=True),
        Item(id=8, value=60, active=True),
        Item(id=9, value=90, active=True),
        Item(id=10, value=30, active=True),
        Item(id=11, value=40, active=True),
        Item(id=12, value=40, active=True),
    ]

    result = (
        (
            data
            | where(lambda x: x.active)
            | select(lambda x: x.value)
            | distinct
            | sort_by(lambda x: -x)
            | take(10)
        )
        | into(list[float])
        | first
    )
    print(result)

    abc = [1, [2, 3], 4, [5, [6, 7]], 8]
    print(abc | traverse | into(list[int]))


if __name__ == "__main__":
    main()
