from context import Context
from strategy import double, increment
from without_pattern import call
from without_pattern_extended import Choice
from without_pattern_extended import call as extended


def test_replacement_and_equivalence() -> None:
    context = Context(increment)
    assert context.call(2) == call(2) == 3
    assert extended(2, Choice.A) == context.call(2)
    context.operation = double
    assert context.call(2) == extended(2, Choice.B) == 4
