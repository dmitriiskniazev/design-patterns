from context import Context
from states import A, C


def test_state_transitions() -> None:
    context = Context(A())
    assert [context.call() for _ in range(3)] == [1, 2, 1]
    context = Context(C())
    assert [context.call() for _ in range(3)] == [3, 1, 2]
