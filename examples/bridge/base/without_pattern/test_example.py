from main import operation


def test_common_step_and_variable_implementation() -> None:
    assert operation(2) == 3
    assert operation(5) == 6
