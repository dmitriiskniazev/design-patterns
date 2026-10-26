from instance import Instance


def operation() -> tuple[int, int]:
    shared = Instance()
    return shared.operation(), shared.operation()


if __name__ == "__main__":
    print(operation())
