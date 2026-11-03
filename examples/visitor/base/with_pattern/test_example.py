from nodes import A, B
from visitor import ValueVisitor


def test_nested_nodes_and_operation() -> None:
    node = B(B(A(3)))
    assert node.accept(ValueVisitor()) == 5
