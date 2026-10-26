from dataclasses import dataclass
from enum import StrEnum


class State(StrEnum):
    A = "a"
    B = "b"
    C = "c"


@dataclass
class Context:
    state: State = State.A

    def call(self) -> int:
        match self.state:
            case State.A:
                self.state = State.B
                return 1
            case State.B | State.C:
                result = 2 if self.state is State.B else 3
                self.state = State.A
                return result


if __name__ == "__main__":
    print(Context(State.C).call())
