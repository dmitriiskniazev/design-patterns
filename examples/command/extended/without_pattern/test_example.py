from main import Choice, Invoker
from receiver import Receiver


def test_repeated_execution_and_lifo_undo() -> None:
    receiver = Receiver(2)
    invoker = Invoker(receiver)
    for choice in (Choice.A, Choice.B, Choice.A, Choice.B):
        invoker.run(choice)
    assert receiver.value == 14
    for expected in (7, 6, 3, 2):
        invoker.undo()
        assert receiver.value == expected
