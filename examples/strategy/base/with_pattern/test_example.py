from context import Context
from strategy import increment


def test_operation_replacement() -> None:
    context = Context(increment)
    assert context.call(2) == 3
