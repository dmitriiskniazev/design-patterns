from expression import Literal


def test_recursive_expression() -> None:
    assert Literal(7).evaluate() == 7
