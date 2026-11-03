from subsystems import SubsystemA, SubsystemB


def client_a() -> int:
    return SubsystemB().operation(SubsystemA().operation(1))


def client_b() -> int:
    return SubsystemB().operation(SubsystemA().operation(2))


if __name__ == "__main__":
    print(client_a(), client_b())
