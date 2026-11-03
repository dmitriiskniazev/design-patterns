from dataclasses import dataclass

from states import State


@dataclass
class Context:
    state: State

    def call(self) -> int:
        return self.state.call(self)
