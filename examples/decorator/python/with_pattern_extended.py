from component import Value
from decorators import DoubleDecorator, IncrementDecorator

if __name__ == "__main__":
    print(
        DoubleDecorator(IncrementDecorator(Value(1))).operation(),
        IncrementDecorator(DoubleDecorator(Value(1))).operation(),
    )
