from __future__ import annotations

import requests
from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (compatible; CompetitiveIntelCopilot/0.1)"


def fetch_page_text(url: str, timeout: int = 15) -> str:
    """Fetch a URL and return its visible text, stripped of scripts/styles/nav noise."""
    response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    lines = (line.strip() for line in text.splitlines())
    return "\n".join(line for line in lines if line)
