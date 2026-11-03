from factory import Factory
from state import Context

if __name__ == "__main__":
    factory = Factory()
    print(Context(0, factory.get(1)), Context(2, factory.get(1)))
