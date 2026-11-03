from pattern.context import Context
from pattern.strategies import Add, Constant, Multiply


def main() -> None:
    values = [1, 2, 3]
    context = Context(strategy=Add(amount=2))
    print(context.apply_all(values))
    context.strategy = Multiply(factor=4)
    print(context.apply_all(values))
    context.strategy = Constant(value=7)
    print(context.apply_all(values))


if __name__ == "__main__":
    main()
