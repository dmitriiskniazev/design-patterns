from command import Double, Increment
from invoker import Invoker
from receiver import Receiver
from without_pattern import Invoker as Plain
from without_pattern_extended import Choice
from without_pattern_extended import Invoker as Extended


def test_commands_undo_and_equivalence() -> None:
    receiver, other = Receiver(2), Receiver(2)
    invoker, plain = Invoker(), Plain(other)
    invoker.run(Increment(receiver))
    plain.run()
    assert receiver.value == other.value == 3
    invoker.undo()
    plain.undo()
    assert receiver.value == other.value == 2
    plain = Extended(other)
    invoker.run(Double(receiver))
    plain.run(Choice.B)
    assert receiver.value == other.value == 4
    invoker.undo()
    plain.undo()
    assert receiver.value == other.value == 2


def test_reused_commands_restore_every_execution_in_lifo_order() -> None:
    receiver, other = Receiver(2), Receiver(2)
    invoker, plain = Invoker(), Extended(other)
    increment, double = Increment(receiver), Double(receiver)
    for command, choice in (
        (increment, Choice.A),
        (double, Choice.B),
        (increment, Choice.A),
        (double, Choice.B),
    ):
        invoker.run(command)
        plain.run(choice)
        assert receiver.value == other.value
    for expected in (7, 6, 3, 2):
        invoker.undo()
        plain.undo()
        assert receiver.value == other.value == expected
