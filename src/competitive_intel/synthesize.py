from __future__ import annotations

import os

from anthropic import Anthropic

from .diff import Change

SYSTEM_PROMPT = """You are a competitive intelligence analyst. You will be given a list of \
detected changes on competitors' public pages and/or search results. Write a concise executive \
summary covering: what changed, why it likely matters, and 2-3 recommended actions. Use markdown \
with a heading per competitor."""


def synthesize_summary(changes: list[Change]) -> str:
    if not changes:
        return "No meaningful competitor changes detected in this run."

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set. Add it to .env.")

    client = Anthropic(api_key=api_key)

    changes_block = "\n\n".join(
        f"## {c.competitor} — {c.label} ({c.url})\n```diff\n{c.diff_text}\n```" for c in changes
    )

    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": changes_block}],
    )
    return response.content[0].text
