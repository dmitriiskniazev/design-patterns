from abc import ABC, abstractmethod


class Template(ABC):
    def call(self, value: int) -> int:
        return self.step(value) + 1

    @abstractmethod
    def step(self, value: int) -> int: ...


class A(Template):
    def step(self, value: int) -> int:
        return value


class B(Template):
    def step(self, value: int) -> int:
        return value * 2
