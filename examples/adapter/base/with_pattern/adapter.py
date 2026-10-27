from dataclasses import dataclass
from typing import Protocol

from adaptee import Adaptee


class Target(Protocol):
    def operation(self, value: int) -> int: ...


@dataclass
class Adapter:
    adaptee: Adaptee

    def operation(self, value: int) -> int:
        return self.adaptee.specific_operation(value)
