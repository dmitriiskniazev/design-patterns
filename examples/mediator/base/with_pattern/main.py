from component import Component
from mediator import Mediator

if __name__ == "__main__":
    sender, receiver = Component(), Component()
    Mediator([sender, receiver]).notify(sender, 1)
    print(receiver.value)
