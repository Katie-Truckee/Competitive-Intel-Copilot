from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date, timedelta

import requests

EXA_SEARCH_URL = "https://api.exa.ai/search"


@dataclass
class SearchResult:
    title: str
    url: str
    published_date: str | None
    text: str


class SearchNotConfigured(RuntimeError):
    pass


def search(query: str, num_results: int = 5, lookback_days: int = 14) -> list[SearchResult]:
    """Run a query against Exa, scoped to recent news."""
    api_key = os.environ.get("EXA_API_KEY")
    if not api_key:
        raise SearchNotConfigured("EXA_API_KEY is not set. Add it to .env.")

    start_published_date = (date.today() - timedelta(days=lookback_days)).isoformat()

    response = requests.post(
        EXA_SEARCH_URL,
        headers={"x-api-key": api_key, "Content-Type": "application/json"},
        json={
            "query": query,
            "numResults": num_results,
            "category": "news",
            "startPublishedDate": f"{start_published_date}T00:00:00.000Z",
            "contents": {"text": {"maxCharacters": 2000}},
        },
        timeout=15,
    )
    response.raise_for_status()
    data = response.json()

    return [
        SearchResult(
            title=r.get("title", ""),
            url=r["url"],
            published_date=r.get("publishedDate"),
            text=r.get("text", ""),
        )
        for r in data.get("results", [])
    ]
