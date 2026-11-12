// Save the free posts of a newsletter as Markdown files, one file per post, with a small front matter header.
//
// Paid and subscriber-only posts are skipped: the Actor only ever sees the public preview of those.
//
// Usage:  node 02-archive-to-markdown.mjs [newsletter] [outDir] [maxPosts]
//         maxPosts 0 means the whole archive (you pay per post row).
// Needs:  APIFY_TOKEN in the environment.
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { ApifyClient } from 'apify-client';

const ACTOR_ID = 'cedarfetch/substack-scraper';

const token = process.env.APIFY_TOKEN;
if (!token) {
    console.error('APIFY_TOKEN is not set. Create a token on the Integrations page of Apify Console and export it first.');
    process.exit(1);
}

const newsletter = process.argv[2] ?? 'simonw.substack.com';
const outDir = process.argv[3] ?? 'posts';
const maxPosts = Number(process.argv[4] ?? 10);
const runInput = {
    publications: [newsletter],
    maxPostsPerPublication: maxPosts,
    onlyFree: true,
    contentFormat: 'markdown',
    includePublicationInfo: false,
};

const client = new ApifyClient({ token });
const run = await client.actor(ACTOR_ID).call(runInput, { log: null });
if (run.status !== 'SUCCEEDED') {
    console.error(`Run did not succeed: ${run.status} ${run.statusMessage ?? ''}`);
    process.exit(1);
}

mkdirSync(outDir, { recursive: true });
let saved = 0;
for await (const item of client.dataset(run.defaultDatasetId).listItems()) {
    if (item.recordType !== 'post') {
        if (item.recordType === 'publication_status') console.log(`${item.input}: ${item.status} - ${item.message}`);
        continue;
    }
    if (item.contentAvailable !== 'full') continue; // a preview is not a whole post
    const authors = (item.authors ?? []).map((author) => author.name).join(', ');
    const header = [
        '---',
        `title: ${JSON.stringify(item.title)}`,
        `url: ${item.url}`,
        `date: ${item.postDate}`,
        `authors: ${JSON.stringify(authors)}`,
        `publication: ${JSON.stringify(item.publicationName)}`,
        '---',
        '',
    ];
    const name = `${item.postDate.slice(0, 10)}-${item.slug}`.replace(/[^A-Za-z0-9._-]+/g, '-');
    writeFileSync(join(outDir, `${name}.md`), header.join('\n') + (item.content ?? '') + '\n', 'utf8');
    saved += 1;
}
console.log(`Saved ${saved} posts to ${outDir}/`);
