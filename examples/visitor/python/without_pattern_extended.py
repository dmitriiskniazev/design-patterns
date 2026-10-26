from plain_nodes import A, B, Node


def call(node: Node) -> int:
    match node:
        case A(value):
            return value * 2
        case B(child):
            return call(child)


if __name__ == "__main__":
    print(call(B(A(2))))
