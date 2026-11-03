"""Compatibility adapter for the course build API."""

from pathlib import Path

from course_engine import build_themes as build_shared_themes


def build_themes(root: Path, target: Path) -> None:
    build_shared_themes(target / "src/themes")
