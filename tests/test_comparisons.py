import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest

from design_patterns.comparisons import build_comparison


ROOT = Path(__file__).resolve().parents[1]
TOPICS = {
    topic["id"]: topic["fileComparison"]
    for topic in json.loads((ROOT / "content/topics.json").read_text())
    if isinstance(topic.get("fileComparison"), dict)
}
GROUPS = ("before", "after", "beforeExtension", "afterExtension")


def test_comparison_topics() -> None:
    ready = {
        topic["id"]
        for topic in json.loads((ROOT / "content/topics.json").read_text())
        if topic["ready"]
    }
    assert len(TOPICS) == 25
    assert set(TOPICS) == ready


@pytest.mark.parametrize("topic", TOPICS)
@pytest.mark.parametrize("group_name", GROUPS)
def test_displayed_comparison_runs_independently(
    topic: str, group_name: str, tmp_path: Path
) -> None:
    comparison = deepcopy(TOPICS[topic])
    build_comparison(ROOT, comparison)
    group = comparison[group_name]
    for item in group["files"]:
        assert item["code"] == (ROOT / item["path"]).read_text()
        assert item["html"]

    files = group.get("allFiles", group["files"])
    assert len({item["name"] for item in files}) == len(files)
    for item in files:
        assert item["code"] == (ROOT / item["path"]).read_text()
        (tmp_path / item["name"]).write_text(item["code"])
    assert group["command"] == (f"uv run --no-project --python 3.15 {group['entry']}")

    result = subprocess.run(
        [sys.executable, "-E", "-B", group["entry"]],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0, result.stderr
    output_key = "extensionOutput" if group_name.endswith("Extension") else "output"
    assert result.stdout == comparison[output_key]
    assert result.stderr == ""


@pytest.fixture
def small_comparison(tmp_path: Path) -> dict:
    (tmp_path / "main.py").write_text('print("base")\n')
    (tmp_path / "helper.py").write_text("value = 1\n")
    return {
        key: {
            "files": [{"name": "main.py", "path": "main.py"}],
            "entry": "main.py",
        }
        for key in GROUPS
    }


def test_extension_reuses_and_replaces_files(
    tmp_path: Path, small_comparison: dict
) -> None:
    small_comparison["after"]["files"].append(
        {"name": "helper.py", "path": "helper.py"}
    )
    (tmp_path / "new_main.py").write_text("from helper import value\nprint(value)\n")
    small_comparison["afterExtension"] = {
        "files": [{"name": "run.py", "path": "new_main.py"}],
        "replaces": ["main.py"],
        "entry": "run.py",
    }
    build_comparison(tmp_path, small_comparison)
    extension = small_comparison["afterExtension"]
    assert [item["name"] for item in extension["allFiles"]] == ["helper.py", "run.py"]
    assert extension["unchanged"] == ["helper.py"]
    assert len(extension["files"]) == 1


def test_missing_entry_rejected(tmp_path: Path, small_comparison: dict) -> None:
    small_comparison["before"]["entry"] = "missing.py"
    with pytest.raises(ValueError, match="Missing comparison entry point"):
        build_comparison(tmp_path, small_comparison)


def test_extension_classifies_actual_source_changes(
    tmp_path: Path, small_comparison: dict
) -> None:
    (tmp_path / "changed.py").write_text('print("extended")\n')
    small_comparison["afterExtension"]["files"] = [
        {"name": "main.py", "path": "changed.py"},
        {"name": "helper.py", "path": "helper.py"},
    ]
    build_comparison(tmp_path, small_comparison)
    assert [item["change"] for item in small_comparison["afterExtension"]["files"]] == [
        "modified",
        "added",
    ]
    assert small_comparison["beforeExtension"]["files"][0]["change"] == "unchanged"


def test_false_stability_claim_rejected(tmp_path: Path, small_comparison: dict) -> None:
    (tmp_path / "changed.py").write_text('print("extended")\n')
    small_comparison["afterExtension"]["files"][0]["path"] = "changed.py"
    small_comparison["architecture"] = {"stableFiles": ["main.py"]}
    with pytest.raises(ValueError, match="Claimed stable comparison file changed"):
        build_comparison(tmp_path, small_comparison)


def test_duplicate_filename_rejected(tmp_path: Path, small_comparison: dict) -> None:
    small_comparison["before"]["files"].append({"name": "main.py", "path": "helper.py"})
    with pytest.raises(ValueError, match="Invalid or duplicate comparison file"):
        build_comparison(tmp_path, small_comparison)


def test_source_outside_project_rejected(
    tmp_path: Path, small_comparison: dict
) -> None:
    small_comparison["before"]["files"][0]["path"] = "../outside.py"
    with pytest.raises(ValueError, match="Comparison source outside project"):
        build_comparison(tmp_path, small_comparison)
