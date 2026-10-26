from handler import Handler
from operations import first, second
from without_pattern import call
from without_pattern_extended import call as extended


def test_first_result_stops_chain_and_equivalence() -> None:
    assert Handler(first).call(1) == call(1) == 1
    chain = Handler(first, Handler(second))
    assert (
        [chain.call(v) for v in (1, 2, 3)]
        == [extended(v) for v in (1, 2, 3)]
        == [1, 2, None]
    )
    calls: list[int] = []

    def later(value: int) -> int:
        calls.append(value)
        return 9

    assert Handler(first, Handler(later)).call(1) == 1
    assert calls == []
