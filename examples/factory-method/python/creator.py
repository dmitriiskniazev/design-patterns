from abc import ABC, abstractmethod

from product import Product, ProductA, ProductB


class Creator(ABC):
    def operation(self) -> str:
        return self.create().operation()

    @abstractmethod
    def create(self) -> Product: ...


class CreatorA(Creator):
    def create(self) -> Product:
        return ProductA()


class CreatorB(Creator):
    def create(self) -> Product:
        return ProductB()
