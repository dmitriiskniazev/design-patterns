from client import operation
from repository import DictRepository, ListRepository
from without_pattern import operation as before
from without_pattern_extended import Storage
from without_pattern_extended import operation as extended


def test_client_is_independent_from_representation() -> None:
    assert before({1: 2}, 1) == operation(DictRepository({1: 2}), 1) == 3
    assert extended(Storage.DICT, 1, {1: 2}, []) == operation(DictRepository({1: 2}), 1)
    assert (
        extended(Storage.LIST, 1, {}, [(1, 2)])
        == operation(ListRepository([(1, 2)]), 1)
        == 3
    )
