from builder import Builder


def test_independent_immutable_snapshots() -> None:
    builder = Builder()
    builder.add("A")
    first = builder.build()
    builder.add("B")
    assert first.parts == ("A",)
    assert builder.build().parts == ("A", "B")
    assert Builder().build().parts == ()
