from dataclasses import dataclass


@dataclass(frozen=True)
class Add:
    amount: int


@dataclass(frozen=True)
class Multiply:
    factor: int


@dataclass(frozen=True)
class Constant:
    value: int
