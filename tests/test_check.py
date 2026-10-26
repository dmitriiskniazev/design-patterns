from pathlib import Path
from types import SimpleNamespace

import pytest

from design_patterns.check import check


def test_discovers_topics_in_separate_processes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for name in ("new-topic", "adapter"):
        (tmp_path / "examples" / name / "python").mkdir(parents=True)
    calls: list[list[str]] = []

    def run(command: list[str], **kwargs: object) -> SimpleNamespace:
        calls.append(command)
        assert kwargs["cwd"] == tmp_path
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr("design_patterns.check.subprocess.run", run)
    assert check(tmp_path) == 0
    paths = [Path(command[-1]).relative_to(tmp_path).as_posix() for command in calls]
    assert paths == [
        "tests",
        "examples/adapter/python",
        "examples/new-topic/python",
    ]


def test_stops_on_failure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "examples/adapter/python").mkdir(parents=True)
    calls: list[list[str]] = []

    def run(command: list[str], **kwargs: object) -> SimpleNamespace:
        calls.append(command)
        return SimpleNamespace(returncode=2)

    monkeypatch.setattr("design_patterns.check.subprocess.run", run)
    assert check(tmp_path) == 2
    assert len(calls) == 1
