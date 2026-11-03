from abstraction import Abstraction
from implementation import ImplementationA


def test_common_step_and_variable_implementation() -> None:
    assert Abstraction(ImplementationA()).operation(2) == 3
    assert Abstraction(ImplementationA()).operation(5) == 6
