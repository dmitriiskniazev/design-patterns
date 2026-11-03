"""Build short source comparisons and one copy of each complete chapter file."""

import ast
from collections.abc import Callable
from pathlib import Path

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

from design_patterns.workspaces import build_workspaces


def order_source_files(
    files: list[dict], entry: str | None, imports: dict[str, list[str]]
) -> list[dict]:
    """Read from the entry through its direct dependencies, then deeper roles."""
    by_name = {file["name"]: file for file in files}
    ordered = []
    seen = set()
    for seed in [entry, *sorted(by_name)]:
        pending = [seed]
        for name in pending:
            if name not in by_name or name in seen:
                continue
            seen.add(name)
            ordered.append(by_name[name])
            pending.extend(imports.get(name, []))
    return ordered


def build_guide(
    root: Path, topic: dict, extract: Callable[[str, list[str]], str]
) -> None:
    guide = topic["guide"]
    formatter, lexer = HtmlFormatter(nowrap=True), PythonLexer()
    if len(guide.get("terms", [])) < 3 or len(guide.get("designNotes", [])) < 2:
        raise ValueError("Guide needs terms and design reasons")

    def read(path: str) -> str:
        source = (root / path).resolve()
        if not source.is_relative_to(root.resolve()) or source.suffix != ".py":
            raise ValueError(f"Invalid guide source: {path}")
        return source.read_text()

    for diagram in guide["diagrams"].values():
        ids = [node["id"] for node in diagram["nodes"]]
        if not ids or len(ids) != len(set(ids)):
            raise ValueError("Invalid guide diagram nodes")
        for edge in diagram["edges"]:
            if edge["from"] not in ids or edge["to"] not in ids:
                raise ValueError("Unknown guide diagram node")
    for contrast in guide["contrasts"]:
        for key in ("before", "after"):
            snippet = contrast[key]
            try:
                snippet["code"] = extract(read(snippet["path"]), snippet["selectors"])
            except (ValueError, StopIteration) as error:
                raise ValueError(
                    f"Invalid guide fragment: {snippet['path']}"
                ) from error
            snippet["html"] = highlight(snippet["code"], lexer, formatter)
    sources: dict[tuple[str, str], dict] = {}
    versions = []

    def version(
        version_key: str,
        label: str,
        files: list[dict],
        command: str,
        entry: str,
    ) -> None:
        refs = []
        imports = {}
        for file in files:
            path = file.get("path")
            code = read(path)
            name = file.get("name", Path(path).name)
            if name.endswith("__init__.py") and not code.strip():
                continue
            tree = ast.parse(code)
            names = {
                node.name
                for node in tree.body
                if isinstance(node, (ast.ClassDef, ast.FunctionDef))
            }
            names.update(
                node.name.id for node in tree.body if isinstance(node, ast.TypeAlias)
            )
            purposes = [
                role["purpose"]
                for role in guide["roles"]
                if any(symbol in role["name"] for symbol in names)
            ]
            role = file.get("role") or " ".join(purposes[:2])
            if not role:
                role = (
                    "Данные и варианты"
                    if name in {"model.py", "models.py"}
                    else "Реализация " + ", ".join(sorted(names))
                )
            if name.startswith("test_"):
                role = "Проверки поведения"
            if any(
                isinstance(node, ast.If)
                and isinstance(node.test, ast.Compare)
                and isinstance(node.test.left, ast.Name)
                and node.test.left.id == "__name__"
                for node in tree.body
            ):
                mode = (
                    "расширенного" if version_key.endswith("Extension") else "базового"
                )
                approach = (
                    "без паттерна"
                    if version_key.startswith("before")
                    else "с паттерном"
                )
                role = (
                    f"Запуск примера {approach}"
                    if "beforeExtension" not in topic["fileComparison"]
                    else f"Запуск {mode} примера {approach}"
                )
            key = (name, code)
            if key not in sources:
                sources[key] = {
                    "id": f"guide-source-{len(sources) + 1}",
                    "name": name,
                    "paths": [],
                    "usedBy": [],
                    "code": code,
                    "html": highlight(code, lexer, formatter),
                    "imports": list(
                        dict.fromkeys(
                            module.replace(".", "/") + ".py"
                            for node in ast.walk(tree)
                            for module in (
                                [node.module]
                                if isinstance(node, ast.ImportFrom)
                                and node.module
                                and not node.level
                                else [alias.name for alias in node.names]
                                if isinstance(node, ast.Import)
                                else []
                            )
                        )
                    ),
                }
            source = sources[key]
            imports[name] = source["imports"]
            if path not in source["paths"]:
                source["paths"].append(path)
            if label not in source["usedBy"]:
                source["usedBy"].append(label)
            refs.append(
                {
                    "id": source["id"],
                    "name": name,
                    "path": path,
                    "role": role,
                    "change": file.get("change", ""),
                }
            )
        if entry not in {ref["name"] for ref in refs}:
            entry = None
        refs = order_source_files(refs, entry, imports)
        versions.append(
            {
                "key": version_key,
                "extended": version_key.endswith("Extension"),
                "label": label,
                "files": refs,
                "command": command,
                "entry": entry,
                "defaultFile": entry or refs[0]["name"],
            }
        )

    comparison = topic["fileComparison"]
    for key, label in (
        ("before", "Без паттерна"),
        ("after", "С паттерном"),
        ("beforeExtension", "Расширение без паттерна"),
        ("afterExtension", "Расширение с паттерном"),
    ):
        if key not in comparison:
            continue
        group = comparison[key]
        version(key, label, group["files"], group["command"], group["entry"])
    guide["sources"] = list(sources.values())
    guide["versions"] = versions
    guide["pairs"] = {
        "base": {"before": 0, "after": 1},
        "extended": {"before": 2, "after": 3},
    }
    if len(versions) == 2:
        guide["pairs"] = {"base": {"before": 0, "after": 1}}
        guide.setdefault("legacyVersionIndices", [0, 1, 1, 1])
    guide.setdefault(
        "legacyVersionIndices",
        [0, 1, 2, 3],
    )
    guide["extensionRequirement"] = (
        topic.get("fileComparison", {}).get("requirement")
        or topic["extension"]["title"]
    )
    build_workspaces(topic)
