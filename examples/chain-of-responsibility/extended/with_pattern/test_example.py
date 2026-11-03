from handler import Handler
from operations import first, second


def test_first_result_stops_processing() -> None:
    chain = Handler(first, Handler(second))
    assert [chain.call(v) for v in (1, 2, 3)] == [1, 2, None]
    calls: list[int] = []

    def later(value: int) -> int:
        calls.append(value)
        return 9

    assert Handler(first, Handler(later)).call(1) == 1
    assert calls == []
