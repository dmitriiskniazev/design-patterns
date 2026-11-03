from nodes import A, B, Node


def call(node: Node) -> int:
    match node:
        case A(value):
            return value
        case B(child):
            return call(child) + 1


def double_call(node: Node) -> int:
    match node:
        case A(value):
            return value * 2
        case B(child):
            return double_call(child)


if __name__ == "__main__":
    print(double_call(B(A(2))))
