from typing import Protocol


class Product(Protocol):
    def operation(self) -> str: ...


class ProductA:
    def operation(self) -> str:
        return "A"


class ProductB:
    def operation(self) -> str:
        return "B"
