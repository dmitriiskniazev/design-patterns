from plain_nodes import A, B, Node


def call(node: Node) -> int:
    match node:
        case A(value):
            return value
        case B(child):
            return call(child) + 1


if __name__ == "__main__":
    print(call(B(A(2))))
