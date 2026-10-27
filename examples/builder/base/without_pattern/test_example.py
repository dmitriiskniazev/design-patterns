from dataclasses import FrozenInstanceError

import pytest
from main import operation


def test_independent_immutable_products() -> None:
    first = operation()
    assert first.parts == ("A",)
    assert operation() is not first
    with pytest.raises(FrozenInstanceError):
        first.parts = ()
