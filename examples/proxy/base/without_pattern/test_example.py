from main import operation
from subject import RealSubject


def test_cache_hits_and_call_count() -> None:
    real = RealSubject()
    cache: list[int] = []
    assert [operation(real, cache) for _ in range(2)] == [1, 1]
    assert real.calls == 1
