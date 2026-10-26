from expression import Literal, Sum
from without_pattern import evaluate
from without_pattern_extended import evaluate as extended


def test_tree_nodes_compose_recursively() -> None:
    assert Literal(1).evaluate() == evaluate(1)
    pair = Sum(Literal(1), Literal(2))
    assert pair.evaluate() == extended((1, 2)) == 3
    assert Sum(pair, Literal(3)).evaluate() == extended(((1, 2), 3)) == 6
