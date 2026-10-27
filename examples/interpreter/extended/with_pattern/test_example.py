from expression import Literal, Sum


def test_recursive_expression() -> None:
    assert Literal(7).evaluate() == 7
    pair = Sum(Literal(1), Literal(2))
    assert pair.evaluate() == 3
    assert Sum(pair, Literal(3)).evaluate() == 6
