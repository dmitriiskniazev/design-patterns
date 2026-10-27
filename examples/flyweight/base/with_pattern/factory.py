from dataclasses import dataclass, field

from state import Shared


@dataclass
class Factory:
    cache: dict[int, Shared] = field(default_factory=dict)

    def get(self, value: int) -> Shared:
        if value not in self.cache:
            self.cache[value] = Shared(value)
        return self.cache[value]
