from facade import Facade


def client_a(facade: Facade) -> int:
    return facade.operation(1)


def client_b(facade: Facade) -> int:
    return facade.operation(2)
