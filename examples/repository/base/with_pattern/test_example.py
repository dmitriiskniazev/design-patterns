from client import operation
from repository import DictRepository


def test_representation_independent_result() -> None:
    assert operation(DictRepository({1: 2}), 1) == 3
