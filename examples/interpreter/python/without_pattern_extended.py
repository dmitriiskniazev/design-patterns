type Node = int | tuple[Node, Node]


def evaluate(node: Node) -> int:
    match node:
        case int():
            return node
        case (left, right):
            return evaluate(left) + evaluate(right)


if __name__ == "__main__":
    print(evaluate((1, 2)))
