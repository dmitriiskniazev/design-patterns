from main import Order, operation


def test_operation_order() -> None:
    assert operation(1, Order.INCREMENT_FIRST) == 4
    assert operation(1, Order.DOUBLE_FIRST) == 3
