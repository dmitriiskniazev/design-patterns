from caretaker import Caretaker
from originator import Originator


def test_snapshot_survives_mutation() -> None:
    originator = Originator(1, False)
    caretaker = Caretaker(originator.save())
    originator.value = 2
    originator.flag = True
    originator.restore(caretaker.snapshot)
    assert originator.value == 1
    assert originator.flag is False
