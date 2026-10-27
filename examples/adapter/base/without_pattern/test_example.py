from main import operation


def test_interface_delegates_input() -> None:
    assert operation(2) == 3
    assert operation(4) == 5
