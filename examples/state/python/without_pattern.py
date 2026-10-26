from dataclasses import dataclass
from enum import StrEnum


class State(StrEnum):
    A = "a"
    B = "b"


@dataclass
class Context:
    state: State = State.A

    def call(self) -> int:
        match self.state:
            case State.A:
                self.state = State.B
                return 1
            case State.B:
                self.state = State.A
                return 2


if __name__ == "__main__":
    print(Context().call())
