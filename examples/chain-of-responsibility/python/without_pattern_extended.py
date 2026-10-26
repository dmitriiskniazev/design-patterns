def call(value: int) -> int | None:
    if value == 1:
        return 1
    return 2 if value == 2 else None


if __name__ == "__main__":
    print(call(2))
