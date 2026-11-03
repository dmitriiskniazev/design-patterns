from typing import Protocol


class Strategy(Protocol):
    def apply(self, value: int) -> int: ...
