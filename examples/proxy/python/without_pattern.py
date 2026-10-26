from subject import RealSubject


def operation(subject: RealSubject, cache: list[int]) -> int:
    if not cache:
        cache.append(subject.operation())
    return cache[0]


if __name__ == "__main__":
    subject, cache = RealSubject(), []
    print(operation(subject, cache), operation(subject, cache))
