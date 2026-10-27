from main import client_a, client_b


def test_shared_sequence_for_both_clients() -> None:
    assert (client_a(), client_b()) == (3, 5)
