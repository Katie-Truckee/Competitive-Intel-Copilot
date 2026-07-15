from __future__ import annotations

import argparse
import os

from dotenv import load_dotenv

from .config import load_competitors
from .collectors.scraper import fetch_page_text
from .collectors.search import search
from .diff import Change, compute_diff, is_meaningful
from .report import write_report
from .storage import SnapshotStore, slugify
from .synthesize import synthesize_summary


def run() -> None:
    load_dotenv()
    competitors = load_competitors()
    store = SnapshotStore()
    changes: list[Change] = []

    search_enabled = bool(os.environ.get("EXA_API_KEY"))
    if not search_enabled:
        print("[warn] EXA_API_KEY not set — skipping search-based monitoring")

    for competitor in competitors:
        for page in competitor.pages:
            key = slugify(competitor.name, page.label)
            try:
                new_text = fetch_page_text(page.url)
            except Exception as exc:
                print(f"[warn] failed to fetch {competitor.name} / {page.label}: {exc}")
                continue

            old_text = store.load(key)
            store.save(key, new_text)

            if old_text is None:
                print(f"[info] first snapshot for {competitor.name} / {page.label}, nothing to diff yet")
                continue

            diff_text = compute_diff(old_text, new_text)
            if is_meaningful(diff_text):
                changes.append(Change(competitor.name, page.label, page.url, diff_text))
                print(f"[info] change detected: {competitor.name} / {page.label}")

        if search_enabled:
            for query in competitor.search_queries:
                try:
                    results = search(query)
                except Exception as exc:
                    print(f"[warn] search failed for '{competitor.name}' / '{query}': {exc}")
                    continue

                for r in results:
                    changes.append(Change(competitor.name, f"search: {query}", r.url, r.text))
                    print(f"[info] search hit: {competitor.name} / {query} -> {r.url}")

    summary = synthesize_summary(changes)
    report_path = write_report(summary, changes)
    print(f"[info] report written to {report_path}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="competitive-intel")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("run", help="Fetch competitor pages, diff against last snapshot, write a report")

    args = parser.parse_args()
    if args.command == "run":
        run()


if __name__ == "__main__":
    main()
