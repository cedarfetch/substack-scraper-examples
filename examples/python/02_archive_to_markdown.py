"""Save the free posts of a newsletter as Markdown files, one file per post, with a small front matter header.

Paid and subscriber-only posts are skipped: the Actor only ever sees the public preview of those.

Usage:  python 02_archive_to_markdown.py [newsletter] [out_dir] [max_posts]
        max_posts 0 means the whole archive (you pay per post row).
Needs:  APIFY_TOKEN in the environment.
"""
import json
import os
from pathlib import Path
import re
import sys

from apify_client import ApifyClient

ACTOR_ID = "cedarfetch/substack-scraper"


def main() -> None:
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("APIFY_TOKEN is not set. Create a token on the Integrations page of Apify Console and export it first.")

    newsletter = sys.argv[1] if len(sys.argv) > 1 else "simonw.substack.com"
    out_dir = Path(sys.argv[2] if len(sys.argv) > 2 else "posts")
    max_posts = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    run_input = {
        "publications": [newsletter],
        "maxPostsPerPublication": max_posts,
        "onlyFree": True,
        "contentFormat": "markdown",
        "includePublicationInfo": False,
    }

    client = ApifyClient(token)
    run = client.actor(ACTOR_ID).call(run_input=run_input, logger=None)
    if run is None or run.status != "SUCCEEDED":
        sys.exit(f"Run did not succeed: {run.status if run else 'no run'} {(run.status_message or '') if run else ''}")

    out_dir.mkdir(parents=True, exist_ok=True)
    saved = 0
    for item in client.dataset(run.default_dataset_id).iterate_items():
        if item["recordType"] != "post":
            if item["recordType"] == "publication_status":
                print(f"{item['input']}: {item['status']} - {item['message']}")
            continue
        if item["contentAvailable"] != "full":
            continue  # a preview is not a whole post
        authors = ", ".join(author["name"] for author in item["authors"] or [])
        header = [
            "---",
            f"title: {json.dumps(item['title'], ensure_ascii=False)}",
            f"url: {item['url']}",
            f"date: {item['postDate']}",
            f"authors: {json.dumps(authors, ensure_ascii=False)}",
            f"publication: {json.dumps(item['publicationName'], ensure_ascii=False)}",
            "---",
            "",
        ]
        name = re.sub(r"[^A-Za-z0-9._-]+", "-", f"{item['postDate'][:10]}-{item['slug']}")
        (out_dir / f"{name}.md").write_text("\n".join(header) + (item["content"] or "") + "\n", encoding="utf-8")
        saved += 1
    print(f"Saved {saved} posts to {out_dir}/")


if __name__ == "__main__":
    main()
