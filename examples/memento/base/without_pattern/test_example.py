from main import restore, save
from originator import Originator


def test_snapshot_survives_mutation() -> None:
    originator = Originator(1)
    snapshot = save(originator)
    originator.value = 2
    restore(originator, snapshot)
    assert originator.value == 1
