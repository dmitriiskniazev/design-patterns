from enum import StrEnum


class Choice(StrEnum):
    A = "a"
    B = "b"


def operation(choice: Choice, value: int) -> int:
    match choice:
        case Choice.A:
            return value + 1
        case Choice.B:
            return value * 2 + 1


if __name__ == "__main__":
    print(operation(Choice.B, 2))
