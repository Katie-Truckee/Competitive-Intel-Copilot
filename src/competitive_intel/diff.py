from __future__ import annotations

import difflib
from dataclasses import dataclass


@dataclass
class Change:
    competitor: str
    label: str
    url: str
    diff_text: str


def compute_diff(old: str, new: str) -> str:
    diff_lines = difflib.unified_diff(
        old.splitlines(),
        new.splitlines(),
        lineterm="",
        n=1,
    )
    return "\n".join(diff_lines)


def is_meaningful(diff_text: str) -> bool:
    """A diff is meaningful if it contains actual added/removed content lines."""
    return any(
        (line.startswith("+") or line.startswith("-"))
        and not line.startswith(("+++", "---"))
        for line in diff_text.splitlines()
    )
