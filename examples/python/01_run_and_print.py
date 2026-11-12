"""Run the Substack Scraper on one newsletter and print its details and one line per post.

Usage:  python 01_run_and_print.py [newsletter]
        newsletter is a name (simonw), an address (simonw.substack.com) or a custom domain.
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

    newsletter = sys.argv[1] if len(sys.argv) > 1 else "simonw.substack.com"
    # includeContent False gives metadata only, which is much faster. Turn it on to get each post's Markdown body.
    run_input = {"publications": [newsletter], "maxPostsPerPublication": 5, "includeContent": False}

    client = ApifyClient(token)
    run = client.actor(ACTOR_ID).call(run_input=run_input, logger=None)
    if run is None or run.status != "SUCCEEDED":
        sys.exit(f"Run did not succeed: {run.status if run else 'no run'} {(run.status_message or '') if run else ''}")

    for item in client.dataset(run.default_dataset_id).iterate_items():
        kind = item["recordType"]
        if kind == "publication_status":
            # A newsletter that could not be read comes back as a free status row.
            print(f"{item['input']}: {item['status']} - {item['message']}")
        elif kind == "publication":
            print(f"{item['publicationName']}: {item['postCount']} posts in the sitemap, paid plans: {item['paidSubscriptionsEnabled']}")
        else:
            print(
                f"{item['postDate'][:10]} | {item['type']} | {item['audience']} | {item['wordcount']} words"
                f" | {item['title']} | {item['url']}"
            )


if __name__ == "__main__":
    main()
