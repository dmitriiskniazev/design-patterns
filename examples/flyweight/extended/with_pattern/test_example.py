from factory import PairFactory
from state import Context


def test_intrinsic_state_and_context_independence() -> None:
    factory = PairFactory()
    first, second = Context(0, factory.get(1, 2)), Context(2, factory.get(1, 2))
    assert first.shared is second.shared
    assert first.state != second.state
    assert first.shared.value == 1
    assert factory.get(1, 2) is not factory.get(1, 3)
    assert factory.get(1, 2).variant == 2
