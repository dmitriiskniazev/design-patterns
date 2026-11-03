from main import Context


def test_state_transitions() -> None:
    context = Context()
    assert [context.call() for _ in range(3)] == [1, 2, 1]
