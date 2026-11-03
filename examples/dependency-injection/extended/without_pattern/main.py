from enum import StrEnum

from provider import ValueProvider


class Choice(StrEnum):
    VALUE = "value"
    DOUBLE = "double"


def operation(choice: Choice) -> int:
    match choice:
        case Choice.VALUE:
            return ValueProvider(1).get() + 1
        case Choice.DOUBLE:
            return ValueProvider(1).get() * 2 + 1


if __name__ == "__main__":
    print(operation(Choice.DOUBLE))
