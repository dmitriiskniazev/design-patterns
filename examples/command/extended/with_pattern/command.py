from dataclasses import dataclass, field
from typing import Protocol

from receiver import Receiver


class Command(Protocol):
    def execute(self) -> None: ...
    def undo(self) -> None: ...


@dataclass
class Increment:
    receiver: Receiver
    history: list[int] = field(default_factory=list, init=False)

    def execute(self) -> None:
        self.history.append(self.receiver.value)
        self.receiver.value += 1

    def undo(self) -> None:
        self.receiver.value = self.history.pop()


@dataclass
class Double:
    receiver: Receiver
    history: list[int] = field(default_factory=list, init=False)

    def execute(self) -> None:
        self.history.append(self.receiver.value)
        self.receiver.value *= 2

    def undo(self) -> None:
        self.receiver.value = self.history.pop()
