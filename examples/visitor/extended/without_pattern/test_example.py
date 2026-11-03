from main import call, double_call
from nodes import A, B


def test_nested_nodes_and_operation() -> None:
    node = B(B(A(3)))
    assert call(node) == 5
    assert double_call(node) == 6
    assert not hasattr(node, "accept")
