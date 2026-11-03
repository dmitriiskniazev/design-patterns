from adaptee import Adaptee, SecondAdaptee
from adapter import Adapter, SecondAdapter
from client import call


def test_interface_delegates_input() -> None:
    assert call(Adapter(Adaptee()), 2) == 3
    assert call(Adapter(Adaptee()), 4) == 5
    assert call(SecondAdapter(SecondAdaptee()), 2) == 4
    assert call(SecondAdapter(SecondAdaptee()), 4) == 8
