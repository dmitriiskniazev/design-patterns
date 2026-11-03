from main import operation
from value import Value


def test_clone_is_independent_and_preserves_runtime_state() -> None:
    original = Value(["X", "Y"])
    clone = operation(original)

    assert clone.parts == ["X", "Y", "B"]
    assert original.parts == ["X", "Y"]
    original.parts.append("Z")
    assert clone.parts == ["X", "Y", "B"]
    assert operation(original).parts == ["X", "Y", "Z", "B"]
