from client import Client
from provider import ValueProvider

if __name__ == "__main__":
    print(Client(ValueProvider(1)).operation())
