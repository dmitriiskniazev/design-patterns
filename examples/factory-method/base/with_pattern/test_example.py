from creator import CreatorA
from product import ProductA


def test_creation_and_shared_algorithm() -> None:
    assert type(CreatorA().create()) is ProductA
    assert CreatorA().operation() == "A"
