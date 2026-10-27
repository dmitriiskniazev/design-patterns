"""Build short Python listings from executable source; keep full files separate."""

import ast
import json
import textwrap
from pathlib import Path
from urllib.parse import urlparse

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

from design_patterns.comparisons import build_comparison
from design_patterns.guide import build_guide

formatter = HtmlFormatter(nowrap=True)
lexer = PythonLexer()


def extract(source: str, selectors: list[str]) -> str:
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)

    def segment(node: ast.stmt) -> str:
        start = min(
            [node.lineno] + [d.lineno for d in getattr(node, "decorator_list", [])]
        )
        return textwrap.dedent("".join(lines[start - 1 : node.end_lineno])).rstrip()

    parts = []
    for selector in selectors:
        if selector == "@module":
            parts.append(source.rstrip())
        elif selector == "@usage":
            guards = [
                n
                for n in tree.body
                if isinstance(n, ast.If)
                and isinstance(n.test, ast.Compare)
                and isinstance(n.test.left, ast.Name)
                and n.test.left.id == "__name__"
                and len(n.test.ops) == 1
                and isinstance(n.test.ops[0], ast.Eq)
                and len(n.test.comparators) == 1
                and isinstance(n.test.comparators[0], ast.Constant)
                and n.test.comparators[0].value == "__main__"
            ]
            if len(guards) != 1:
                raise ValueError("Expected one if __name__ == '__main__' guard")
            node = guards[0]
            parts.append(
                textwrap.dedent(
                    "".join(lines[node.body[0].lineno - 1 : node.end_lineno])
                ).rstrip()
            )
        elif selector.startswith("fields:"):
            name = selector.split(":", 1)[1]
            node = next(
                n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == name
            )
            start = min([node.lineno] + [d.lineno for d in node.decorator_list])
            header = "".join(lines[start - 1 : node.body[0].lineno - 1]).rstrip()
            fields = [segment(n) for n in node.body if isinstance(n, ast.AnnAssign)]
            parts.append(
                header + "\n" + textwrap.indent("\n".join(fields) or "pass", "    ")
            )
        elif selector.startswith("import:"):
            name = selector.split(":", 1)[1]
            node = next(
                n
                for n in tree.body
                if isinstance(n, (ast.Import, ast.ImportFrom))
                and any(a.name == name for a in n.names)
            )
            parts.append(segment(node))
        elif selector.startswith("body:"):
            class_name, method_name = selector.removeprefix("body:").split(".", 1)
            cls = next(
                n
                for n in tree.body
                if isinstance(n, ast.ClassDef) and n.name == class_name
            )
            method = next(
                n
                for n in cls.body
                if isinstance(n, ast.FunctionDef) and n.name == method_name
            )
            parts.append(
                textwrap.dedent(
                    "".join(lines[method.body[0].lineno - 1 : method.end_lineno])
                ).rstrip()
            )
        elif "." in selector:
            class_name, method_name = selector.split(".", 1)
            cls = next(
                n
                for n in tree.body
                if isinstance(n, ast.ClassDef) and n.name == class_name
            )
            method = next(
                n
                for n in cls.body
                if isinstance(n, ast.FunctionDef) and n.name == method_name
            )
            if method_name == "__init__":
                parts.append(
                    lines[cls.lineno - 1].rstrip()
                    + "\n"
                    + textwrap.indent(segment(method), "    ")
                )
            else:
                parts.append(segment(method))
        else:
            node = next(
                n
                for n in tree.body
                if getattr(n, "name", None) == selector
                or (isinstance(n, ast.TypeAlias) and n.name.id == selector)
                or (
                    isinstance(n, ast.Assign)
                    and any(
                        isinstance(target, ast.Name) and target.id == selector
                        for target in n.targets
                    )
                )
            )
            parts.append(segment(node))
    code = "\n\n".join(parts) + "\n"
    if sum(bool(line.strip()) for line in code.splitlines()) > 12:
        raise ValueError(f"Listing too long: {selectors}")
    return code


def build(root: Path) -> list[dict]:
    topics = json.loads((root / "web/lessons.json").read_text())
    for topic in topics:
        if topic["ready"] and not isinstance(topic.get("guide"), dict):
            raise ValueError(f"Missing guide for {topic['id']}")
    identifiers = [topic["id"] for topic in topics]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("Duplicate topic identifiers")
    for topic in topics:
        if topic["ready"]:
            source_url = urlparse(topic.get("source", ""))
            if source_url.scheme != "https" or not source_url.netloc:
                raise ValueError(f"Missing HTTPS source for {topic['id']}")
    listing_count = 0
    for topic in topics:
        if not topic["ready"]:
            continue
        if "fileComparison" in topic:
            build_comparison(root, topic["fileComparison"])
        for flow, key in ((topic, "after"), (topic["extension"], "afterExtension")):
            group = topic["fileComparison"][key]
            directory = group["directory"]
            default_file = flow["entryFile"]
            path = f"{directory}/{default_file}"
            nodes = flow["overview"]["nodes"]
            owners = {node["id"] for node in nodes}
            if len(owners) != len(nodes) or any(
                not 1 <= node["step"] <= len(flow["steps"]) for node in nodes
            ):
                raise ValueError(f"Invalid solution map: {topic['id']}")
            for step in flow["steps"]:
                if step["owner"] not in owners or not step["place"]:
                    raise ValueError(f"Missing fragment context: {topic['id']}")
                file = f"{directory}/{step.get('file', default_file)}"
                try:
                    step["code"] = extract((root / file).read_text(), step["selectors"])
                except (ValueError, StopIteration) as error:
                    raise ValueError(
                        f"Invalid listing in {file}: {step['selectors']}: {error}"
                    ) from error
                step["html"] = highlight(step["code"], lexer, formatter)
                step["sourcePath"] = file
                listing_count += 1
            source = (root / path).read_text()
            source_files = [
                {
                    "path": item["path"],
                    "role": "Запуск"
                    if item["name"] == default_file
                    else "Роль: " + Path(item["name"]).stem,
                    "code": item["code"],
                    "html": item["html"],
                }
                for item in group["files"]
            ]
            if path not in {item["path"] for item in source_files}:
                raise ValueError(f"Entry point missing from source files: {path}")
            flow["example"] = {
                "path": path,
                "command": f"uv run --no-project --python 3.15 {path}",
                "code": source,
                "html": highlight(source, lexer, formatter),
                "files": source_files,
            }

        build_guide(root, topic, extract)

    print(
        f"Built {listing_count} short Python listings for {sum(t['ready'] for t in topics)} lessons"
    )

    return topics
