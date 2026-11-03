from main import Choice, operation


def test_common_step_and_variable_implementation() -> None:
    assert operation(Choice.A, 2) == 3
    assert operation(Choice.B, 2) == 5
