from main import Choice, operation


def test_interface_delegates_input() -> None:
    assert operation(Choice.A, 2) == 3
    assert operation(Choice.B, 2) == 4
    assert operation(Choice.B, 4) == 8
