from dataclasses import dataclass
from typing import Protocol


class Repository(Protocol):
    def get(self, key: int) -> int: ...


@dataclass
class DictRepository:
    values: dict[int, int]

    def get(self, key: int) -> int:
        return self.values[key]


@dataclass
class ListRepository:
    values: list[tuple[int, int]]

    def get(self, key: int) -> int:
        return next(value for stored_key, value in self.values if stored_key == key)
