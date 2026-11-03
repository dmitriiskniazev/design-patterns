"""Filesystem boundaries must match the two independent teaching axes."""

import ast
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TOPICS = json.loads((ROOT / "web/lessons.json").read_text())
ADDITIONS = [
    ("adapter", "adaptee.py", "SecondAdaptee"),
    ("adapter", "adapter.py", "SecondAdapter"),
    ("bridge", "implementation.py", "ImplementationB"),
    ("chain-of-responsibility", "operations.py", "second"),
    ("command", "command.py", "Double"),
    ("composite", "component.py", "RepeatedComponent"),
    ("decorator", "decorators.py", "DoubleDecorator"),
    ("dependency-injection", "provider.py", "DoubleProvider"),
    ("facade", "subsystems.py", "SubsystemC"),
    ("facade", "facade.py", "ExtendedFacade"),
    ("factory-method", "creator.py", "CreatorB"),
    ("factory-method", "product.py", "ProductB"),
    ("flyweight", "factory.py", "PairFactory"),
    ("interpreter", "expression.py", "Sum"),
    ("iterator", "collection.py", "reverse"),
    ("observer", "callbacks.py", "double"),
    ("repository", "repository.py", "ListRepository"),
    ("state", "states.py", "C"),
    ("template-method", "template.py", "B"),
    ("visitor", "visitor.py", "DoubleVisitor"),
]


def test_topics_follow_their_declared_comparison_layout() -> None:
    for topic in TOPICS:
        if "beforeExtension" not in topic["fileComparison"]:
            directory = ROOT / topic["fileComparison"]["before"]["directory"]
            assert not (directory / "base").exists()
            assert not (directory / "extended").exists()
            assert (directory / "test_example.py").is_file()
            for approach in ("baseline", "pattern"):
                assert (directory / approach / "main.py").is_file()
                assert not (directory / approach / "formats").exists()
            assert topic["fileComparison"]["after"]["directory"] == (
                topic["fileComparison"]["before"]["directory"]
            )
            for key, approach in (("before", "baseline"), ("after", "pattern")):
                group = topic["fileComparison"][key]
                assert group["module"] == f"{approach}.main"
                assert group["entry"] == f"{approach}/main.py"
                assert approach in group["sources"]
            if topic["id"] == "abstract-factory":
                assert {path.stem for path in (directory / "formats").glob("*.py")} == {
                    "__init__", "json", "yaml", "toml",
                }
            continue
        directory = ROOT / "examples" / topic["id"]
        assert {p.name for p in directory.iterdir()} == {"base", "extended"}
        expected = set()
        for stage in ("base", "extended"):
            assert {p.name for p in (directory / stage).iterdir()} == {
                "without_pattern",
                "with_pattern",
            }
            for approach in ("without_pattern", "with_pattern"):
                leaf = directory / stage / approach
                assert (leaf / "main.py").is_file()
                assert (leaf / "test_example.py").is_file()
                assert not list(leaf.glob("*pattern*.py"))
                expected.add(leaf.relative_to(ROOT).as_posix())
        groups = topic["fileComparison"]
        assert {
            groups[key]["directory"]
            for key in ("before", "after", "beforeExtension", "afterExtension")
        } == expected


@pytest.mark.parametrize(("topic", "filename", "addition"), ADDITIONS)
def test_new_participant_is_only_in_extension(
    topic: str, filename: str, addition: str
) -> None:
    def names(stage: str) -> set[str]:
        source = ROOT / "examples" / topic / stage / "with_pattern" / filename
        return {
            node.name
            for node in ast.parse(source.read_text()).body
            if isinstance(node, (ast.ClassDef, ast.FunctionDef))
        }

    assert addition not in names("base")
    assert addition in names("extended")


def test_flyweight_variant_field_is_an_extension() -> None:
    for approach in ("without_pattern", "with_pattern"):
        base = ROOT / "examples/flyweight/base" / approach / "state.py"
        extended = ROOT / "examples/flyweight/extended" / approach / "state.py"
        assert "variant:" not in base.read_text()
        assert "variant:" in extended.read_text()
