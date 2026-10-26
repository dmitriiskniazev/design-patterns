from creator import CreatorA, CreatorB
from product import ProductA, ProductB
from without_pattern import operation
from without_pattern_extended import Kind
from without_pattern_extended import operation as extended


def test_creation_is_the_only_overridden_step() -> None:
    assert type(CreatorA().create()) is ProductA
    assert type(CreatorB().create()) is ProductB
    assert CreatorA.operation is CreatorB.operation
    assert operation() == CreatorA().operation() == "A"
    assert extended(Kind.A) == CreatorA().operation()
    assert extended(Kind.B) == CreatorB().operation() == "B"
