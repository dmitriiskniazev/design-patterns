from typing import Protocol

from product import Product


class Factory(Protocol):
    def first(self) -> Product: ...
    def second(self) -> Product: ...


class FactoryA:
    def first(self) -> Product:
        return Product("A1")

    def second(self) -> Product:
        return Product("A2")
