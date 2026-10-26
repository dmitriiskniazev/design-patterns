from caretaker import Caretaker
from extended_originator import Originator

if __name__ == "__main__":
    originator = Originator(1, False)
    caretaker = Caretaker(originator.save())
    originator.value, originator.flag = 2, True
    originator.restore(caretaker.snapshot)
    print(originator.value, originator.flag)
