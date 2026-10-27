from dataclasses import dataclass


@dataclass(frozen=True)
class A:
    value: int


@dataclass(frozen=True)
class B:
    child: Node


type Node = A | B
