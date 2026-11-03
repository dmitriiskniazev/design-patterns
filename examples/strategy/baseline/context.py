from dataclasses import dataclass

from baseline.operations import Add, Constant, Multiply


@dataclass
class Context:
    operation: Add | Multiply | Constant

    def apply_all(self, values: list[int]) -> list[int]:
        match self.operation:
            case Add(amount):
                return [value + amount for value in values]
            case Multiply(factor):
                return [value * factor for value in values]
            case Constant(value):
                return [value for _ in values]
