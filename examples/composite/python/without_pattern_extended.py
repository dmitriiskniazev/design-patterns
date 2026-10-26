type Node = int | list[Node] | tuple[Node]


def operation(node: Node) -> int:
    match node:
        case int():
            return node
        case list():
            return sum(operation(child) for child in node)
        case (child,):
            return operation(child) * 2


if __name__ == "__main__":
    print(operation([1, ([2],)]))
