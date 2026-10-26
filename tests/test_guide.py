import json
from copy import deepcopy
from pathlib import Path

import pytest

from design_patterns.build import build, extract
from design_patterns.comparisons import build_comparison
from design_patterns.guide import build_guide, order_source_files, source_diff

ROOT = Path(__file__).resolve().parents[1]
GUIDES = {
    key: guide
    for filename in (ROOT / "content").glob("guide-*.json")
    for key, guide in json.loads(filename.read_text()).items()
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


@pytest.mark.parametrize("chapter_ids", [[], ["unknown"]])
def test_build_rejects_incomplete_guide_coverage(
    tmp_path: Path, chapter_ids: list[str]
) -> None:
    content = tmp_path / "content"
    content.mkdir()
    (content / "topics.json").write_text(
        json.dumps([{"id": "strategy", "ready": True}])
    )
    (content / "guide-test.json").write_text(
        json.dumps({key: {} for key in chapter_ids})
    )
    with pytest.raises(ValueError, match="Guide coverage mismatch"):
        build(tmp_path)


def test_build_rejects_duplicate_guide_chapter(tmp_path: Path) -> None:
    content = tmp_path / "content"
    content.mkdir()
    (content / "topics.json").write_text(
        json.dumps([{"id": "strategy", "ready": True}])
    )
    for name in ("a", "b"):
        (content / f"guide-{name}.json").write_text('{"strategy": {}}')
    with pytest.raises(ValueError, match="Duplicate guide chapters"):
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
    assert len(guide["contrasts"]) == 2
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
    topics = json.loads(
        (ROOT / "assets/course-data.js")
        .read_text()
        .split("window.COURSE_TOPICS = ", 1)[1]
        .removesuffix(";\n")
    )
    chapters = [topic["guide"] for topic in topics if "guide" in topic]
    assert len(chapters) == 25
    for guide in chapters:
        assert [version["key"] for version in guide["versions"]] == [
            "before",
            "after",
            "beforeExtension",
            "afterExtension",
        ]
        assert guide["pairs"] == {
            "base": {"before": 0, "after": 1},
            "extended": {"before": 2, "after": 3},
        }
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
                    if (ROOT / ref["path"]).with_name(dependency).is_file():
                        assert dependency in {item["name"] for item in version["files"]}
        for row in guide["contrasts"]:
            for side in ("before", "after"):
                assert (
                    row["commonBeforeCode"]
                    + row[side]["difference"]
                    + row["commonAfterCode"]
                ) == row[side]["code"]
                assert row[side]["html"]


@pytest.mark.parametrize(
    ("before", "after", "kinds"),
    [
        (
            "value = 1\nprint(value)\n",
            "value = 2\nprint(value)\n",
            ["removed", "added", "equal"],
        ),
        ("", 'print("<new>")\n', ["added"]),
        ("value = 1\n", "", ["removed"]),
        ("\nvalue = 1\n\n", "\nvalue = 1\n\n", ["equal", "equal", "equal"]),
        ("value = 1", "value = 2", ["removed", "added"]),
    ],
)
def test_source_diff_preserves_both_sources(
    before: str, after: str, kinds: list[str]
) -> None:
    rows = source_diff(before, after)
    assert [row["kind"] for row in rows] == kinds
    assert "".join(row["text"] for row in rows if row["kind"] != "added") == before
    assert "".join(row["text"] for row in rows if row["kind"] != "removed") == after
    assert [row["beforeLine"] for row in rows if row["beforeLine"]] == list(
        range(1, len(before.splitlines()) + 1)
    )
    assert [row["afterLine"] for row in rows if row["afterLine"]] == list(
        range(1, len(after.splitlines()) + 1)
    )
    assert all("<new>" not in row["html"] for row in rows)


def test_extension_diff_pairs_entrypoints_and_keeps_copyable_sources() -> None:
    topic = next(
        topic
        for topic in json.loads((ROOT / "content/topics.json").read_text())
        if topic["id"] == "strategy"
    )
    topic["guide"] = deepcopy(GUIDES["strategy"])
    build_comparison(ROOT, topic["fileComparison"])
    build_guide(ROOT, topic, extract)
    guide = topic["guide"]
    sources = {source["id"]: source for source in guide["sources"]}
    for base_index, extension_index in ((0, 2), (1, 3)):
        base, extension = (
            guide["versions"][base_index],
            guide["versions"][extension_index],
        )
        entry = next(
            ref for ref in extension["files"] if ref["name"] == extension["entry"]
        )
        assert entry["diff"]["baseName"] == base["entry"]
        assert entry["change"] == "modified"
        assert entry["role"] == (
            "Запуск расширенного примера "
            + ("без паттерна" if extension_index == 2 else "с паттерном")
        )
        for ref in extension["files"]:
            source = sources[ref["id"]]
            assert source["code"] == (ROOT / ref["path"]).read_text()
            assert "diff" not in source
            assert (
                "".join(
                    row["text"]
                    for row in ref["diff"]["rows"]
                    if row["kind"] != "removed"
                )
                == source["code"]
            )
            if ref["change"] == "unchanged":
                assert all(row["kind"] == "equal" for row in ref["diff"]["rows"])
