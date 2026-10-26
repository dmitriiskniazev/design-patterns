from enum import StrEnum


class Order(StrEnum):
    INCREMENT_FIRST = "increment_first"
    DOUBLE_FIRST = "double_first"


def operation(value: int, order: Order) -> int:
    match order:
        case Order.INCREMENT_FIRST:
            return (value + 1) * 2
        case Order.DOUBLE_FIRST:
            return value * 2 + 1


if __name__ == "__main__":
    print(operation(1, Order.INCREMENT_FIRST), operation(1, Order.DOUBLE_FIRST))
