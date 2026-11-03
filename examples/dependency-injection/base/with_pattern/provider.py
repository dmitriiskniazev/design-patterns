from dataclasses import dataclass
from typing import Protocol


class Provider(Protocol):
    def get(self) -> int: ...


@dataclass
class ValueProvider:
    value: int

    def get(self) -> int:
        return self.value
