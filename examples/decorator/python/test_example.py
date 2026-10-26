from component import Value
from decorators import DoubleDecorator, IncrementDecorator
from without_pattern import operation
from without_pattern_extended import Order
from without_pattern_extended import operation as extended


def test_order_and_same_interface() -> None:
    assert operation(1) == IncrementDecorator(Value(1)).operation() == 2
    assert (
        extended(1, Order.INCREMENT_FIRST)
        == DoubleDecorator(IncrementDecorator(Value(1))).operation()
        == 4
    )
    assert (
        extended(1, Order.DOUBLE_FIRST)
        == IncrementDecorator(DoubleDecorator(Value(1))).operation()
        == 3
    )
