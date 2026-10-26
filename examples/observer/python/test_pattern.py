from callbacks import double, increment
from publisher import Publisher
from without_pattern import notify
from without_pattern_extended import notify as extended


def test_subscription_and_equivalence() -> None:
    publisher = Publisher()
    publisher.subscribe(increment)
    assert publisher.notify(2) == notify(2) == [3]
    publisher.subscribe(double)
    assert publisher.notify(2) == extended(2) == [3, 4]
    assert Publisher().notify(2) == []
