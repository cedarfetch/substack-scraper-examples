// Print the posts that are new or changed since the previous run, for a list of newsletters.
//
// The first run labels every post of the last 14 days "new" (it creates the baseline). Run it again
// later, or put the same input on a schedule, and you only get the differences.
//
// Usage:  node 03-new-posts-feed.mjs [newsletter ...]
// Needs:  APIFY_TOKEN in the environment.
import { ApifyClient } from 'apify-client';

const ACTOR_ID = 'cedarfetch/substack-scraper';

const token = process.env.APIFY_TOKEN;
if (!token) {
    console.error('APIFY_TOKEN is not set. Create a token on the Integrations page of Apify Console and export it first.');
    process.exit(1);
}

const newsletters = process.argv.length > 2
    ? process.argv.slice(2)
    : ['simonw.substack.com', 'www.lennysnewsletter.com', 'www.noahpinion.blog'];
const runInput = {
    publications: newsletters,
    postedAfter: '14 days',
    includeContent: false,
    includePublicationInfo: false,
    trackChanges: true,
    changesOnly: true,
    snapshotStoreName: 'new-posts-example',
};

const client = new ApifyClient({ token });
const run = await client.actor(ACTOR_ID).call(runInput, { log: null });
if (run.status !== 'SUCCEEDED') {
    console.error(`Run did not succeed: ${run.status} ${run.statusMessage ?? ''}`);
    process.exit(1);
}

let count = 0;
for await (const item of client.dataset(run.defaultDatasetId).listItems()) {
    if (item.recordType !== 'post') {
        if (item.recordType === 'publication_status') console.log(`${item.input}: ${item.status} - ${item.message}`);
        continue;
    }
    count += 1;
    let what = (item.changeType ?? 'post').toUpperCase();
    if (item.changeType === 'updated') what += ` (${(item.changes ?? []).join(', ')})`;
    const lock = item.isPaywalled ? ' [paywalled]' : '';
    console.log(`${what} ${item.postDate.slice(0, 10)} ${item.publicationName}: ${item.title}${lock} ${item.url}`);
}
console.log(`${count} new or updated posts since the last run`);
