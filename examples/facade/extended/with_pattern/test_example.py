from clients import client_a, client_b
from facade import ExtendedFacade, Facade


def test_shared_sequence_for_both_clients() -> None:
    assert (client_a(Facade()), client_b(Facade())) == (4, 6)
    assert (client_a(ExtendedFacade()), client_b(ExtendedFacade())) == (3, 5)
