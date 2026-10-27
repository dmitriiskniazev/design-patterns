from nodes import A, B


class ValueVisitor:
    def a(self, node: A) -> int:
        return node.value

    def b(self, node: B) -> int:
        return node.child.accept(self) + 1
