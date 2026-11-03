from component import Value
from decorators import IncrementDecorator

if __name__ == "__main__":
    print(IncrementDecorator(Value(1)).operation())
