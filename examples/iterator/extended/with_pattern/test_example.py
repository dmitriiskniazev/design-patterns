from collection import Collection, reverse


def test_traversal_and_independence() -> None:
    collection = Collection((1, 2))
    assert list(collection) == [1, 2]
    first, second = iter(collection), iter(collection)
    assert (next(first), next(first), next(second)) == (1, 2, 1)
    assert list(reverse(collection)) == [2, 1]
