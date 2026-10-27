from main import create


def test_intrinsic_state_and_context_independence() -> None:
    first, second = create(0, 1, 2), create(2, 1, 2)
    assert first.shared == second.shared
    assert first.shared is not second.shared
    assert first.state != second.state
    assert create(0, 1, 2).shared != create(0, 1, 3).shared
