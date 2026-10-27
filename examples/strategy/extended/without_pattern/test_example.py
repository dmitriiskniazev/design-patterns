from main import Choice, call


def test_operation_replacement() -> None:
    assert call(2, Choice.A) == 3
    assert call(2, Choice.B) == 4
