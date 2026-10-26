"""Build short source comparisons and one copy of each complete chapter file."""

import ast
from collections.abc import Callable
from difflib import SequenceMatcher
from pathlib import Path

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer


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


def source_diff(before: str, after: str) -> list[dict]:
    """Return all lines in order; source strings remain the copyable originals."""
    old_lines = before.splitlines(keepends=True)
    new_lines = after.splitlines(keepends=True)
    lexer = PythonLexer(stripnl=False, ensurenl=False)
    formatter = HtmlFormatter(nowrap=True)
    old_html = highlight(before, lexer, formatter).splitlines() if before else []
    new_html = highlight(after, lexer, formatter).splitlines() if after else []
    rows = []
    for tag, start, end, new_start, new_end in SequenceMatcher(
        None, old_lines, new_lines, autojunk=False
    ).get_opcodes():
        if tag == "equal":
            for offset, index in enumerate(range(start, end)):
                rows.append(
                    {
                        "kind": "equal",
                        "beforeLine": index + 1,
                        "afterLine": new_start + offset + 1,
                        "text": old_lines[index],
                        "html": old_html[index],
                    }
                )
        else:
            for index in range(start, end):
                rows.append(
                    {
                        "kind": "removed",
                        "beforeLine": index + 1,
                        "afterLine": None,
                        "text": old_lines[index],
                        "html": old_html[index],
                    }
                )
            for index in range(new_start, new_end):
                rows.append(
                    {
                        "kind": "added",
                        "beforeLine": None,
                        "afterLine": index + 1,
                        "text": new_lines[index],
                        "html": new_html[index],
                    }
                )
    return rows


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
        before = contrast["before"]["code"].splitlines(keepends=True)
        after = contrast["after"]["code"].splitlines(keepends=True)
        prefix = 0
        while prefix < min(len(before), len(after)) and before[prefix] == after[prefix]:
            prefix += 1
        suffix = 0
        while (
            suffix < min(len(before), len(after)) - prefix
            and before[-suffix - 1] == after[-suffix - 1]
        ):
            suffix += 1
        contrast["commonBeforeCode"] = "".join(before[:prefix])
        contrast["commonAfterCode"] = (
            "".join(before[len(before) - suffix :]) if suffix else ""
        )
        contrast["commonBefore"] = highlight(
            contrast["commonBeforeCode"], lexer, formatter
        )
        contrast["commonAfter"] = (
            highlight(contrast["commonAfterCode"], lexer, formatter) if suffix else ""
        )
        for key, lines in (("before", before), ("after", after)):
            code = "".join(lines[prefix : len(lines) - suffix if suffix else None])
            contrast[key]["difference"] = code
            contrast[key]["differenceHtml"] = (
                highlight(code, lexer, formatter) if code.strip() else ""
            )

    sources: dict[tuple[str, str], dict] = {}
    versions = []

    def version(
        version_key: str,
        label: str,
        files: list[dict],
        command: str = "",
        default_file: str | None = None,
    ) -> None:
        refs = []
        launches = {}
        imports = {}
        for file in files:
            path = file.get("path")
            code = read(path)
            name = Path(path).name
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
                mode = "расширенного" if name.endswith("_extended.py") else "базового"
                approach = (
                    "без паттерна"
                    if name.startswith("without_pattern")
                    else "с паттерном"
                )
                role = f"Запуск {mode} примера {approach}"
                launches[name] = path
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
                            module + ".py"
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
        if not command and default_file in launches:
            command = f"uv run --no-project --python 3.15 {launches[default_file]}"
        entry = Path(command.split()[-1]).name if command else None
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
                "defaultFile": entry or default_file or refs[0]["name"],
            }
        )

    def baseline_files(seed: str) -> list[dict]:
        known = {file["path"]: file for file in guide["baselineFiles"]}
        pending = [f"examples/{topic['id']}/python/{seed}"]
        complete = []
        seen = set()
        for path in pending:
            if path in seen:
                continue
            seen.add(path)
            code = read(path)
            complete.append(known.get(path, {"path": path}))
            for node in ast.walk(ast.parse(code)):
                modules = (
                    [node.module]
                    if isinstance(node, ast.ImportFrom)
                    and node.module
                    and not node.level
                    else [alias.name for alias in node.names]
                    if isinstance(node, ast.Import)
                    else []
                )
                for module in modules:
                    dependency = Path(path).parent / (module + ".py")
                    if (root / dependency).is_file():
                        pending.append(str(dependency))
        return complete

    def implementation_files(files: list[dict], entry: str) -> list[dict]:
        available = {Path(file["path"]).name: file for file in files}
        pending = [entry]
        selected = []
        seen = set()
        for name in pending:
            if name in seen:
                continue
            seen.add(name)
            file = available[name]
            selected.append(file)
            for node in ast.walk(ast.parse(read(file["path"]))):
                modules = (
                    [node.module]
                    if isinstance(node, ast.ImportFrom)
                    and node.module
                    and not node.level
                    else [alias.name for alias in node.names]
                    if isinstance(node, ast.Import)
                    else []
                )
                pending.extend(
                    module + ".py" for module in modules if module + ".py" in available
                )
        return selected

    if comparison := topic.get("fileComparison"):
        for key, label in (
            ("before", "Без паттерна"),
            ("after", "С паттерном"),
            ("beforeExtension", "Расширение без паттерна"),
            ("afterExtension", "Расширение с паттерном"),
        ):
            group = comparison[key]
            version(key, label, group.get("allFiles", group["files"]), group["command"])
    else:
        version(
            "before",
            "Без паттерна",
            baseline_files("without_pattern.py"),
            default_file="without_pattern.py",
        )
        version(
            "after",
            "С паттерном",
            implementation_files(topic["example"]["files"], topic["entryFile"]),
            topic["example"]["command"],
        )
        version(
            "beforeExtension",
            "Расширение без паттерна",
            baseline_files("without_pattern_extended.py"),
            default_file="without_pattern_extended.py",
        )
        version(
            "afterExtension",
            "Расширение с паттерном",
            implementation_files(
                topic["extension"]["example"]["files"], topic["extension"]["entryFile"]
            ),
            topic["extension"]["example"]["command"],
        )
    by_id = {source["id"]: source for source in sources.values()}
    for base_index, extension_index in ((0, 2), (1, 3)):
        base_version, extension = versions[base_index], versions[extension_index]
        base = {file["name"]: file for file in base_version["files"]}
        for file in extension["files"]:
            base_name = (
                base_version["entry"]
                if file["name"] == extension["entry"]
                else file["name"]
            )
            original = base.get(base_name)
            before = by_id[original["id"]]["code"] if original else ""
            after = by_id[file["id"]]["code"]
            file["change"] = (
                "added"
                if original is None
                else "unchanged"
                if before == after
                else "modified"
            )
            file["diff"] = {
                "baseName": original["name"] if original else None,
                "baseId": original["id"] if original else None,
                "rows": source_diff(before, after),
            }
    guide["sources"] = list(sources.values())
    guide["versions"] = versions
    guide["pairs"] = {
        "base": {"before": 0, "after": 1},
        "extended": {"before": 2, "after": 3},
    }
    guide.setdefault(
        "legacyVersionIndices",
        [0, 1, 2, 3] if topic.get("fileComparison") else [0, 1, 3],
    )
    guide["extensionRequirement"] = (
        topic.get("fileComparison", {}).get("requirement")
        or topic["extension"]["title"]
    )
