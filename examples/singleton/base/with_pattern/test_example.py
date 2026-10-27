from instance import Instance
from singleton import Singleton


def test_shared_identity_and_state() -> None:
    shared = Singleton()
    start = shared.value
    assert Singleton() is shared
    assert Singleton().operation() == start + 1
    assert Singleton().operation() == start + 2
    assert Instance().operation() == Instance().operation() == 1
