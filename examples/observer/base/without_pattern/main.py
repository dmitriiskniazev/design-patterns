from callbacks import increment


def notify(value: int) -> list[int]:
    return [increment(value)]


if __name__ == "__main__":
    print(notify(2))
