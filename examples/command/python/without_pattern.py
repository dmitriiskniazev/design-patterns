from dataclasses import dataclass, field

from receiver import Receiver


@dataclass
class Invoker:
    receiver: Receiver
    history: list[int] = field(default_factory=list)

    def run(self) -> None:
        self.history.append(self.receiver.value)
        self.receiver.value += 1

    def undo(self) -> None:
        self.receiver.value = self.history.pop()


if __name__ == "__main__":
    receiver = Receiver(2)
    Invoker(receiver).run()
    print(receiver.value)
