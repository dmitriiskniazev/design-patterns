from context import Context
from strategy import double, increment


def test_operation_replacement() -> None:
    context = Context(increment)
    assert context.call(2) == 3
    context.operation = double
    assert context.call(2) == 4
