from state import Context, Shared


def create(state: int, value: int) -> Context:
    return Context(state, Shared(value))


if __name__ == "__main__":
    print(create(0, 1), create(2, 1))
