from plain_originator import Originator


def save(originator: Originator) -> int:
    return originator.value


def restore(originator: Originator, snapshot: int) -> None:
    originator.value = snapshot


if __name__ == "__main__":
    originator = Originator(1)
    snapshot = save(originator)
    originator.value = 2
    restore(originator, snapshot)
    print(originator.value)
