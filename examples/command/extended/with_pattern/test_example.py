from command import Double, Increment
from invoker import Invoker
from receiver import Receiver


def test_repeated_execution_and_lifo_undo() -> None:
    receiver = Receiver(2)
    invoker = Invoker()
    increment = Increment(receiver)
    double = Double(receiver)
    for command in (increment, double, increment, double):
        invoker.run(command)
    assert receiver.value == 14
    for expected in (7, 6, 3, 2):
        invoker.undo()
        assert receiver.value == expected
