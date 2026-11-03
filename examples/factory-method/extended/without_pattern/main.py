from enum import StrEnum

from product import ProductA, ProductB


class Kind(StrEnum):
    A = "A"
    B = "B"


def operation(kind: Kind) -> str:
    match kind:
        case Kind.A:
            return ProductA().operation()
        case Kind.B:
            return ProductB().operation()


if __name__ == "__main__":
    print(operation(Kind.B))
