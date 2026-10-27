from dataclasses import dataclass
from typing import Protocol


class Component(Protocol):
    def operation(self) -> int: ...


@dataclass
class Value:
    value: int

    def operation(self) -> int:
        return self.value
