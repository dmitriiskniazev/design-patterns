from client import Client
from provider import ValueProvider


def test_provider_selection() -> None:
    assert Client(ValueProvider(1)).operation() == 2
    assert Client(ValueProvider(5)).operation() == 6
