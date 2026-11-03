import json
from copy import deepcopy
from pathlib import Path

import pytest

from design_patterns.build import build, extract
from design_patterns.guide import build_guide, order_source_files
from design_patterns.workspaces import aligned_lines, build_workspaces

ROOT = Path(__file__).resolve().parents[1]
GUIDES = {
    topic["id"]: topic["guide"]
    for topic in json.loads((ROOT / "web/lessons.json").read_text())
    if topic["ready"]
}


def test_source_reading_order_handles_shared_dependencies_cycles_and_orphans() -> None:
    files = [
        {"name": name} for name in ["leaf.py", "b.py", "entry.py", "a.py", "unused.py"]
    ]
    dependencies = {
        "entry.py": ["a.py", "b.py", "external.py"],
        "a.py": ["leaf.py"],
        "b.py": ["leaf.py"],
        "leaf.py": ["entry.py"],
    }
    assert [
        file["name"] for file in order_source_files(files, "entry.py", dependencies)
    ] == ["entry.py", "a.py", "b.py", "leaf.py", "unused.py"]


def test_build_rejects_missing_guide(tmp_path: Path) -> None:
    (tmp_path / "web").mkdir()
    (tmp_path / "web/lessons.json").write_text(
        json.dumps([{"id": "strategy", "ready": True}])
    )
    with pytest.raises(ValueError, match="Missing guide"):
        build(tmp_path)


def test_build_rejects_duplicate_topics(tmp_path: Path) -> None:
    (tmp_path / "web").mkdir()
    (tmp_path / "web/lessons.json").write_text(
        json.dumps([{"id": "strategy", "ready": True, "guide": {}}] * 2)
    )
    with pytest.raises(ValueError, match="Duplicate topic identifiers"):
        build(tmp_path)


@pytest.mark.parametrize("topic_id", GUIDES)
def test_guide_differences_are_real_source(topic_id: str) -> None:
    guide = deepcopy(GUIDES[topic_id])
    # Source extraction and validation use the same inputs as the course build.
    for row in guide["contrasts"]:
        for side in ("before", "after"):
            snippet = row[side]
            code = extract((ROOT / snippet["path"]).read_text(), snippet["selectors"])
            assert 0 < sum(bool(line.strip()) for line in code.splitlines()) <= 12
    assert len(guide["contrasts"]) == (3 if topic_id == "abstract-factory" else 2)
    assert len(guide["growth"]) >= 2
    assert len(guide["applications"]) >= 2
    assert len(guide["terms"]) >= 3
    assert len(guide["designNotes"]) >= 2


def test_guide_rejects_unknown_diagram_node() -> None:
    guide = deepcopy(GUIDES["strategy"])
    guide["diagrams"]["before"]["edges"][0]["to"] = "missing"
    with pytest.raises(ValueError, match="Unknown guide diagram node"):
        build_guide(ROOT, {"guide": guide}, extract)


def test_guide_rejects_external_source() -> None:
    guide = deepcopy(GUIDES["strategy"])
    guide["contrasts"][0]["before"]["path"] = "../outside.py"
    with pytest.raises(ValueError, match="Invalid guide fragment"):
        build_guide(ROOT, {"guide": guide}, extract)


def test_guide_has_exact_differences_and_unique_full_files() -> None:
    topics = build(ROOT)
    chapters = [topic["guide"] for topic in topics if "guide" in topic]
    assert len(chapters) == 25
    for guide in chapters:
        expected = (
            ["before", "after"]
            if len(guide["versions"]) == 2
            else [
                "before",
                "after",
                "beforeExtension",
                "afterExtension",
            ]
        )
        assert [version["key"] for version in guide["versions"]] == expected
        expected_pairs = {
            "base": {"before": 0, "after": 1},
            "extended": {"before": 2, "after": 3},
        }
        if len(expected) == 2:
            del expected_pairs["extended"]
        assert guide["pairs"] == expected_pairs
        sources = guide["sources"]
        assert len({(file["name"], file["code"]) for file in sources}) == len(sources)
        by_id = {file["id"]: file for file in sources}
        for version in guide["versions"]:
            assert version["defaultFile"] in {ref["name"] for ref in version["files"]}
            if version["entry"]:
                assert version["files"][0]["name"] == version["entry"]
            for ref in version["files"]:
                if version["key"] in {"after", "afterExtension"}:
                    assert not ref["name"].startswith(("without_pattern", "test_"))
                assert version["label"] in by_id[ref["id"]]["usedBy"]
                assert ref["role"].strip()
                assert by_id[ref["id"]]["code"] == (ROOT / ref["path"]).read_text()
                for dependency in by_id[ref["id"]]["imports"]:
                    source_root = (ROOT / ref["path"]).parents[
                        len(Path(ref["name"]).parts) - 1
                    ]
                    if (source_root / dependency).is_file():
                        assert dependency in {item["name"] for item in version["files"]}
        for row in guide["contrasts"]:
            for side in ("before", "after"):
                assert row[side]["code"] == extract(
                    (ROOT / row[side]["path"]).read_text(), row[side]["selectors"]
                )
                assert row[side]["html"]


@pytest.mark.parametrize(
    ("before", "after"),
    [
        ("value = 1\nprint(value)\n", "value = 2\nprint(value)\n"),
        ("", 'print("<new>")\n'),
        ("value = 1\n", ""),
        ("\nvalue = 1\n\n", "\nvalue = 1\n\n"),
        ("value = 1", "value = 2"),
        (
            'text = """first\n    second\nthird"""\n',
            'text = """first\n    changed\nthird"""\n',
        ),
    ],
)
def test_aligned_lines_preserve_both_sources(before: str, after: str) -> None:
    rows = aligned_lines(before, after)
    for side, source in (("before", before), ("after", after)):
        cells = [row[side] for row in rows if row[side] is not None]
        assert "".join(cell["text"] for cell in cells) == source
        assert [cell["number"] for cell in cells] == list(
            range(1, len(source.splitlines()) + 1)
        )
        assert all("<new>" not in cell["html"] for cell in cells)


def test_workspace_semantics_and_complete_coverage() -> None:
    topics = build(ROOT)
    for topic in topics:
        guide = topic["guide"]
        sources = {source["id"]: source for source in guide["sources"]}
        for stage, workspace in guide["workspaces"].items():
            pairs = workspace["pairs"]
            assert pairs[0]["id"] == "operation"
            assert len({pair["id"] for pair in pairs}) == len(pairs)
            for side, version in guide["pairs"][stage].items():
                expected = {ref["name"] for ref in guide["versions"][version]["files"]}
                assert {pair[side]["name"] for pair in pairs if pair[side]} == expected
                for pair in pairs:
                    code = sources[pair[side]["id"]]["code"] if pair[side] else ""
                    assert (
                        "".join(row[side]["text"] for row in pair["rows"] if row[side])
                        == code
                    )
            for pair in pairs:
                for row in pair["rows"]:
                    left, right = row["before"], row["after"]
                    if left and right:
                        assert (left["kind"] == right["kind"] == "equal") == (
                            left["text"] == right["text"]
                        )
                        for first, second in ((left, right), (right, left)):
                            if first["text"].lstrip().startswith("class "):
                                assert not second["text"].lstrip().startswith(("def ", "async def "))
                if pair["common"]:
                    assert (
                        sources[pair["before"]["id"]]["code"]
                        == sources[pair["after"]["id"]]["code"]
                    )
    repository = next(t for t in topics if t["id"] == "repository")
    operation = repository["guide"]["workspaces"]["base"]["pairs"][0]
    assert operation["before"]["name"] == "main.py"
    assert operation["after"]["name"] == "client.py"


def test_abstract_factory_diff_aligns_matching_function_declarations() -> None:
    directory = ROOT / "examples/abstract_factory"
    rows = aligned_lines(
        (directory / "baseline/client.py").read_text(),
        (directory / "pattern/client.py").read_text(),
    )
    for name in ("write_and_read", "validate_and_read"):
        row = next(
            row for row in rows
            if row["before"] and row["before"]["text"].startswith(f"def {name}(")
        )
        assert row["after"] is not None
        assert row["after"]["text"].startswith(f"def {name}(")
        assert row["before"]["kind"] == "removed"
        assert row["after"]["kind"] == "added"
    enum_row = next(
        row for row in rows
        if row["before"] and row["before"]["text"].startswith("class Format(")
    )
    assert enum_row["after"] is None
    signature_row = next(
        index for index, row in enumerate(rows)
        if row["after"] and row["after"]["text"] == "def write_and_read(\n"
    )
    assert rows[signature_row + 1]["before"] is None
    assert rows[signature_row + 1]["after"]["number"] == 5
    assert rows[signature_row + 2]["before"] is None
    assert rows[signature_row + 2]["after"]["number"] == 6


def test_diff_does_not_pair_unrelated_replacements() -> None:
    rows = aligned_lines('class Old:\n    pass\n', 'def new():\n    return 42\n')
    assert all(not (row["before"] and row["after"]) for row in rows)


def test_diff_pairs_similar_changes_without_blank_anchors() -> None:
    rows = aligned_lines(
        'class Mode:\n    VALUE = "old"\n\ndef run(value):\n    return value + 1\n',
        '\ndef run(\n    value: int,\n):\n    return value + 2\n',
    )
    row = next(row for row in rows if row["before"] and "return value" in row["before"]["text"])
    assert row["after"] and "return value + 2" in row["after"]["text"]
    row = next(row for row in rows if row["before"] and row["before"]["text"].startswith("def run("))
    assert row["after"] and row["after"]["text"].startswith("def run(")


def test_workspace_rejects_unknown_source() -> None:
    topic = next(t for t in build(ROOT) if t["id"] == "repository")
    topic["guide"]["filePairs"]["base"][0]["after"] = "missing.py"
    with pytest.raises(ValueError, match="Unknown workspace file"):
        build_workspaces(topic)


def test_paired_strategy_keeps_legacy_sides_and_all_roles() -> None:
    topic = next(topic for topic in build(ROOT) if topic["id"] == "strategy")
    guide = topic["guide"]
    assert len(guide["versions"]) == 2
    assert guide["legacyVersionIndices"] == [0, 1, 0, 1]
    assert set(guide["workspaces"]) == {"base"}
    assert {file["name"] for file in guide["versions"][0]["files"]} == {
        "baseline/main.py", "baseline/context.py", "baseline/operations.py",
    }
    assert {file["name"] for file in guide["versions"][1]["files"]} == {
        "pattern/main.py", "pattern/context.py", "pattern/strategies.py", "pattern/interfaces.py",
    }
    contrast = guide["contrasts"][1]
    assert contrast["before"]["code"] == (
        "case Constant(value):\n    return [value for _ in values]\n"
    )
    assert "class Constant:" in contrast["after"]["code"]


def test_paired_example_keeps_shared_sources_and_nested_dependency_links() -> None:
    topic = next(topic for topic in build(ROOT) if topic["id"] == "abstract-factory")
    guide = topic["guide"]
    assert len(guide["versions"]) == 2
    assert "extended" not in guide["pairs"]
    shared = [
        source for source in guide["sources"] if source["name"].startswith("formats/")
    ]
    assert {source["name"] for source in shared} == {
        "formats/json.py",
        "formats/yaml.py",
        "formats/toml.py",
    }
    assert all(len(source["usedBy"]) == 2 for source in shared)
    client = next(
        source for source in guide["sources"] if source["name"] == "pattern/client.py"
    )
    assert "pattern/factories.py" in client["imports"]
    for version in guide["versions"]:
        assert version["files"][0]["name"] == version["entry"]
