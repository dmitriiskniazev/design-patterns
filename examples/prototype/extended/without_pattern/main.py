from clone import operation as clone
from value import Value


def operation(original: Value) -> Value:
    result = clone(original)
    result.parts.append("B")
    return result


if __name__ == "__main__":
    print(operation(Value(["A"])).parts)
