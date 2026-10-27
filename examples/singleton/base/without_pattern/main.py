from instance import Instance


def operation() -> int:
    shared = Instance()
    return shared.operation()


if __name__ == "__main__":
    print(operation())
