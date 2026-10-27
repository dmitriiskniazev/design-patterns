from main import operation


def test_provider_selection() -> None:
    assert operation() == 2
