from client import operation
from factory import FactoryA


def test_consistent_product_family() -> None:
    assert operation(FactoryA()) == ("A1", "A2")
