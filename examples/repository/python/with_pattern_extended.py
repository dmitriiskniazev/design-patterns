from client import operation
from repository import ListRepository

if __name__ == "__main__":
    print(operation(ListRepository([(1, 2)]), 1))
