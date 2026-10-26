from typing import Protocol


class Implementation(Protocol):
    def operation(self, value: int) -> int: ...


class ImplementationA:
    def operation(self, value: int) -> int:
        return value


class ImplementationB:
    def operation(self, value: int) -> int:
        return value * 2
