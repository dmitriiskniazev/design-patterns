"""Compatibility checks across the installed engine and the course adapter."""

import shutil
import subprocess
from pathlib import Path

import pytest

from design_patterns.site import package


@pytest.mark.skipif(shutil.which("node") is None, reason="Node is needed for adapter checks")
def test_shared_engine_preserves_preferences_labels_and_routes() -> None:
    root = Path(__file__).resolve().parents[1]
    target = package(root)
    result = subprocess.run(
        ["node", str(Path(__file__).with_name("shared_adapter.mjs")), str(target)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
