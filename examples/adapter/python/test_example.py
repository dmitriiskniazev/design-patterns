from adaptee import Adaptee, SecondAdaptee
from adapter import Adapter, SecondAdapter
from client import call
from without_pattern import operation
from without_pattern_extended import Choice
from without_pattern_extended import operation as extended


def test_both_interfaces() -> None:
    assert operation(2) == call(Adapter(Adaptee()), 2) == 3
    assert extended(Choice.A, 2) == call(Adapter(Adaptee()), 2)
    assert extended(Choice.B, 2) == call(SecondAdapter(SecondAdaptee()), 2) == 4
