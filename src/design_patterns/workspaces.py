"""Resolve authored semantic file pairs and align their complete source lines."""

import re
from difflib import SequenceMatcher

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer


_DECLARATION = re.compile(r"^([ \t]*)(async[ \t]+def|def|class)[ \t]+(\w+)")
_BINDING = re.compile(r"^([ \t]*)(\w+(?:\.\w+)*)[ \t]*(?::|=(?!=))")


def _line_key(line: str) -> str:
    """Keep a declaration anchored when its parameters or line wrapping change."""
    declaration = _DECLARATION.match(line)
    if declaration:
        indent, kind, name = declaration.groups()
        return f"{indent}{kind} {name}"
    return line


def _similarity(before: str, after: str) -> float:
    left, right = before.strip(), after.strip()
    if not left or not right:
        return 0.01 if not left and not right else 0
    if _DECLARATION.match(before) or _DECLARATION.match(after):
        if _line_key(before) != _line_key(after):
            return 0
    ratio = SequenceMatcher(None, left, right, autojunk=False).ratio()
    old_binding, new_binding = _BINDING.match(before), _BINDING.match(after)
    if old_binding and new_binding and old_binding.groups() == new_binding.groups():
        # A variable's annotation and its new initializer are useful neighbours.
        ratio = max(ratio, 0.8)
    # Weak punctuation/indentation coincidences should leave separate gaps.
    return ratio - 0.5 if ratio >= 0.6 else 0


def _changed_pairs(old: list[str], new: list[str]) -> list[tuple[int | None, int | None]]:
    """Find an ordered maximum-similarity alignment, allowing unpaired lines."""
    height, width = len(old), len(new)
    scores = [[0.0] * (width + 1) for _ in range(height + 1)]
    choices = {}
    for left in range(height - 1, -1, -1):
        for right in range(width - 1, -1, -1):
            similarity = _similarity(old[left], new[right])
            paired = similarity + scores[left + 1][right + 1]
            removed, added = scores[left + 1][right], scores[left][right + 1]
            if similarity and paired >= max(removed, added):
                scores[left][right], choices[left, right] = paired, "pair"
            elif removed >= added:
                scores[left][right], choices[left, right] = removed, "remove"
            else:
                scores[left][right], choices[left, right] = added, "add"
    pairs = []
    left = right = 0
    while left < height or right < width:
        choice = choices.get((left, right))
        if choice == "pair":
            pairs.append((left, right))
            left += 1
            right += 1
        elif right == width or choice == "remove":
            pairs.append((left, None))
            left += 1
        else:
            pairs.append((None, right))
            right += 1
    return pairs


def aligned_lines(before: str, after: str) -> list[dict]:
    lexer = PythonLexer(stripnl=False, ensurenl=False)
    formatter = HtmlFormatter(nowrap=True)
    old, new = before.splitlines(keepends=True), after.splitlines(keepends=True)
    old_html = highlight(before, lexer, formatter).splitlines() if before else []
    new_html = highlight(after, lexer, formatter).splitlines() if after else []

    def cell(
        lines: list[str], html: list[str], index: int | None, kind: str
    ) -> dict | None:
        if index is None:
            return None
        return {
            "number": index + 1,
            "text": lines[index],
            "html": html[index],
            "kind": kind,
        }

    rows = []
    for tag, start, end, new_start, new_end in SequenceMatcher(
        lambda key: not key.strip(),
        [_line_key(line) for line in old],
        [_line_key(line) for line in new],
        autojunk=False,
    ).get_opcodes():
        if tag == "equal":
            pairs = list(zip(range(start, end), range(new_start, new_end)))
        else:
            pairs = [
                (
                    start + left if left is not None else None,
                    new_start + right if right is not None else None,
                )
                for left, right in _changed_pairs(old[start:end], new[new_start:new_end])
            ]
        for left, right in pairs:
            equal = left is not None and right is not None and old[left] == new[right]
            rows.append(
                {
                    "before": cell(
                        old, old_html, left, "equal" if equal else "removed"
                    ),
                    "after": cell(
                        new, new_html, right, "equal" if equal else "added"
                    ),
                }
            )
    return rows


def build_workspaces(topic: dict) -> None:
    guide = topic["guide"]
    sources = {source["id"]: source for source in guide["sources"]}
    workspaces = {}
    for stage, indices in guide["pairs"].items():
        versions = {side: guide["versions"][index] for side, index in indices.items()}
        refs = {
            side: {ref["name"]: ref for ref in version["files"]}
            for side, version in versions.items()
        }
        authored = guide["filePairs"][stage]
        pairs, ids = [], set()
        covered = {"before": set(), "after": set()}
        for item in authored:
            if (
                not isinstance(item["id"], str)
                or not re.fullmatch(r"[a-z][a-z0-9-]*", item["id"])
                or item["id"] in ids
                or not item["label"]
            ):
                raise ValueError(f"Invalid workspace pair: {topic['id']}/{stage}")
            ids.add(item["id"])
            resolved = {}
            code = {}
            for side in ("before", "after"):
                name = item.get(side)
                if name and name not in refs[side]:
                    raise ValueError(
                        f"Unknown workspace file: {topic['id']}/{stage}/{side}/{name}"
                    )
                resolved[side] = refs[side].get(name)
                code[side] = sources[resolved[side]["id"]]["code"] if name else ""
                if name:
                    covered[side].add(name)
            if not any(resolved.values()):
                raise ValueError(f"Empty workspace pair: {item['id']}")
            common = all(resolved.values()) and code["before"] == code["after"]
            pairs.append(
                {
                    **item,
                    **resolved,
                    "common": bool(common),
                    "rows": aligned_lines(code["before"], code["after"]),
                }
            )
        if not pairs or any(covered[side] != set(refs[side]) for side in covered):
            raise ValueError(f"Unreachable workspace files: {topic['id']}/{stage}")
        workspaces[stage] = {
            "pairs": pairs,
            "defaultPair": pairs[0]["id"],
            "commands": {
                side: version["command"] for side, version in versions.items()
            },
        }
    guide["workspaces"] = workspaces
