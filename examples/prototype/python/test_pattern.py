from prototype import Prototype
from value import Value
from without_pattern import operation
from without_pattern_extended import operation as extended


def test_clone_preserves_runtime_state_and_copies_mutable_parts() -> None:
    original, plain = Prototype(["X", "Y"]), Value(["X", "Y"])
    clone, direct = original.clone(), operation(plain)
    assert clone.parts == direct.parts == ["X", "Y"]
    clone.parts.append("B")
    direct.parts.append("B")
    assert clone.parts == direct.parts == extended(plain).parts
    assert original.parts == plain.parts == ["X", "Y"]
    original.parts.append("Z")
    plain.parts.append("Z")
    assert original.clone().parts == operation(plain).parts == ["X", "Y", "Z"]
    assert clone.parts == direct.parts == ["X", "Y", "B"]
