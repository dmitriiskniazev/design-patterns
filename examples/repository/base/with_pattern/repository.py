from dataclasses import dataclass
from typing import Protocol


class Repository(Protocol):
    def get(self, key: int) -> int: ...


@dataclass
class DictRepository:
    values: dict[int, int]

    def get(self, key: int) -> int:
        return self.values[key]
