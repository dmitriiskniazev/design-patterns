from typing import Protocol


class ContextLike(Protocol):
    state: State


class State(Protocol):
    def call(self, context: ContextLike) -> int: ...


class A:
    def call(self, context: ContextLike) -> int:
        context.state = B()
        return 1


class B:
    def call(self, context: ContextLike) -> int:
        context.state = A()
        return 2


class C:
    def call(self, context: ContextLike) -> int:
        context.state = A()
        return 3
