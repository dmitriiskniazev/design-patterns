"""Проверять инфраструктуру и каждый самостоятельный вариант отдельным процессом."""

import argparse
import subprocess
import sys
from pathlib import Path


def check(root: Path, topic: str | None = None) -> int:
    examples = root / "examples"
    selected = examples / topic if topic else examples
    variants = sorted(path.parent for path in selected.rglob("test_example.py"))
    if not variants:
        raise ValueError(f"No example variants found: {selected}")
    directories = ([root / "tests"] if topic is None else []) + variants
    for directory in directories:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", str(directory)],
            cwd=root,
            check=False,
        )
        if result.returncode:
            return result.returncode
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topic", nargs="?", help="Например, abstract-factory")
    raise SystemExit(check(Path.cwd(), parser.parse_args().topic))
