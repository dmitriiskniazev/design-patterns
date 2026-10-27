from collections.abc import Callable
from dataclasses import dataclass

type Operation = Callable[[int], int | None]


@dataclass
class Handler:
    operation: Operation
    next: Handler | None = None

    def call(self, value: int) -> int | None:
        result = self.operation(value)
        if result is not None:
            return result
        return self.next.call(value) if self.next else None
