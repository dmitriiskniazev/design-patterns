from component import Value
from decorators import DoubleDecorator, IncrementDecorator


def test_operation_order() -> None:
    assert IncrementDecorator(Value(1)).operation() == 2
    assert DoubleDecorator(IncrementDecorator(Value(1))).operation() == 4
    assert IncrementDecorator(DoubleDecorator(Value(1))).operation() == 3
