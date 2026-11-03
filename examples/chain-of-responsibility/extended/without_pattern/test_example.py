from main import call


def test_first_result_stops_processing() -> None:
    assert [call(v) for v in (1, 2, 3)] == [1, 2, None]
