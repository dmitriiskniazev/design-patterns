from client import operation
from factory import FactoryA, FactoryB


def test_consistent_product_family() -> None:
    assert operation(FactoryA()) == ("A1", "A2")
    assert operation(FactoryB()) == ("B1", "B2")
