from component import Component
from mediator import Mediator
from without_pattern import notify
from without_pattern_extended import notify as extended


def test_shared_routing_and_equivalence() -> None:
    sender, first, second, plain = Component(), Component(), Component(), Component()
    Mediator([sender, first]).notify(sender, 1)
    notify(plain, 1)
    assert first.value == plain.value == 1
    assert sender.value == 0
    a, b = Component(), Component()
    Mediator([sender, first, second]).notify(sender, 2)
    extended(a, b, 2)
    assert (first.value, second.value) == (a.value, b.value) == (2, 2)
