from main import Choice, operation


def test_provider_selection() -> None:
    assert operation(Choice.VALUE) == 2
    assert operation(Choice.DOUBLE) == 3
