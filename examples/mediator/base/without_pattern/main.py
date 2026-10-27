from component import Component


def notify(receiver: Component, value: int) -> None:
    receiver.receive(value)


if __name__ == "__main__":
    receiver = Component()
    notify(receiver, 1)
    print(receiver.value)
