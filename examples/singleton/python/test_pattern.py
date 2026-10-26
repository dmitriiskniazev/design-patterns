from instance import Instance
from singleton import Singleton
from without_pattern import operation
from without_pattern_extended import operation as extended


def test_repeated_construction_preserves_shared_state() -> None:
    shared = Singleton()
    start = shared.value
    assert Singleton() is shared
    assert Singleton().operation() == start + operation()
    assert Singleton().operation() == start + extended()[1]
    assert Instance().operation() == Instance().operation() == 1
