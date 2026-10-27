from component import Component
from mediator import Mediator


def test_recipient_routing() -> None:
    sender, first, second = Component(), Component(), Component()
    Mediator([sender, first]).notify(sender, 2)
    assert sender.value == 0
    assert first.value == 2
    assert second.value == 0
