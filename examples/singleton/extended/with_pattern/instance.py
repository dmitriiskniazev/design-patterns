from dataclasses import dataclass


@dataclass
class Instance:
    value: int = 0

    def operation(self) -> int:
        self.value += 1
        return self.value
