from handler import Handler
from operations import first, second

if __name__ == "__main__":
    chain = Handler(first, Handler(second))
    print(chain.call(2))
