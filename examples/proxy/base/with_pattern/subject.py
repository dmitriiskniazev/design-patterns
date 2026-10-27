from dataclasses import dataclass
from typing import Protocol


class Subject(Protocol):
    def operation(self) -> int: ...


@dataclass
class RealSubject:
    calls: int = 0

    def operation(self) -> int:
        self.calls += 1
        return 1
