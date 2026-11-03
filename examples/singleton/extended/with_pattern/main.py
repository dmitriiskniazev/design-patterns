from singleton import Singleton

if __name__ == "__main__":
    first = Singleton().operation()
    second = Singleton().operation()
    print((first, second))
