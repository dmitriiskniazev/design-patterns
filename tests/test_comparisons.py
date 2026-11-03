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
    for topic in json.loads((ROOT / "web/lessons.json").read_text())
    if isinstance(topic.get("fileComparison"), dict)
}
GROUPS = ("before", "after", "beforeExtension", "afterExtension")


def test_comparison_topics() -> None:
    ready = {
        topic["id"]
        for topic in json.loads((ROOT / "web/lessons.json").read_text())
        if topic["ready"]
    }
    assert len(TOPICS) == 25
    assert set(TOPICS) == ready


@pytest.mark.parametrize(
    ("topic", "group_name"),
    [
        (topic, key)
        for topic, comparison in TOPICS.items()
        for key in GROUPS
        if key in comparison
    ],
)
def test_displayed_comparison_runs_independently(
    topic: str, group_name: str, tmp_path: Path
) -> None:
    comparison = deepcopy(TOPICS[topic])
    build_comparison(ROOT, comparison)
    group = comparison[group_name]
    for item in group["files"]:
        assert item["code"] == (ROOT / item["path"]).read_text()
        assert item["html"] or not item["code"]

    files = group["files"]
    assert len({item["name"] for item in files}) == len(files)
    for item in files:
        assert item["code"] == (ROOT / item["path"]).read_text()
        target = tmp_path / item["name"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(item["code"])
    if "module" in group:
        assert f"python -m {group['module']}" in group["command"]
    else:
        assert group["command"] == (
            f"uv run --no-project --python 3.15 {group['directory']}/{group['entry']}"
        )

    result = subprocess.run(
        [
            sys.executable,
            "-E",
            "-B",
            *(["-m", group["module"]] if "module" in group else [group["entry"]]),
        ],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0, result.stderr
    output_key = "extensionOutput" if group_name.endswith("Extension") else "output"
    assert result.stdout == comparison[output_key]
    assert result.stderr == ""
    # The learner's tests must also work after copying just this leaf directory.
    if "module" in group:
        # The shared example is the copyable unit; its tests compare both clients.
        for other_key in ("before", "after"):
            for item in comparison[other_key]["files"]:
                target = tmp_path / item["name"]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(item["code"])
    test = ROOT / group["directory"] / "test_example.py"
    (tmp_path / "test_example.py").write_text(test.read_text())
    checked = subprocess.run(
        [sys.executable, "-E", "-B", "-m", "pytest", "-q", "test_example.py"],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert checked.returncode == 0, checked.stdout + checked.stderr


@pytest.fixture
def small_comparison(tmp_path: Path) -> dict:
    comparison = {}
    for key in GROUPS:
        directory = tmp_path / key
        directory.mkdir()
        (directory / "main.py").write_text('print("base")\n')
        comparison[key] = {"directory": key, "entry": "main.py"}
    return comparison


def test_extension_does_not_overlay_baseline(
    tmp_path: Path, small_comparison: dict
) -> None:
    (tmp_path / "after/helper.py").write_text("value = 1\n")
    build_comparison(tmp_path, small_comparison)
    assert [file["name"] for file in small_comparison["afterExtension"]["files"]] == [
        "main.py"
    ]


def test_missing_dependency_rejected(tmp_path: Path, small_comparison: dict) -> None:
    (tmp_path / "after/helper.py").write_text("value = 1\n")
    (tmp_path / "afterExtension/main.py").write_text(
        "from helper import value\nprint(value)\n"
    )
    with pytest.raises(ValueError, match="Missing local dependency"):
        build_comparison(tmp_path, small_comparison)


def test_missing_entry_rejected(tmp_path: Path, small_comparison: dict) -> None:
    small_comparison["before"]["entry"] = "missing.py"
    with pytest.raises(ValueError, match="Missing comparison entry point"):
        build_comparison(tmp_path, small_comparison)


def test_extension_classifies_actual_source_changes(
    tmp_path: Path, small_comparison: dict
) -> None:
    (tmp_path / "afterExtension/main.py").write_text('print("extended")\n')
    (tmp_path / "afterExtension/helper.py").write_text("value = 1\n")
    build_comparison(tmp_path, small_comparison)
    changes = {
        file["name"]: file["change"]
        for file in small_comparison["afterExtension"]["files"]
    }
    assert changes == {"helper.py": "added", "main.py": "modified"}
    assert small_comparison["beforeExtension"]["files"][0]["change"] == "unchanged"


def test_false_stability_claim_rejected(tmp_path: Path, small_comparison: dict) -> None:
    (tmp_path / "afterExtension/main.py").write_text('print("extended")\n')
    small_comparison["architecture"] = {"stableFiles": ["main.py"]}
    with pytest.raises(ValueError, match="Claimed stable comparison file changed"):
        build_comparison(tmp_path, small_comparison)


def test_source_outside_variant_rejected(
    tmp_path: Path, small_comparison: dict
) -> None:
    (tmp_path / "before/main.py").unlink()
    (tmp_path / "before/main.py").symlink_to(tmp_path / "after/main.py")
    with pytest.raises(ValueError, match="Comparison source outside variant"):
        build_comparison(tmp_path, small_comparison)


def test_directory_outside_project_rejected(
    tmp_path: Path, small_comparison: dict
) -> None:
    small_comparison["before"]["directory"] = "../outside"
    with pytest.raises(ValueError, match="Comparison directory outside project"):
        build_comparison(tmp_path, small_comparison)
