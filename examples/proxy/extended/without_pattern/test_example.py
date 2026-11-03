from main import operation
from subject import RealSubject


def test_cache_hits_and_call_count() -> None:
    real = RealSubject()
    cache: list[int] = []
    calls = [0]
    assert [operation(real, cache, calls) for _ in range(2)] == [1, 1]
    assert real.calls == 1
    assert calls == [2]
