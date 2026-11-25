# Substack scraper: examples in Python, Node.js and cURL for newsletter posts as Markdown

Working examples for downloading the public posts of any Substack newsletter, on `name.substack.com` or a custom domain, as Markdown, plain text or HTML, with the [Substack Scraper Actor](https://apify.com/cedarfetch/substack-scraper) on Apify. Each post comes with title, date, authors, audience, paywall flag, likes, comment and restack counts and word count, and with change tracking on you get a feed of new and updated posts.

The scripts call the Actor from code with the official Apify API client. If you would rather not use a paid tool, the last section names the public Substack endpoints it reads, so you can fetch them yourself.

## Quick start

You need an Apify API token (Integrations page in Apify Console, https://console.apify.com/account/integrations). Apify's free plan includes monthly platform credit, which is enough to try this.

**Python** (3.11 or newer, required by `apify-client` 3.x):

```bash
cd examples/python
pip install -r requirements.txt
export APIFY_TOKEN=your_token_here      # Windows cmd: set APIFY_TOKEN=your_token_here
python 01_run_and_print.py simonw.substack.com
```

On Windows, run `set PYTHONUTF8=1` first if the console fails on non-ASCII titles.

**Node.js** (18 or newer):

```bash
cd examples/node
npm install
export APIFY_TOKEN=your_token_here
node 01-run-and-print.mjs simonw.substack.com
```

**cURL** (no install, one HTTP call):

```bash
export APIFY_TOKEN=your_token_here
bash examples/curl/run.sh
```

Metadata-only runs are fast (about 25 posts per request). With bodies the Actor makes one request per post at a polite pace, about 1.4 seconds per post at the defaults, so `examples/curl/input.json` asks for five free posts and finishes in under a minute. Real rows are in [`sample-output/sample.json`](sample-output/sample.json).

## What is in this repository

| Path | What it does |
|---|---|
| `examples/python/01_run_and_print.py` | Run the Actor on one newsletter, print its details and one line per post. |
| `examples/python/02_archive_to_markdown.py` | Save free posts as Markdown files with a small front matter header. |
| `examples/python/03_new_posts_feed.py` | Print only posts that are new or changed since the last run, for a list of newsletters. |
| `examples/node/01-run-and-print.mjs`, `02-archive-to-markdown.mjs`, `03-new-posts-feed.mjs` | The same three scripts as ES modules. |
| `examples/curl/run.sh`, `input.json` | One-call version using the `run-sync-get-dataset-items` endpoint. |
| `sample-output/sample.json` | 7 real rows (1 publication row and 6 posts, with Markdown bodies), shortened (see below). |

The token is always read from the `APIFY_TOKEN` environment variable. Nothing is hard-coded.

## Input options

Only `publications` is required. You can paste `simonw`, `simonw.substack.com`, `https://simonw.substack.com/archive`, a custom domain such as `www.lennysnewsletter.com`, or a single post URL (only that post is read). Links on `substack.com` itself (profiles, the app feed, search, Notes) are rejected: use the newsletter's own address. The options used most often:

| Field | Default | What it does |
|---|---|---|
| `publications` | (required) | Newsletters or post URLs. |
| `maxPostsPerPublication` | 0 (all) | Stop after this many matching posts per newsletter. |
| `sort` | `new` | `new`: newest first. `top`: most popular first, as Substack ranks them. |
| `coverage` | `archive_and_sections` | `archive_and_sections`: the main archive plus sections the publisher hid from it. `everything`: also any other post in the public sitemap (one request per such post). `archive`: the main archive only. |
| `postedAfter`, `postedBefore` | none | ISO date or relative value (`30 days`, `2 weeks`, `24 hours`, `6 months`). |
| `includeContent` | true | Fetch each post's body (one request per post). Off: metadata only. |
| `contentFormat` | `markdown` | `markdown`, `text` or `html`. |
| `postTypes` | all | Any of `newsletter`, `podcast`, `thread`, `video`. |
| `onlyFree` | false | Skip paywalled and subscriber-only posts. |
| `includePublicationInfo` | true | One free `publication` row per newsletter. |
| `trackChanges` | false | Label every post `new`, `updated`, `unchanged` or `removed` against the previous run. |
| `changesOnly` | false | With tracking on, skip unchanged posts. |
| `snapshotStoreName` | `substack-scraper-snapshots` | Named key-value store for snapshots. Use different names for independent feeds. |

The Actor has more options (`concurrency`, `requestDelayMs`, `maxRetries` and others). See its [listing](https://apify.com/cedarfetch/substack-scraper) for the full input reference.

## Output

Rows go to the default dataset. `recordType` is `post`, `publication` (one free info row per newsletter, before its posts) or `publication_status` (a newsletter that could not be read; free). A publication row from [`sample-output/sample.json`](sample-output/sample.json), shortened:

```json
{
    "recordType": "publication",
    "publicationDomain": "simonw.substack.com",
    "publicationName": "Simon Willison’s Newsletter",
    "url": "https://simonw.substack.com",
    "description": "AI, LLMs, web engineering, open source, data science, Datasette, SQLite, Python and more",
    "authorName": "Simon Willison",
    "authorHandle": "simonw",
    "language": "en",
    "type": "newsletter",
    "paidSubscriptionsEnabled": false,
    "monthlyPrice": null,
    "annualPrice": null,
    "priceCurrency": null,
    "hasPodcast": false,
    "firstPostDate": "2023-03-13T20:19:30.907Z",
    "postCount": 198,
    "scrapedAt": "2026-11-12T00:46:50.581Z"
}
```

A post row (same file), shortened:

```json
{
    "recordType": "post",
    "publicationDomain": "simonw.substack.com",
    "publicationName": "Simon Willison’s Newsletter",
    "postId": 224270395,
    "slug": "locating-the-source-of-a-mysterious",
    "url": "https://simonw.substack.com/p/locating-the-source-of-a-mysterious",
    "title": "Locating the source of a mysterious beep with Claude",
    "subtitle": "Plus Hide your slop PR descriptions behind <details><summary> - and Fable 5.2 and Muse Ember",
    "type": "newsletter",
    "audience": "everyone",
    "isPaywalled": false,
    "requiresPaidSubscription": false,
    "contentAvailable": "full",
    "postDate": "2026-11-10T07:41:51.409Z",
    "updatedAt": "2026-11-10T07:50:41.642Z",
    "authors": [
        {
            "name": "Simon Willison",
            "handle": "simonw"
        }
    ],
    "wordcount": 5034,
    "reactionCount": 29,
    "commentCount": 11,
    "restackCount": 2,
    "tags": [
        "alms",
        "ai"
    ],
    "language": "en",
    "contentFormat": "markdown",
    "content": "In this newsletter:\n\n- Locating the source of a mysterious beep with Claude\n- Hide your slop PR descriptions behind \\<details>\\<summary>\n\nPlus 2 links, 3 quotations, 4 releases, 1 research report, 1 tool, and 3 comments\n\n---\n\n**Sponsor mess...",
    "source": "post",
    "scrapedAt": "2026-11-12T00:46:50.581Z"
}
```

The sample file comes from running the Actor itself against one public newsletter on 2026-11-11 (free posts only) and keeps every field of each row. Only length was cut: long text, including the Markdown body, is truncated with `...` and lists show their first few entries.

How to read the main fields:

- `audience` is `everyone` (free), `only_subscribers` (free signup required), `only_paid` or `founding`. `isPaywalled` is true for anything but `everyone`.
- `contentAvailable` is `full` (free post, body included), `preview` (gated post: only the public preview) or `none` (content off, or the post has no body). Check it before treating `content` as a whole post.
- `wordcount` is the full post's length as Substack reports it, also for paywalled posts, so you can see how much of a post the preview covers.
- `commentCount` is a number only. Comment text and commenters are never collected.
- Podcast posts have `type: "podcast"`, `podcastUrl` and `podcastDurationSecs`.

With change tracking on, post rows also carry `changeType` (`new`, `updated`, `unchanged`, `removed`), `changes` (for example `title_changed`, `audience_changed`, `wordcount_changed`), `previousTitle`, `previousAudience`, `previousWordcount` and `previousUpdatedAt`.

## Recipes

**Newsletter archive to Markdown files.** [`02_archive_to_markdown.py`](examples/python/02_archive_to_markdown.py) uses `onlyFree: true` and `contentFormat: "markdown"` and writes one `.md` file per post, with title, URL, date, authors and publication in a front matter header. Markdown keeps headings, links, lists, quotes, code and footnotes; subscribe buttons and share widgets are dropped.

**A feed of new posts across many newsletters.** [`03_new_posts_feed.py`](examples/python/03_new_posts_feed.py) uses `trackChanges`, `changesOnly` and `postedAfter: "14 days"`. The first run labels every post of the last 14 days `new` because it creates the baseline. Schedule the same input daily in Apify Console and each run delivers only posts that are new or whose title, subtitle, audience, slug or word count changed, and you pay only for those. A day with nothing new delivers zero post rows and succeeds.

**A RAG or search corpus.** Run with `onlyFree: true` and `contentFormat: "markdown"`, use one document per row (`content` as the text; `title`, `url`, `postDate`, `authors` and `publicationName` as metadata) and split on Markdown headings. If you include paywalled posts, filter on `contentAvailable == "full"` so previews do not end up in the corpus as if they were whole posts. To keep it fresh, add change tracking and re-embed rows with `changeType` `new` or `updated`.

**Podcast episodes only, without bodies.** `postTypes: ["podcast"]`, `includeContent: false`, `coverage: "everything"` (many publishers hide their podcast from the main archive). Rows carry `podcastUrl` and `podcastDurationSecs`.

**Sponsorship research.** With `includePublicationInfo` on, each newsletter gets a publication row with `paidSubscriptionsEnabled`, `plans`, `monthlyPrice`, `annualPrice`, `postCount` and `hasPodcast`. Subscriber counts are not included.

## Pricing

The Actor uses pay-per-event pricing. Prices shown on the [Apify listing](https://apify.com/cedarfetch/substack-scraper) when this repository was written (2026-11-11):

- Post row: $0.001 each (from $1.00 per 1,000 posts), with or without the body. `removed` rows from change tracking count as post rows.
- Actor start: $0.00005 per GB of run memory, minimum one event.
- Publication info rows and rows for newsletters that could not be read are free. With `changesOnly`, unchanged posts are not delivered and not charged.

Apify's free plan includes monthly platform credit that you can use to try the Actor. Prices can change, so check the Pricing tab of the listing before you schedule anything. Set Maximum cost per run in the run options, or `maxTotalChargeUsd` in the API client, to cap spending.

## Limits and honest caveats

- Paywalled posts are preview only. The Actor never logs in and never tries to get around a paywall. For paid and subscriber-only posts you get what an anonymous visitor sees: usually the opening of the post, sometimes nothing beyond the title and description.
- No comments and no subscriber or reader data. Comment counts only.
- No discovery or search. You tell it which newsletters to read. Substack's global search, category, leaderboard and profile pages live on substack.com and are not used.
- Notes, chats and live streams are not posts and are not included.
- Posts a publisher hides from every listing are only found with `coverage: "everything"`, which costs one request per such post. On some newsletters (often those with a podcast) that is hundreds of extra requests.
- Substack throttles clients that read fast. The defaults stay under it in testing. If you raise `concurrency` or lower `requestDelayMs`, the Actor slows itself down on the first 429, and a newsletter that stays throttled is reported as `rate_limited` with everything read so far delivered. Large archives with bodies take time: about 1.4 seconds per post at the defaults.
- `sort: "top"` is Substack's own popularity order. With `postedAfter` it cannot stop early, so it reads the whole archive listing.
- Explicit post URLs bypass `postedAfter`, `postedBefore`, `postTypes`, `onlyFree` and the cap.
- Removed posts are only reported by runs that read the whole archive (no `postedAfter`, no cap). The feed example above uses `postedAfter`, so it does not report removals.
- Markdown conversion handles what Substack's editor produces. Unusual embeds (polls, audio players, paid-only widgets) are dropped or reduced to a link.
- The sync endpoint used by `run.sh` answers 408 after 300 seconds. For large archives use the Python or Node examples, which wait for the run to finish.
- Republishing other people's posts usually needs their permission. You are responsible for how you use the data, for respecting copyright and each newsletter's terms.

## Guide

Step-by-step write-up of the underlying endpoints, their limits and a do-it-yourself version: [How to pull a Substack newsletter's posts as Markdown](https://dev.to/cedarfetch/how-to-pull-a-substack-newsletters-posts-as-markdown-5c83).

## Do it yourself (no paid tool)

Each Substack newsletter serves a few public endpoints to every visitor's browser. The Actor reads these:

| Endpoint | What you get |
|---|---|
| `https://<newsletter>/api/v1/archive?sort=new&limit=25` | Post list (metadata, no body), 25 per page at most. The answer has `posts` and `nextCursor`; pass `&cursor=<nextCursor>` for the next page. `sort=top` ranks by popularity. |
| `https://<newsletter>/api/v1/posts/<slug>` | One post, with `body_html` (the full body for free posts, a public preview for gated posts). |
| `https://<newsletter>/sitemap.xml` | Every public post URL, including posts hidden from the archive listing. |

A minimal Python version, standard library only:

```python
import json
import urllib.parse
import urllib.request

host = "simonw.substack.com"


def get(url):
    request = urllib.request.Request(url, headers={"User-Agent": "newsletter-reader/1.0", "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


# Archive listing: metadata only, newest first, up to 25 posts per page.
page = get(f"https://{host}/api/v1/archive?sort=new&limit=5")
for post in page["posts"]:
    print(post["post_date"][:10], post["audience"], post["title"], post["canonical_url"])

# Follow page["nextCursor"] for the next page.
cursor = urllib.parse.quote(page["nextCursor"])
older = get(f"https://{host}/api/v1/archive?sort=new&limit=5&cursor={cursor}")

# One post, with its body as HTML.
slug = page["posts"][0]["slug"]
full = get(f"https://{host}/api/v1/posts/{slug}")
print(full["title"], len(full["body_html"]), "characters of HTML")
```

Substack throttles fast clients, so pause between requests and back off on 429. Converting `body_html` into clean Markdown is the part that takes work (footnotes, embeds, image captions, buttons). What the paid Actor adds on top: that Markdown conversion, sections hidden from the archive, the sitemap pass for hidden posts, custom-domain detection, retries and slowdown on rate limits, per-newsletter error reporting, and the snapshot comparison behind `changeType`. If you only need a few posts as HTML, the endpoints above are enough.

## Related

Other example repositories from Cedarfetch Labs:

- [shopify-store-scraper-examples](https://github.com/cedarfetch/shopify-store-scraper-examples): Shopify product, price and stock data
- [ats-jobs-scraper-examples](https://github.com/cedarfetch/ats-jobs-scraper-examples): Greenhouse, Lever, Ashby and other applicant-tracking-system job boards
- [remote-jobs-scraper-examples](https://github.com/cedarfetch/remote-jobs-scraper-examples): remote jobs from seven public boards
- [google-trending-searches-examples](https://github.com/cedarfetch/google-trending-searches-examples): what is trending on Google right now, per country

Listing: https://apify.com/cedarfetch/substack-scraper

Not affiliated with Substack.

Maintained by Cedarfetch Labs, the developer of this Actor.
