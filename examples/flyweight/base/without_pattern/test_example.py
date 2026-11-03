from main import create


def test_intrinsic_state_and_context_independence() -> None:
    first, second = create(0, 1), create(2, 1)
    assert first.shared == second.shared
    assert first.shared is not second.shared
    assert first.state != second.state
