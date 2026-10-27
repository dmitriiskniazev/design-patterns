from product import Product


def operation() -> tuple[str, str]:
    return Product("A1").operation(), Product("A2").operation()


if __name__ == "__main__":
    print(operation())
