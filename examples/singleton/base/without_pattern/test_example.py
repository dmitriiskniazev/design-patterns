from main import operation


def test_explicit_shared_instance_per_call() -> None:
    assert operation() == 1
    assert operation() == 1
