"""Load complete, independently runnable files for side-by-side lessons."""

import ast
from pathlib import Path

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer


def build_comparison(root: Path, comparison: dict) -> None:
    """Resolve source files and overlay each extension onto its own baseline."""
    formatter = HtmlFormatter(nowrap=True)
    lexer = PythonLexer()
    for key in ("before", "after", "beforeExtension", "afterExtension"):
        group = comparison[key]
        names: set[str] = set()
        for item in group["files"]:
            name = item["name"]
            if Path(name).name != name or not name.endswith(".py") or name in names:
                raise ValueError(f"Invalid or duplicate comparison file: {name}")
            names.add(name)
            path = (root / item["path"]).resolve()
            if not path.is_relative_to(root.resolve()):
                raise ValueError(f"Comparison source outside project: {path}")
            code = path.read_text()
            ast.parse(code, filename=str(path))
            item["code"] = code
            item["html"] = highlight(code, lexer, formatter)
        if key.endswith("Extension"):
            base = comparison["before" if key == "beforeExtension" else "after"]
            complete = {item["name"]: item for item in base["files"]}
            for item in group["files"]:
                previous = complete.get(item["name"])
                item["change"] = (
                    "added"
                    if previous is None
                    else "unchanged"
                    if previous["code"] == item["code"]
                    else "modified"
                )
            for name in group.get("replaces", []):
                if name not in complete:
                    raise ValueError(f"Unknown replaced comparison file: {name}")
                del complete[name]
            complete.update({item["name"]: item for item in group["files"]})
            group["allFiles"] = list(complete.values())
            group["unchanged"] = [name for name in complete if name not in names]
        else:
            complete = {item["name"]: item for item in group["files"]}
        if group["entry"] not in complete:
            raise ValueError(f"Missing comparison entry point: {group['entry']}")
        group["command"] = f"uv run --no-project --python 3.15 {group['entry']}"
    base = {item["name"]: item for item in comparison["after"]["files"]}
    extended = {item["name"]: item for item in comparison["afterExtension"]["allFiles"]}
    for name in comparison.get("architecture", {}).get("stableFiles", []):
        if (
            name not in base
            or name not in extended
            or base[name]["code"] != extended[name]["code"]
        ):
            raise ValueError(f"Claimed stable comparison file changed: {name}")
