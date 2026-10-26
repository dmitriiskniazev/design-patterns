from factory import Factory, PairFactory
from state import Context
from without_pattern import create
from without_pattern_extended import create as extended


def test_equal_values_share_only_intrinsic_state() -> None:
    factory = Factory()
    first, second = Context(0, factory.get(1)), Context(2, factory.get(1))
    assert (first, second) == (create(0, 1), create(2, 1))
    assert first.shared is second.shared
    assert first.state != second.state
    pairs = PairFactory()
    assert Context(0, pairs.get(1, 2)) == extended(0, 1, 2)
    assert pairs.get(1, 2) is pairs.get(1, 2)
    assert pairs.get(1, 2) is not pairs.get(1, 3)
