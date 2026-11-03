from main import notify


def test_ordered_notifications() -> None:
    assert notify(2) == [3]
