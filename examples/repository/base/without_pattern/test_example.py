from main import operation


def test_representation_independent_result() -> None:
    assert operation({1: 2}, 1) == 3
