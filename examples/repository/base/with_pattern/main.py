from client import operation
from repository import DictRepository

if __name__ == "__main__":
    print(operation(DictRepository({1: 2}), 1))
