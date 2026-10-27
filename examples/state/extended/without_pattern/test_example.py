from main import Context, State


def test_state_transitions() -> None:
    context = Context()
    assert [context.call() for _ in range(3)] == [1, 2, 1]
    context = Context(State.C)
    assert [context.call() for _ in range(3)] == [3, 1, 2]
