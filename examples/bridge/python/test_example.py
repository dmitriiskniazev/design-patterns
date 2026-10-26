from abstraction import Abstraction
from implementation import ImplementationA, ImplementationB
from without_pattern import operation
from without_pattern_extended import Choice
from without_pattern_extended import operation as extended


def test_implementation_changes_without_abstraction() -> None:
    assert operation(2) == Abstraction(ImplementationA()).operation(2) == 3
    assert extended(Choice.A, 2) == Abstraction(ImplementationA()).operation(2)
    assert extended(Choice.B, 2) == Abstraction(ImplementationB()).operation(2) == 5
