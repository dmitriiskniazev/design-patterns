from baseline.context import Context
from baseline.operations import Add, Constant, Multiply


def main() -> None:
    values = [1, 2, 3]
    context = Context(operation=Add(amount=2))
    print(context.apply_all(values))
    context.operation = Multiply(factor=4)
    print(context.apply_all(values))
    context.operation = Constant(value=7)
    print(context.apply_all(values))


if __name__ == "__main__":
    main()
