from factory import Factory
from state import Context


def test_intrinsic_state_and_context_independence() -> None:
    factory = Factory()
    first, second = Context(0, factory.get(1)), Context(2, factory.get(1))
    assert first.shared is second.shared
    assert first.state != second.state
    assert first.shared.value == 1
