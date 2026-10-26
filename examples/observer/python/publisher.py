from collections.abc import Callable
from dataclasses import dataclass, field

type Callback = Callable[[int], int]


@dataclass
class Publisher:
    callbacks: list[Callback] = field(default_factory=list)

    def subscribe(self, callback: Callback) -> None:
        self.callbacks.append(callback)

    def notify(self, value: int) -> list[int]:
        return [callback(value) for callback in self.callbacks]
