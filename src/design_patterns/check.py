"""Проверять инфраструктуру и каждую тему в отдельном процессе."""

import subprocess
import sys
from pathlib import Path


def check(root: Path) -> int:
    directories = [root / "tests", *sorted((root / "examples").glob("*/python"))]
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
    raise SystemExit(check(Path.cwd()))
