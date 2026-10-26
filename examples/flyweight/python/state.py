from dataclasses import dataclass


@dataclass(frozen=True)
class Shared:
    value: int
    variant: int = 0


@dataclass(frozen=True)
class Context:
    state: int
    shared: Shared
