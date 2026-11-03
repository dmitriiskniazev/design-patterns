from value import Value


def operation(original: Value) -> Value:
    return Value(original.parts.copy())


if __name__ == "__main__":
    print(operation(Value(["A"])).parts)
