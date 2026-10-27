from adaptee import SecondAdaptee
from adapter import SecondAdapter
from client import call

if __name__ == "__main__":
    print(call(SecondAdapter(SecondAdaptee()), 2))
