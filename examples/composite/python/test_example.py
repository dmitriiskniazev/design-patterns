from component import Composite, Leaf, RepeatedComponent
from without_pattern import operation
from without_pattern_extended import operation as extended


def test_nested_components_and_new_kind() -> None:
    assert (
        operation([1, [2]])
        == Composite([Leaf(1), Composite([Leaf(2)])]).operation()
        == 3
    )
    assert (
        extended([1, ([2],)])
        == Composite([Leaf(1), RepeatedComponent(Composite([Leaf(2)]))]).operation()
        == 5
    )
