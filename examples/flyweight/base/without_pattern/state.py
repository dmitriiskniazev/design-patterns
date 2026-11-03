from dataclasses import dataclass


@dataclass(frozen=True)
class Shared:
    value: int


@dataclass(frozen=True)
class Context:
    state: int
    shared: Shared
