from dataclasses import dataclass
from typing import Protocol


class Expression(Protocol):
    def evaluate(self) -> int: ...


@dataclass(frozen=True)
class Literal:
    value: int

    def evaluate(self) -> int:
        return self.value


@dataclass(frozen=True)
class Sum:
    left: Expression
    right: Expression

    def evaluate(self) -> int:
        return self.left.evaluate() + self.right.evaluate()
