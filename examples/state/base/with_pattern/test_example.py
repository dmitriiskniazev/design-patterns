from context import Context
from states import A


def test_state_transitions() -> None:
    context = Context(A())
    assert [context.call() for _ in range(3)] == [1, 2, 1]
