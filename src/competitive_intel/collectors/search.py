from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class SearchResult:
    title: str
    snippet: str
    url: str


class SearchProviderNotConfigured(RuntimeError):
    pass


def search(query: str) -> list[SearchResult]:
    """Run a query against the configured search provider.

    Pick a provider (e.g. Serper, Exa, Bing) and implement the request here.
    Set SEARCH_API_PROVIDER / SEARCH_API_KEY in .env once decided.
    """
    provider = os.environ.get("SEARCH_API_PROVIDER")
    api_key = os.environ.get("SEARCH_API_KEY")

    if not provider or not api_key:
        raise SearchProviderNotConfigured(
            "No search provider configured. Set SEARCH_API_PROVIDER and SEARCH_API_KEY "
            "in .env, then implement the request for that provider in search.py."
        )

    raise NotImplementedError(f"No implementation wired up yet for provider '{provider}'.")
