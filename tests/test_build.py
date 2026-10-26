import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from design_patterns.build import build, extract


def test_import_does_not_build(tmp_path: Path) -> None:
    subprocess.run(
        [sys.executable, "-c", "import design_patterns.build"],
        cwd=tmp_path,
        check=True,
    )
    assert not list(tmp_path.iterdir())


def test_extract_rejects_long_listing() -> None:
    with pytest.raises(ValueError, match="Listing too long"):
        extract("\n".join(f"value_{i} = {i}" for i in range(13)), ["@module"])


def test_build_complete_course(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    for directory in ("web", "examples"):
        shutil.copytree(
            root / directory,
            tmp_path / directory,
            ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"),
        )
    topics = build(tmp_path)
    ready = [topic for topic in topics if topic["ready"]]
    assert len(ready) == 25
    assert not list(tmp_path.rglob("*.zip"))
    assert not (tmp_path / "assets").exists()
    for topic in ready:
        for flow in (topic, topic["extension"]):
            example = flow["example"]
            assert "archivePath" not in example
            for file in example["files"]:
                assert file["code"] == (root / file["path"]).read_text()
            for step in flow["steps"]:
                lines = step["code"].splitlines()
                assert sum(bool(line.strip()) for line in lines) <= 12
                assert step["html"]
    assert not (tmp_path / "lessons").exists()
    assert not (tmp_path / "reference").exists()
