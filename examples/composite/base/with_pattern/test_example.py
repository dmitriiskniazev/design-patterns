from component import Composite, Leaf


def test_nested_composition() -> None:
    assert Composite([]).operation() == 0
    assert Composite([Leaf(1), Composite([Leaf(2)])]).operation() == 3
