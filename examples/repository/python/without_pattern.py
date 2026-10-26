def operation(values: dict[int, int], key: int) -> int:
    return values[key] + 1


if __name__ == "__main__":
    print(operation({1: 2}, 1))
