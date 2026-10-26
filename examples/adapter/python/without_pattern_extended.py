from enum import StrEnum

from adaptee import Adaptee, SecondAdaptee


class Choice(StrEnum):
    A = "a"
    B = "b"


def operation(choice: Choice, value: int) -> int:
    match choice:
        case Choice.A:
            return Adaptee().specific_operation(value)
        case Choice.B:
            return SecondAdaptee().different_operation(value)


if __name__ == "__main__":
    print(operation(Choice.B, 2))
