from factory import PairFactory
from state import Context

if __name__ == "__main__":
    factory = PairFactory()
    print(Context(0, factory.get(1, 2)), Context(2, factory.get(1, 2)))
