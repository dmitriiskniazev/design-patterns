from subject import RealSubject
from without_pattern import operation as cached_operation


def operation(subject: RealSubject, cache: list[int], calls: list[int]) -> int:
    calls[0] += 1
    return cached_operation(subject, cache)


if __name__ == "__main__":
    subject, cache, calls = RealSubject(), [], [0]
    print(operation(subject, cache, calls), operation(subject, cache, calls))
