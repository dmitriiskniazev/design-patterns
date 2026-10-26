from caretaker import Caretaker
from extended_originator import Originator as Extended
from originator import Originator
from plain_extended_originator import Originator as PlainExtended
from plain_originator import Originator as Plain
from without_pattern import restore, save
from without_pattern_extended import restore as restore_extended
from without_pattern_extended import save as save_extended


def test_opaque_snapshot_and_equivalence() -> None:
    originator, plain = Originator(1), Plain(1)
    caretaker, snapshot = Caretaker(originator.save()), save(plain)
    originator.value = plain.value = 2
    originator.restore(caretaker.snapshot)
    restore(plain, snapshot)
    assert originator.value == plain.value == 1
    originator, plain = Extended(1, False), PlainExtended(1, False)
    caretaker, snapshot = Caretaker(originator.save()), save_extended(plain)
    originator.value, originator.flag = 2, True
    plain.value, plain.flag = 2, True
    originator.restore(caretaker.snapshot)
    restore_extended(plain, snapshot)
    assert (
        (originator.value, originator.flag) == (plain.value, plain.flag) == (1, False)
    )
