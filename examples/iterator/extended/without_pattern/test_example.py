from main import call


def test_traversal_and_independence() -> None:
    assert call((1, 2)) == [2, 1]
    assert call(()) == []
