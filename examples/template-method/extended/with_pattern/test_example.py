from template import A, B


def test_fixed_final_step() -> None:
    assert A().call(2) == 3
    assert B().step(2) == 4
    assert B().call(2) == 5
    assert A.call is B.call
