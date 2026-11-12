"""Print the posts that are new or changed since the previous run, for a list of newsletters.

The first run labels every post of the last 14 days "new" (it creates the baseline). Run it again
later, or put the same input on a schedule, and you only get the differences.

Usage:  python 03_new_posts_feed.py [newsletter ...]
Needs:  APIFY_TOKEN in the environment.
"""
import os
import sys

from apify_client import ApifyClient

ACTOR_ID = "cedarfetch/substack-scraper"


def main() -> None:
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("APIFY_TOKEN is not set. Create a token on the Integrations page of Apify Console and export it first.")

    newsletters = sys.argv[1:] or ["simonw.substack.com", "www.lennysnewsletter.com", "www.noahpinion.blog"]
    run_input = {
        "publications": newsletters,
        "postedAfter": "14 days",
        "includeContent": False,
        "includePublicationInfo": False,
        "trackChanges": True,
        "changesOnly": True,
        "snapshotStoreName": "new-posts-example",
    }

    client = ApifyClient(token)
    run = client.actor(ACTOR_ID).call(run_input=run_input, logger=None)
    if run is None or run.status != "SUCCEEDED":
        sys.exit(f"Run did not succeed: {run.status if run else 'no run'} {(run.status_message or '') if run else ''}")

    count = 0
    for item in client.dataset(run.default_dataset_id).iterate_items():
        if item["recordType"] != "post":
            if item["recordType"] == "publication_status":
                print(f"{item['input']}: {item['status']} - {item['message']}")
            continue
        count += 1
        what = (item.get("changeType") or "post").upper()
        if item.get("changeType") == "updated":
            what += " (" + ", ".join(item["changes"] or []) + ")"
        lock = " [paywalled]" if item["isPaywalled"] else ""
        print(f"{what} {item['postDate'][:10]} {item['publicationName']}: {item['title']}{lock} {item['url']}")
    print(f"{count} new or updated posts since the last run")


if __name__ == "__main__":
    main()
