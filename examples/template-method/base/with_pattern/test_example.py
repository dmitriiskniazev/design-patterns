from template import A


def test_fixed_final_step() -> None:
    assert A().call(2) == 3
