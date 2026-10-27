from adaptee import Adaptee
from adapter import Adapter
from client import call


def test_interface_delegates_input() -> None:
    assert call(Adapter(Adaptee()), 2) == 3
    assert call(Adapter(Adaptee()), 4) == 5
