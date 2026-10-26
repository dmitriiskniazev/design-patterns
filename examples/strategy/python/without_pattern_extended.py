from enum import StrEnum


class Choice(StrEnum):
    A = "a"
    B = "b"


def call(value: int, choice: Choice) -> int:
    match choice:
        case Choice.A:
            return value + 1
        case Choice.B:
            return value * 2


if __name__ == "__main__":
    print(call(2, Choice.B))
