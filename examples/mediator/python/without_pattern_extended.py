from component import Component


def notify(first: Component, second: Component, value: int) -> None:
    first.receive(value)
    second.receive(value)


if __name__ == "__main__":
    first, second = Component(), Component()
    notify(first, second, 1)
    print(first.value, second.value)
