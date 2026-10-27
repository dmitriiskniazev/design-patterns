from component import Value
from decorators import IncrementDecorator


def test_operation_order() -> None:
    assert IncrementDecorator(Value(1)).operation() == 2
    assert IncrementDecorator(Value(5)).operation() == 6
