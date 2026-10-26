from dataclasses import dataclass

from component import Component


@dataclass
class IncrementDecorator:
    inner: Component

    def operation(self) -> int:
        return self.inner.operation() + 1


@dataclass
class DoubleDecorator:
    inner: Component

    def operation(self) -> int:
        return self.inner.operation() * 2
