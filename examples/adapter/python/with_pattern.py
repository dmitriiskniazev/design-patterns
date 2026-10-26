from adaptee import Adaptee
from adapter import Adapter
from client import call

if __name__ == "__main__":
    print(call(Adapter(Adaptee()), 2))
