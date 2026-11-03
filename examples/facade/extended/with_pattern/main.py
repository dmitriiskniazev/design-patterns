from clients import client_a, client_b
from facade import ExtendedFacade

if __name__ == "__main__":
    print(client_a(ExtendedFacade()), client_b(ExtendedFacade()))
