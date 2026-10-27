from cached_proxy import CachedProxy
from counting_proxy import CountingProxy
from subject import RealSubject

if __name__ == "__main__":
    proxy = CountingProxy(CachedProxy(RealSubject()))
    print(proxy.operation(), proxy.operation())
