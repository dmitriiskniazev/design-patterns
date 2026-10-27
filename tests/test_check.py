from pathlib import Path
from types import SimpleNamespace

import pytest

from design_patterns.check import check


def variant(root: Path, topic: str, stage: str, approach: str) -> Path:
    directory = root / "examples" / topic / stage / approach
    directory.mkdir(parents=True)
    (directory / "test_example.py").touch()
    return directory


def test_discovers_variants_in_separate_processes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    expected = [
        variant(tmp_path, name, stage, approach)
        for name in ("adapter", "new-topic")
        for stage in ("base", "extended")
        for approach in ("with_pattern", "without_pattern")
    ]
    calls = []

    def run(command: list[str], **kwargs: object) -> SimpleNamespace:
        calls.append(Path(command[-1]))
        assert kwargs["cwd"] == tmp_path
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr("design_patterns.check.subprocess.run", run)
    assert check(tmp_path) == 0
    assert calls == [tmp_path / "tests", *expected]


def test_topic_filter_runs_only_its_variants(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    selected = variant(tmp_path, "adapter", "base", "with_pattern")
    variant(tmp_path, "strategy", "base", "with_pattern")
    calls = []

    def run(command: list[str], **kwargs: object) -> SimpleNamespace:
        calls.append(Path(command[-1]))
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr("design_patterns.check.subprocess.run", run)
    assert check(tmp_path, "adapter") == 0
    assert calls == [selected]


def test_stops_on_failure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    variant(tmp_path, "adapter", "base", "with_pattern")
    calls = []

    def run(command: list[str], **kwargs: object) -> SimpleNamespace:
        calls.append(command)
        return SimpleNamespace(returncode=2)

    monkeypatch.setattr("design_patterns.check.subprocess.run", run)
    assert check(tmp_path) == 2
    assert len(calls) == 1


def test_unknown_topic_is_not_a_successful_empty_run(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="No example variants"):
        check(tmp_path, "missing")
