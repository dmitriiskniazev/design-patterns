from handler import Handler
from operations import first


def test_first_result_stops_processing() -> None:
    assert [Handler(first).call(v) for v in (1, 2)] == [1, None]
    calls: list[int] = []

    def later(value: int) -> int:
        calls.append(value)
        return 9

    assert Handler(first, Handler(later)).call(1) == 1
    assert calls == []
