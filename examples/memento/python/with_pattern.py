from caretaker import Caretaker
from originator import Originator

if __name__ == "__main__":
    originator = Originator(1)
    caretaker = Caretaker(originator.save())
    originator.value = 2
    originator.restore(caretaker.snapshot)
    print(originator.value)
