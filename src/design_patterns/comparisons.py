"""Load four complete snapshots without importing or overlaying another variant."""

import ast
import sys
from pathlib import Path

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer


def build_comparison(root: Path, comparison: dict) -> None:
    formatter = HtmlFormatter(nowrap=True)
    lexer = PythonLexer()
    for key in ("before", "after", "beforeExtension", "afterExtension"):
        group = comparison[key]
        directory = (root / group["directory"]).resolve()
        if not directory.is_relative_to(root.resolve()):
            raise ValueError(f"Comparison directory outside project: {directory}")
        paths = sorted(directory.glob("*.py"))
        files = []
        for path in paths:
            if path.name.startswith("test_"):
                continue
            if not path.resolve().is_relative_to(directory):
                raise ValueError(f"Comparison source outside variant: {path}")
            code = path.read_text()
            tree = ast.parse(code, filename=str(path))
            for node in ast.walk(tree):
                modules = (
                    [node.module or ""]
                    if isinstance(node, ast.ImportFrom)
                    else [alias.name for alias in node.names]
                    if isinstance(node, ast.Import)
                    else []
                )
                if isinstance(node, ast.ImportFrom) and node.level:
                    raise ValueError(f"Relative import outside variant: {path}")
                for module in modules:
                    if module.split(".")[0] not in sys.stdlib_module_names:
                        dependency = directory / f"{module}.py"
                        if (
                            not dependency.is_file()
                            or not dependency.resolve().is_relative_to(directory)
                        ):
                            raise ValueError(
                                f"Missing local dependency {module} in {path}"
                            )
            files.append(
                {
                    "name": path.name,
                    "path": path.relative_to(root.resolve()).as_posix(),
                    "code": code,
                    "html": highlight(code, lexer, formatter),
                }
            )
        if group["entry"] not in {file["name"] for file in files}:
            raise ValueError(f"Missing comparison entry point: {group['entry']}")
        group["files"] = files
        group["command"] = (
            f"uv run --no-project --python 3.15 {group['directory']}/{group['entry']}"
        )
        if key.endswith("Extension"):
            base = comparison["before" if key == "beforeExtension" else "after"]
            originals = {file["name"]: file["code"] for file in base["files"]}
            for file in files:
                original = originals.get(file["name"])
                file["change"] = (
                    "added"
                    if original is None
                    else "unchanged"
                    if original == file["code"]
                    else "modified"
                )
    base = {item["name"]: item["code"] for item in comparison["after"]["files"]}
    extended = {
        item["name"]: item["code"] for item in comparison["afterExtension"]["files"]
    }
    for name in comparison.get("architecture", {}).get("stableFiles", []):
        if name not in base or name not in extended or base[name] != extended[name]:
            raise ValueError(f"Claimed stable comparison file changed: {name}")
