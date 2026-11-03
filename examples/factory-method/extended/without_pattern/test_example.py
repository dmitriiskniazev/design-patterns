from main import Kind, operation


def test_creation_and_shared_algorithm() -> None:
    assert operation(Kind.A) == "A"
    assert operation(Kind.B) == "B"
