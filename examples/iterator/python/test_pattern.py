from collection import Collection, reverse
from without_pattern import call
from without_pattern_extended import call as extended


def test_independent_iterators_and_equivalence() -> None:
    collection = Collection((1, 2))
    assert list(collection) == call((1, 2)) == [1, 2]
    assert list(reverse(collection)) == extended((1, 2)) == [2, 1]
    first, second = iter(collection), iter(collection)
    assert (next(first), next(first), next(second)) == (1, 2, 1)
