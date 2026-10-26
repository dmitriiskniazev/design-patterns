from context import Context
from strategy import double

if __name__ == "__main__":
    print(Context(double).call(2))
