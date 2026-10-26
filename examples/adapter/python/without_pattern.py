from adaptee import Adaptee


def operation(value: int) -> int:
    return Adaptee().specific_operation(value)


if __name__ == "__main__":
    print(operation(2))
