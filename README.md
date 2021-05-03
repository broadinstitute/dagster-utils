# Dagster Utils

A collection of common utilities used by the Monster team to develop Dagster pipelines. Each subsection has its own readme explaining its contents.

## Versioning

This library is versioned semantically.

* **Major versions** (e.g. 1.4.6 -> 2.0.0) represent significant shifts in functionality and may alter the call signatures of core features of the library. You may need to follow a migration plan to upgrade to a new major version.
* **Minor versions** (e.g. 1.4.6 -> 1.5.0) represent the removal or alteration of specific library features. They will not change core functionality, but the changelog should be reviewed before upgrading to avoid unexpected feature removals.
* **Patch versions** (e.g. 1.4.6 -> 1.4.7) represent internal improvements or new features that do not alter existing functionality or call signatures. They may introduce deprecations, but they will never remove deprecated functions. You can always safely upgrade to a new patch version.
* **Prerelease versions** (e.g. 1.4.6 -> 1.4.7-alpha.1) represent changes that have not yet been made part of an official release. See the section below for more info.

### Releasing a new version

Whenever a new change is merged to master, our CI will automatically cut a new prerelease version and publish it to Artifactory.

To release a new version, determine what type of version increase your changes constitute (see the above guide) and create a new tag for that version (do not include a `v` in the version number) in this repository. An action will automatically trigger to publish this new version to Artifactory and update our library version to match.

## How to use this library

This library is hosted on the [Broad Artifactory](https://broadinstitute.jfrog.io/). To configure Poetry to check that repository for packages, follow the instructions on private repositories [in their docs](https://python-poetry.org/docs/repositories/#install-dependencies-from-a-private-repository).

Credentials to authenticate to the Broad Artifactory instance are located in Vault under `secret/dsp/accts/artifactory/dsdejenkins`. Note that there's no way to configure Poetry with credentials in its config file other than to hardcode them in plain text. Instead of committing a plaintext password to your repository, you'll need to either:

* include a specific command in your actions to tell Poetry to use a given credential set: ```bash
# e.g. if you named your source "broad-artifactory" under the [[tool.poetry.source]] header
poetry config http-basic.broad-artifactory [interpolated username] [interpolated password]
```
* specify the credentials using [environment variables](https://python-poetry.org/docs/configuration/#using-environment-variables): ```bash
# e.g. for "broad-artifactory"
export POETRY_HTTP_BASIC_BROAD_ARTIFACTORY_USERNAME=secret_user
export POETRY_HTTP_BASIC_BROAD_ARTIFACTORY_PASSWORD=secret_pass
```
