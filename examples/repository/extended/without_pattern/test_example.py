from main import Storage, operation


def test_representation_independent_result() -> None:
    assert operation(Storage.DICT, 1, {1: 2}, []) == 3
    assert operation(Storage.LIST, 1, {}, [(1, 2)]) == 3
