from product import Product


def operation() -> Product:
    return Product(("A",))


if __name__ == "__main__":
    print(operation().parts)
