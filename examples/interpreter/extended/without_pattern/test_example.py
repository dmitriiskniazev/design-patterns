from main import evaluate


def test_recursive_expression() -> None:
    assert evaluate(7) == 7
    assert evaluate((1, 2)) == 3
    assert evaluate(((1, 2), 3)) == 6
