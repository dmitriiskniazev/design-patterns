import without_pattern as before
import without_pattern_extended as extended
from clients import client_a, client_b
from facade import ExtendedFacade, Facade


def test_clients_keep_the_same_entrypoint() -> None:
    assert (
        (before.client_a(), before.client_b())
        == (client_a(Facade()), client_b(Facade()))
        == (4, 6)
    )
    assert (
        (extended.client_a(), extended.client_b())
        == (client_a(ExtendedFacade()), client_b(ExtendedFacade()))
        == (3, 5)
    )
