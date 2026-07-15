from __future__ import annotations

import re
from pathlib import Path

DEFAULT_SNAPSHOT_DIR = Path(__file__).resolve().parents[2] / "data" / "snapshots"


def slugify(*parts: str) -> str:
    slug = "-".join(parts).lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    return slug


class SnapshotStore:
    def __init__(self, directory: Path = DEFAULT_SNAPSHOT_DIR):
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)

    def _path(self, key: str) -> Path:
        return self.directory / f"{key}.txt"

    def load(self, key: str) -> str | None:
        path = self._path(key)
        return path.read_text() if path.exists() else None

    def save(self, key: str, content: str) -> None:
        self._path(key).write_text(content)
