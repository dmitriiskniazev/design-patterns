from callbacks import double, increment
from publisher import Publisher

if __name__ == "__main__":
    publisher = Publisher()
    publisher.subscribe(increment)
    publisher.subscribe(double)
    print(publisher.notify(2))
