from dataclasses import dataclass
from typing import Protocol


class Visitor[T](Protocol):
    def a(self, node: A) -> T: ...
    def b(self, node: B) -> T: ...


class Node(Protocol):
    def accept[T](self, visitor: Visitor[T]) -> T: ...


@dataclass(frozen=True)
class A:
    value: int

    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.a(self)


@dataclass(frozen=True)
class B:
    child: Node

    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.b(self)
