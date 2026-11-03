from callbacks import double, increment
from publisher import Publisher


def test_ordered_notifications() -> None:
    publisher = Publisher()
    assert publisher.notify(2) == []
    publisher.subscribe(increment)
    assert publisher.notify(2) == [3]
    publisher.subscribe(double)
    assert publisher.notify(2) == [3, 4]
