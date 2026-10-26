from state import Context, Shared


def create(state: int, value: int, variant: int) -> Context:
    return Context(state, Shared(value, variant))


if __name__ == "__main__":
    print(create(0, 1, 2), create(2, 1, 2))
