from subsystems import SubsystemA, SubsystemB, SubsystemC


def client_a() -> int:
    return SubsystemC().operation(SubsystemB().operation(SubsystemA().operation(1)))


def client_b() -> int:
    return SubsystemC().operation(SubsystemB().operation(SubsystemA().operation(2)))


if __name__ == "__main__":
    print(client_a(), client_b())
