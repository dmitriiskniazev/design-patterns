import pytest

from baseline import operations
from baseline.context import Context as BaselineContext
from pattern import strategies
from pattern.context import Context as PatternContext
from pattern.interfaces import Strategy


@pytest.mark.parametrize(
    ("operation", "strategy", "expected"),
    [
        (operations.Add(2), strategies.Add(2), [3, 0, 2, 5]),
        (operations.Add(10), strategies.Add(10), [11, 8, 10, 13]),
        (operations.Multiply(4), strategies.Multiply(4), [4, -8, 0, 12]),
        (operations.Multiply(-2), strategies.Multiply(-2), [-2, 4, 0, -6]),
        (operations.Constant(7), strategies.Constant(7), [7, 7, 7, 7]),
        (operations.Constant(-3), strategies.Constant(-3), [-3, -3, -3, -3]),
    ],
)
def test_same_results_and_unchanged_input(
    operation: operations.Add | operations.Multiply | operations.Constant,
    strategy: Strategy,
    expected: list[int],
) -> None:
    values = [1, -2, 0, 3]
    for context in (BaselineContext(operation), PatternContext(strategy)):
        assert context.apply_all(values) == expected
        assert context.apply_all([]) == []
        assert values == [1, -2, 0, 3]


def test_baseline_can_replace_operation() -> None:
    context = BaselineContext(operations.Add(2))
    assert context.apply_all([1, 2, 3]) == [3, 4, 5]
    context.operation = operations.Multiply(4)
    assert context.apply_all([1, 2, 3]) == [4, 8, 12]
    context.operation = operations.Constant(7)
    assert context.apply_all([1, 2, 3]) == [7, 7, 7]


def test_pattern_can_replace_strategy() -> None:
    context = PatternContext(strategies.Add(2))
    assert context.apply_all([1, 2, 3]) == [3, 4, 5]
    context.strategy = strategies.Multiply(4)
    assert context.apply_all([1, 2, 3]) == [4, 8, 12]
    context.strategy = strategies.Constant(7)
    assert context.apply_all([1, 2, 3]) == [7, 7, 7]


def test_context_accepts_an_external_strategy_without_inheritance() -> None:
    class Negate:
        def apply(self, value: int) -> int:
            return -value

    context = PatternContext(Negate())
    assert context.apply_all([1, -2, 0, 3]) == [-1, 2, 0, -3]
