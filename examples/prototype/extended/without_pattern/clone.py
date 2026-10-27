from value import Value


def operation(original: Value) -> Value:
    return Value(original.parts.copy())
