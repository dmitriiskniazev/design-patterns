"""Deployment layout and complete offline snapshots."""

import json
from pathlib import Path

from design_patterns.site import package


def test_offline_snapshot_contains_every_published_file() -> None:
    root = Path(__file__).resolve().parents[1]
    target = package(root)
    worker = (target / "sw.js").read_text()
    files = json.loads(worker.split("const FILES = ", 1)[1].split(";", 1)[0])
    assert "web/" in files and "./" in files
    assert ".nojekyll" not in files
    assert "course-data.js" in files
    assert not list(target.rglob("*.zip"))
    assert not (target / "examples").exists()
    assert not (target / "lessons.json").exists()
    assert not (target / "assets").exists()
    assert "location.replace" in (target / "web/index.html").read_text()
    for name in files:
        assert (target / name).exists()
    for path in target.rglob("*"):
        if path.is_file() and path.name != "sw.js" and not path.name.startswith("."):
            assert path.relative_to(target).as_posix() in files
    assert "__VERSION__" not in worker
    assert not list(target.rglob("__pycache__"))


def test_manifest_paths_stay_inside_project() -> None:
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "web/manifest.webmanifest").read_text())
    assert manifest["start_url"] == "./"
    assert manifest["scope"] == "./"
    assert manifest["display"] == "standalone"
    assert {icon["sizes"] for icon in manifest["icons"]} == {"192x192", "512x512"}


def test_published_html_references_only_packaged_scripts_and_styles() -> None:
    from html.parser import HTMLParser

    class Resources(HTMLParser):
        paths: list[str]

        def __init__(self) -> None:
            super().__init__()
            self.paths = []

        def handle_starttag(
            self, tag: str, attrs: list[tuple[str, str | None]]
        ) -> None:
            values = dict(attrs)
            if tag == "script" and values.get("src"):
                self.paths.append(values["src"])
            if tag == "link" and values.get("rel") == "stylesheet":
                self.paths.append(values["href"])

    root = Path(__file__).resolve().parents[1]
    target = package(root)
    resources = Resources()
    resources.feed((target / "index.html").read_text())
    for name in resources.paths:
        assert "://" not in name
        assert (target / name).is_file(), name


def test_themes_fonts_and_nested_modules_are_packaged() -> None:
    import re

    root = Path(__file__).resolve().parents[1]
    target = package(root)
    themes = json.loads((target / "src/themes/catalog.json").read_text())
    fonts = json.loads((target / "fonts/catalog.json").read_text())
    palettes = (target / "src/themes/palettes.css").read_text()
    assert len(themes) >= 20
    assert len({theme["id"] for theme in themes}) == len(themes)
    assert {
        "one_light",
        "one_dark",
        "github_light",
        "github_dark",
        "dracula",
        "monokai",
    } <= {theme["id"] for theme in themes}
    for theme in themes:
        assert f':root[data-theme="{theme["id"]}"]' in palettes
    assert len(fonts) == 9
    for font in fonts:
        assert font["faces"]
        for face in font["faces"]:
            assert (target / "fonts" / face["file"]).is_file()
            assert face["russian"]
        assert any((target / "fonts" / font["id"]).glob("*LICEN*")) or any(
            (target / "fonts" / font["id"]).glob("OFL*")
        )
    for module in (target / "src").rglob("*.js"):
        for ref in re.findall(
            r"(?:\bfrom\s+|^\s*import\s*(?:\(\s*)?)[\'\"]([^\'\"]+)[\'\"]",
            module.read_text(),
            re.MULTILINE,
        ):
            assert ref.startswith(".")
            assert (module.parent / ref).resolve().is_file(), (module, ref)
    for css in target.rglob("*.css"):
        for ref in re.findall(r"url\([\'\"]?([^\'\")]+)", css.read_text()):
            assert (css.parent / ref).resolve().is_file(), (css, ref)


def test_verdandi_preserves_keyword_and_string_emphasis(tmp_path: Path) -> None:
    import re

    from design_patterns.themes import build_themes

    root = Path(__file__).resolve().parents[1]
    (tmp_path / "src/themes").mkdir(parents=True)
    build_themes(root, tmp_path)
    css = (tmp_path / "src/themes/palettes.css").read_text()
    for theme in ("verdandi", "verdandi_alter"):
        scope = re.escape(f':root[data-theme="{theme}"] .source-code ')
        keyword = re.search(scope + r"\.k \{([^}]+)\}", css)
        string = re.search(scope + r"\.s2 \{([^}]+)\}", css)
        assert keyword and "font-weight: bold" in keyword.group(1)
        assert string and "font-style: italic" in string.group(1)
        operator = re.search(scope + r"\.o \{([^}]+)\}", css)
        assert operator and "font-weight: bold" in operator.group(1)
        for token in ("nf", "fm", "nc", "nd", "nb", "bp"):
            name = re.search(scope + rf"\.{token} \{{([^}}]+)\}}", css)
            assert name and (
                "#B5BBC0" if theme == "verdandi_alter" else "#212529"
            ) in name.group(1)
