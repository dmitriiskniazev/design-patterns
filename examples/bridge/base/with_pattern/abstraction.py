from dataclasses import dataclass

from implementation import Implementation


@dataclass
class Abstraction:
    implementation: Implementation

    def operation(self, value: int) -> int:
        return self.implementation.operation(value) + 1
