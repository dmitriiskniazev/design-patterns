from dataclasses import dataclass

from pattern.interfaces import Strategy


@dataclass
class Context:
    strategy: Strategy

    def apply_all(self, values: list[int]) -> list[int]:
        return [self.strategy.apply(value) for value in values]
