// Run the Substack Scraper on one newsletter and print its details and one line per post.
//
// Usage:  node 01-run-and-print.mjs [newsletter]
//         newsletter is a name (simonw), an address (simonw.substack.com) or a custom domain.
// Needs:  APIFY_TOKEN in the environment.
import { ApifyClient } from 'apify-client';

const ACTOR_ID = 'cedarfetch/substack-scraper';

const token = process.env.APIFY_TOKEN;
if (!token) {
    console.error('APIFY_TOKEN is not set. Create a token on the Integrations page of Apify Console and export it first.');
    process.exit(1);
}

const newsletter = process.argv[2] ?? 'simonw.substack.com';
// includeContent false gives metadata only, which is much faster. Turn it on to get each post's Markdown body.
const runInput = { publications: [newsletter], maxPostsPerPublication: 5, includeContent: false };

const client = new ApifyClient({ token });
const run = await client.actor(ACTOR_ID).call(runInput, { log: null });
if (run.status !== 'SUCCEEDED') {
    console.error(`Run did not succeed: ${run.status} ${run.statusMessage ?? ''}`);
    process.exit(1);
}

for await (const item of client.dataset(run.defaultDatasetId).listItems()) {
    if (item.recordType === 'publication_status') {
        // A newsletter that could not be read comes back as a free status row.
        console.log(`${item.input}: ${item.status} - ${item.message}`);
    } else if (item.recordType === 'publication') {
        console.log(`${item.publicationName}: ${item.postCount} posts in the sitemap, paid plans: ${item.paidSubscriptionsEnabled}`);
    } else {
        console.log(
            `${item.postDate.slice(0, 10)} | ${item.type} | ${item.audience} | ${item.wordcount} words`
            + ` | ${item.title} | ${item.url}`,
        );
    }
}
