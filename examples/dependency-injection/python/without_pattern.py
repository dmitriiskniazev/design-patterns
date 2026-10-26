from provider import ValueProvider


def operation() -> int:
    return ValueProvider(1).get() + 1


if __name__ == "__main__":
    print(operation())
