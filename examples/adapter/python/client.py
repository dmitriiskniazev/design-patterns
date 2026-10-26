from adapter import Target


def call(target: Target, value: int) -> int:
    return target.operation(value)
