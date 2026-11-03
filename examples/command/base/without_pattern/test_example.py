from main import Invoker
from receiver import Receiver


def test_repeated_execution_and_lifo_undo() -> None:
    receiver = Receiver(2)
    invoker = Invoker(receiver)
    invoker.run()
    invoker.run()
    assert receiver.value == 4
    for expected in (3, 2):
        invoker.undo()
        assert receiver.value == expected
