"""Package the course for GitHub Pages, including an atomic offline snapshot."""

import hashlib
import json
import shutil
import struct
import zlib
from pathlib import Path

from design_patterns.build import build


def icon(size: int) -> bytes:
    """Draw a simple two-column code mark as a dependency-free PNG."""
    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))

    rows = bytearray()
    for y in range(size):
        rows.append(0)
        for x in range(size):
            mark = (size // 4 <= x < size * 3 // 8 or size * 5 // 8 <= x < size * 3 // 4) and size // 4 <= y < size * 3 // 4
            rows.extend((121, 176, 163) if mark else (32, 38, 42))
    header = struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b"")


def package(root: Path) -> Path:
    build(root)
    target = root / ".build/site"
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    for directory in ("web", "assets"):
        shutil.copytree(root / directory, target / directory)
    for source in (root / "examples").rglob("*.py"):
        destination = target / source.relative_to(root)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    for size in (180, 192, 512):
        (target / f"assets/icon-{size}.png").write_bytes(icon(size))
    (target / "index.html").write_text('<!doctype html><html lang="ru"><meta charset="utf-8"><title>Паттерны</title><script>location.replace("web/"+location.search+location.hash)</script><a href="web/">Открыть курс</a></html>')
    (target / ".nojekyll").touch()
    files = sorted(
        path for path in target.rglob("*")
        if path.is_file() and not path.name.startswith(".")
    )
    digest = hashlib.sha256()
    for path in files:
        digest.update(path.relative_to(target).as_posix().encode())
        digest.update(path.read_bytes())
    template = (root / "web/service-worker.js").read_text()
    digest.update(template.encode())
    paths = [path.relative_to(target).as_posix() for path in files]
    worker = template.replace('"__VERSION__"', json.dumps(digest.hexdigest()[:20])).replace('"__FILES__"', json.dumps(paths + ["./", "web/"]))
    (target / "sw.js").write_text(worker)
    return target


def main() -> None:
    print(f"Pages site: {package(Path.cwd())}")
