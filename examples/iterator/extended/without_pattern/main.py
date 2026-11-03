def call(values: tuple[int, ...]) -> list[int]:
    return list(reversed(values))


if __name__ == "__main__":
    print(call((1, 2)))
