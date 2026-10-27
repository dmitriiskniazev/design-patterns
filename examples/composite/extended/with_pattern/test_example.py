from component import Composite, Leaf, RepeatedComponent


def test_nested_composition() -> None:
    assert Composite([]).operation() == 0
    assert Composite([Leaf(1), Composite([Leaf(2)])]).operation() == 3
    assert (
        Composite([Leaf(1), RepeatedComponent(Composite([Leaf(2)]))]).operation() == 5
    )
