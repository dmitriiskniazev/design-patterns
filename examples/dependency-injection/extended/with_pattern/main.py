from client import Client
from provider import DoubleProvider, ValueProvider

if __name__ == "__main__":
    print(Client(DoubleProvider(ValueProvider(1))).operation())
