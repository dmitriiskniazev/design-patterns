from dataclasses import dataclass, field
from enum import StrEnum

from receiver import Receiver


class Choice(StrEnum):
    A = "a"
    B = "b"


@dataclass
class Invoker:
    receiver: Receiver
    history: list[int] = field(default_factory=list)

    def run(self, choice: Choice) -> None:
        self.history.append(self.receiver.value)
        match choice:
            case Choice.A:
                self.receiver.value += 1
            case Choice.B:
                self.receiver.value *= 2

    def undo(self) -> None:
        self.receiver.value = self.history.pop()


if __name__ == "__main__":
    receiver = Receiver(2)
    Invoker(receiver).run(Choice.B)
    print(receiver.value)
