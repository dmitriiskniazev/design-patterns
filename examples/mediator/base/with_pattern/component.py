from dataclasses import dataclass


@dataclass
class Component:
    value: int = 0

    def receive(self, value: int) -> None:
        self.value = value
