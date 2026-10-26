from abstraction import Abstraction
from implementation import ImplementationB

if __name__ == "__main__":
    print(Abstraction(ImplementationB()).operation(2))
