from __future__ import annotations

from datetime import date
from pathlib import Path

from .diff import Change

DEFAULT_REPORT_DIR = Path(__file__).resolve().parents[2] / "data" / "reports"


def write_report(summary: str, changes: list[Change], out_dir: Path = DEFAULT_REPORT_DIR) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / f"{date.today().isoformat()}.md"

    lines = [f"# Competitive Intel Report — {date.today().isoformat()}", "", summary, ""]
    if changes:
        lines += ["## Raw changes", ""]
        for c in changes:
            lines += [f"### {c.competitor} — {c.label}", f"<{c.url}>", "", "```diff", c.diff_text, "```", ""]

    report_path.write_text("\n".join(lines))
    return report_path
