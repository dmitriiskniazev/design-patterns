from collections.abc import Iterator
from dataclasses import dataclass


@dataclass(frozen=True)
class Collection:
    values: tuple[int, ...]

    def __iter__(self) -> Iterator[int]:
        return iter(self.values)


def reverse(collection: Collection) -> Iterator[int]:
    return reversed(collection.values)
