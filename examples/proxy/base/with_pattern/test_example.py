from cached_proxy import CachedProxy
from subject import RealSubject


def test_cache_hits_and_call_count() -> None:
    real = RealSubject()
    proxy = CachedProxy(real)
    assert [proxy.operation() for _ in range(2)] == [1, 1]
    assert real.calls == 1
