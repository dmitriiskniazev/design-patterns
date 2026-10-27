from main import call


def test_operation_replacement() -> None:
    assert call(2) == 3
    assert call(5) == 6
