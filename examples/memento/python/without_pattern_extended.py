from plain_extended_originator import Originator


def save(originator: Originator) -> tuple[int, bool]:
    return originator.value, originator.flag


def restore(originator: Originator, snapshot: tuple[int, bool]) -> None:
    originator.value, originator.flag = snapshot


if __name__ == "__main__":
    originator = Originator(1, False)
    snapshot = save(originator)
    originator.value, originator.flag = 2, True
    restore(originator, snapshot)
    print(originator.value, originator.flag)
