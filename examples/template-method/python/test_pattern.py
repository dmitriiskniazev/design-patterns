from template import A, B
from without_pattern import call
from without_pattern_extended import call as extended


def test_fixed_outer_step_and_equivalence() -> None:
    assert A().call(2) == call(2) == 3
    assert B().call(2) == extended(2) == 5
    assert B().step(2) == 4
