from main import Kind, operation


def test_consistent_product_family() -> None:
    assert operation(Kind.A) == ("A1", "A2")
    assert operation(Kind.B) == ("B1", "B2")
