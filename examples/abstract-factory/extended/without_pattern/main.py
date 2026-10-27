from enum import StrEnum

from product import Product


class Kind(StrEnum):
    A = "A"
    B = "B"


def operation(kind: Kind) -> tuple[str, str]:
    match kind:
        case Kind.A:
            first, second = Product("A1"), Product("A2")
        case Kind.B:
            first, second = Product("B1"), Product("B2")
    return first.operation(), second.operation()


if __name__ == "__main__":
    print(operation(Kind.B))
