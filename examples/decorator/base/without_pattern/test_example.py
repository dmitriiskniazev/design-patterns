from main import operation


def test_operation_order() -> None:
    assert operation(1) == 2
    assert operation(5) == 6
