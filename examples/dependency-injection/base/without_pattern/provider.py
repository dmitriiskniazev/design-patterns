from dataclasses import dataclass


@dataclass
class ValueProvider:
    value: int

    def get(self) -> int:
        return self.value
