from main import call


def test_fixed_final_step() -> None:
    assert call(2) == 3
