from main import call
from nodes import A, B


def test_nested_nodes_and_operation() -> None:
    node = B(B(A(3)))
    assert call(node) == 5
    assert not hasattr(node, "accept")
