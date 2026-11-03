from component import Component
from main import notify


def test_recipient_routing() -> None:
    first, second = Component(), Component()
    notify(first, second, 2)
    assert first.value == 2
    assert second.value == 2
