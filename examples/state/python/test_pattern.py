from context import Context
from states import A, C
from without_pattern import Context as Plain
from without_pattern_extended import Context as Extended
from without_pattern_extended import State


def test_transition_and_equivalence() -> None:
    context, plain = Context(A()), Plain()
    assert (
        [context.call(), context.call(), context.call()]
        == [plain.call(), plain.call(), plain.call()]
        == [1, 2, 1]
    )
    context, plain = Context(C()), Extended(State.C)
    assert [context.call(), context.call()] == [plain.call(), plain.call()] == [3, 1]
