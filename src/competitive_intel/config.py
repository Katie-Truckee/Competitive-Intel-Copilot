from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "competitors.yaml"


@dataclass
class Page:
    label: str
    url: str


@dataclass
class Competitor:
    name: str
    pages: list[Page] = field(default_factory=list)
    search_queries: list[str] = field(default_factory=list)


def load_competitors(path: Path = DEFAULT_CONFIG_PATH) -> list[Competitor]:
    raw = yaml.safe_load(path.read_text())
    competitors = []
    for entry in raw.get("competitors", []):
        pages = [Page(**p) for p in entry.get("pages", [])]
        competitors.append(
            Competitor(
                name=entry["name"],
                pages=pages,
                search_queries=entry.get("search_queries", []),
            )
        )
    return competitors
