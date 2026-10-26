from nodes import A, B
from plain_nodes import A as PlainA
from plain_nodes import B as PlainB
from visitor import DoubleVisitor, ValueVisitor
from without_pattern import call
from without_pattern_extended import call as extended


def test_operations_and_equivalence() -> None:
    node, plain = B(B(A(3))), PlainB(PlainB(PlainA(3)))
    assert node.accept(ValueVisitor()) == call(plain) == 5
    assert node.accept(DoubleVisitor()) == extended(plain) == 6
    assert not hasattr(plain, "accept")
