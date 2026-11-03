from main import operation


def test_nested_composition() -> None:
    assert operation([]) == 0
    assert operation([1, [2]]) == 3
