from abstraction import Abstraction
from implementation import ImplementationA, ImplementationB


def test_common_step_and_variable_implementation() -> None:
    assert Abstraction(ImplementationA()).operation(2) == 3
    assert Abstraction(ImplementationB()).operation(2) == 5
