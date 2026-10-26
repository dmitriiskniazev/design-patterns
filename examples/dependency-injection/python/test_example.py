from client import Client
from provider import DoubleProvider, ValueProvider
from without_pattern import operation
from without_pattern_extended import Choice
from without_pattern_extended import operation as extended


def test_dependency_selected_outside_client() -> None:
    assert operation() == Client(ValueProvider(1)).operation() == 2
    assert extended(Choice.VALUE) == Client(ValueProvider(1)).operation()
    assert (
        extended(Choice.DOUBLE)
        == Client(DoubleProvider(ValueProvider(1))).operation()
        == 3
    )
    assert Client(ValueProvider(5)).operation() == 6
