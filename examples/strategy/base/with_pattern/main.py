from context import Context
from strategy import increment

if __name__ == "__main__":
    print(Context(increment).call(2))
