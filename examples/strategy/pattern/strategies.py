from dataclasses import dataclass


@dataclass(frozen=True)
class Add:
    amount: int

    def apply(self, value: int) -> int:
        return value + self.amount


@dataclass(frozen=True)
class Multiply:
    factor: int

    def apply(self, value: int) -> int:
        return value * self.factor


@dataclass(frozen=True)
class Constant:
    value: int

    def apply(self, value: int) -> int:
        return self.value
