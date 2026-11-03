from clients import client_a, client_b
from facade import Facade

if __name__ == "__main__":
    print(client_a(Facade()), client_b(Facade()))
