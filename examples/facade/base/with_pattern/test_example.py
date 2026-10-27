from clients import client_a, client_b
from facade import Facade


def test_shared_sequence_for_both_clients() -> None:
    assert (client_a(Facade()), client_b(Facade())) == (4, 6)
