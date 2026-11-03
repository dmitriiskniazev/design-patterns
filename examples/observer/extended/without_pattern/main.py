from callbacks import double, increment


def notify(value: int) -> list[int]:
    return [increment(value), double(value)]


if __name__ == "__main__":
    print(notify(2))
