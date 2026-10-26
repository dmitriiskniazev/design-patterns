from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class Context:
    operation: Callable[[int], int]

    def call(self, value: int) -> int:
        return self.operation(value)
