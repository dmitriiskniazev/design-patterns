from cached_proxy import CachedProxy
from subject import RealSubject

if __name__ == "__main__":
    proxy = CachedProxy(RealSubject())
    print(proxy.operation(), proxy.operation())
