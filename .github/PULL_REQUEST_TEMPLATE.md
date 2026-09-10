## What does this PR do?

<!-- Brief description of the change, and the jurisdiction(s) it affects. -->

## Scrape comparison data

<!--
The "Compare pre/post scrape" check diffs your scrape output against the
published bulk data, and reads both download links from this section.

pre-data: sign in at https://open.pluralpolicy.com/data/session-json/, find the
jurisdiction and session your change affects, and copy the download link for the
most recently updated archive.

post-data: run the scraper with your change and publish the output as a .zip.
Either drag the file into this description, or upload it somewhere reachable
(a release asset on your fork works well) and paste the link.

    docker compose run --rm scrape <jurisdiction> bills --scrape
    zip -r scrape.zip _data/<jurisdiction>

Replace the placeholder URLs below, keeping the "pre-data:" and "post-data:"
labels at the start of the line. Re-post them in a comment any time you re-run
the scraper; the newest links win and the report comment is updated in place.
-->

pre-data: https://REPLACE-ME/pre.zip
post-data: https://REPLACE-ME/post.zip

## Checklist

- [ ] Scraper runs cleanly end to end
- [ ] Both comparison links above are filled in (or explain below why not)
