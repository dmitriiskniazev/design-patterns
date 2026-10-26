"""Deployment layout and complete offline snapshots."""

import json
from pathlib import Path

from design_patterns.site import package


def test_offline_snapshot_contains_every_published_file() -> None:
    root = Path(__file__).resolve().parents[1]
    target = package(root)
    worker = (target / "sw.js").read_text()
    files = json.loads(worker.split("const FILES = ", 1)[1].split(";", 1)[0])
    assert "web/" in files and "./" in files
    assert ".nojekyll" not in files
    assert "assets/course-data.js" in files
    assert "assets/examples/strategy-base.zip" in files
    for name in files:
        assert (target / name).exists()
    for path in target.rglob("*"):
        if path.is_file() and path.name != "sw.js" and not path.name.startswith("."):
            assert path.relative_to(target).as_posix() in files
    assert "__VERSION__" not in worker
    assert not list(target.rglob("__pycache__"))


def test_manifest_paths_stay_inside_project() -> None:
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "web/manifest.webmanifest").read_text())
    assert manifest["start_url"] == "./"
    assert manifest["scope"] == "../"
    assert manifest["display"] == "standalone"
    assert {icon["sizes"] for icon in manifest["icons"]} == {"192x192", "512x512"}
