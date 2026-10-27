from subject import RealSubject


def operation(subject: RealSubject, cache: list[int]) -> int:
    if not cache:
        cache.append(subject.operation())
    return cache[0]
