from value import Value
from without_pattern import operation as clone


def operation(original: Value) -> Value:
    result = clone(original)
    result.parts.append("B")
    return result


if __name__ == "__main__":
    print(operation(Value(["A"])).parts)
