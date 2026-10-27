from product import ProductA


def operation() -> str:
    return ProductA().operation()


if __name__ == "__main__":
    print(operation())
