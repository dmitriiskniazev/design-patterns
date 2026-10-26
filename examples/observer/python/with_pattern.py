from callbacks import increment
from publisher import Publisher

if __name__ == "__main__":
    publisher = Publisher()
    publisher.subscribe(increment)
    print(publisher.notify(2))
