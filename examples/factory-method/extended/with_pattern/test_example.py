from creator import CreatorA, CreatorB
from product import ProductA, ProductB


def test_creation_and_shared_algorithm() -> None:
    assert type(CreatorA().create()) is ProductA
    assert CreatorA().operation() == "A"
    assert type(CreatorB().create()) is ProductB
    assert CreatorB().operation() == "B"
    assert CreatorA.operation is CreatorB.operation
