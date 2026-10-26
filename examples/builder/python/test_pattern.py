from builder import Builder
from without_pattern import operation
from without_pattern_extended import operation as extended


def test_build_creates_independent_immutable_snapshots() -> None:
    builder = Builder()
    builder.add("A")
    first = builder.build()
    assert first == operation()
    builder.add("B")
    assert builder.build() == extended()
    assert first.parts == ("A",)
    assert Builder().build().parts == ()
