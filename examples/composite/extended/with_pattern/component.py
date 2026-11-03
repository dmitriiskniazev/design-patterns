from dataclasses import dataclass
from typing import Protocol


class Component(Protocol):
    def operation(self) -> int: ...


@dataclass
class Leaf:
    value: int

    def operation(self) -> int:
        return self.value


@dataclass
class Composite:
    children: list[Component]

    def operation(self) -> int:
        return sum(child.operation() for child in self.children)


@dataclass
class RepeatedComponent:
    component: Component

    def operation(self) -> int:
        return self.component.operation() * 2
