from prototype import Prototype


def test_clone_is_independent_and_preserves_runtime_state() -> None:
    original = Prototype(["X", "Y"])
    clone = original.clone()
    assert clone.parts == ["X", "Y"]
    clone.parts.append("B")
    assert clone.parts == ["X", "Y", "B"]
    assert original.parts == ["X", "Y"]
    original.parts.append("Z")
    assert clone.parts == ["X", "Y", "B"]
    assert original.clone().parts == ["X", "Y", "Z"]
