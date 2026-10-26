from client import operation
from factory import FactoryA, FactoryB
from without_pattern import operation as direct
from without_pattern_extended import Kind
from without_pattern_extended import operation as extended


def test_same_client_accepts_a_complete_other_family() -> None:
    assert direct() == operation(FactoryA()) == ("A1", "A2")
    assert extended(Kind.B) == operation(FactoryB()) == ("B1", "B2")
    assert extended(Kind.A) == operation(FactoryA())
