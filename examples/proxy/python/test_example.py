from cached_proxy import CachedProxy
from counting_proxy import CountingProxy
from subject import RealSubject
from without_pattern import operation
from without_pattern_extended import operation as extended


def test_cache_and_count_keep_result() -> None:
    before, real = RealSubject(), RealSubject()
    proxy = CachedProxy(real)
    cache: list[int] = []
    assert (
        [operation(before, cache) for _ in range(2)]
        == [proxy.operation() for _ in range(2)]
        == [1, 1]
    )
    assert before.calls == real.calls == 1
    counter, calls = CountingProxy(proxy), [0]
    assert [extended(before, cache, calls) for _ in range(2)] == [
        counter.operation() for _ in range(2)
    ]
    assert counter.calls == calls[0] == 2
