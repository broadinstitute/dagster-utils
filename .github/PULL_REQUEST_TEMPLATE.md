## Why

[Relevant ticket](https://broadinstitute.atlassian.net/browse/<ticket_id>)

## This PR


## Library Checklist

<!-- Delete whichever checklist doesn't apply to your PR. -->

<!-- If this is a PR for making a code change: -->

[] I have added my changes to CHANGELOG.md under "Pending Release".

<!-- If this is a PR for updating the changelog for a new version to be released: -->

[] The title of my PR starts with the text `[RELEASE]`, in all caps, to make sure automations handle it correctly.
[] I have added a header to CHANGELOG.md for the new version number. This header is _below_ the "Pending Release" header.
[] My new header includes the date of release (update to the current date before merging the PR).
[] All changes that were under "Pending Release" have been moved under this new header.
[] The "Pending Release" header is still at the top, including the italicized explanation for what to put into it, and now contains no changes.
[] Immediately after merging this PR, I will [create a new tag](https://github.com/broadinstitute/dagster-utils/releases/new) for the version being released. The tag's name will be the number of the release (e.g. `1.3.0` and _not_ `v1.3.0`).
