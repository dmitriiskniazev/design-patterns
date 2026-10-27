from dataclasses import dataclass, field

from state import Shared


@dataclass
class Factory:
    cache: dict[int, Shared] = field(default_factory=dict)

    def get(self, value: int) -> Shared:
        if value not in self.cache:
            self.cache[value] = Shared(value)
        return self.cache[value]


@dataclass
class PairFactory:
    cache: dict[tuple[int, int], Shared] = field(default_factory=dict)

    def get(self, value: int, variant: int) -> Shared:
        key = (value, variant)
        if key not in self.cache:
            self.cache[key] = Shared(value, variant)
        return self.cache[key]
