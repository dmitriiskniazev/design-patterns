from abstraction import Abstraction
from implementation import ImplementationA

if __name__ == "__main__":
    print(Abstraction(ImplementationA()).operation(2))
