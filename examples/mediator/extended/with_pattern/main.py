from component import Component
from mediator import Mediator

if __name__ == "__main__":
    sender, first, second = Component(), Component(), Component()
    Mediator([sender, first, second]).notify(sender, 1)
    print(first.value, second.value)
