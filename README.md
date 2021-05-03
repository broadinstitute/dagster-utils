# Dagster Utils

A collection of common utilities used by the Monster team to develop Dagster pipelines. Each subsection has its own readme explaining its contents.

## How to use this library

This library is hosted on the [Broad Artifactory](https://broadinstitute.jfrog.io/). To configure Poetry to check that repository for packages, follow the instructions on private repositories [in their docs](https://python-poetry.org/docs/repositories/#install-dependencies-from-a-private-repository). Once you've configured the Artifactory as a repository, you can reference this package as `dagster_utils`, e.g. for Poetry:

```
# pyproject.toml
[tool.poetry.dependencies]
dagster_utils = "^0.1.0"
```

No authentication is required to pull packages from Artifactory.

## Versioning

This library is versioned semantically.

* **Major versions** (e.g. 1.4.6 -> 2.0.0) represent significant shifts in functionality and may alter the call signatures of core features of the library. You may need to follow a migration plan to upgrade to a new major version.
* **Minor versions** (e.g. 1.4.6 -> 1.5.0) represent the removal or alteration of specific library features. They will not change core functionality, but the changelog should be reviewed before upgrading to avoid unexpected feature removals.
* **Patch versions** (e.g. 1.4.6 -> 1.4.7) represent internal improvements or new features that do not alter existing functionality or call signatures. They may introduce deprecations, but they will never remove deprecated functions. You can always safely upgrade to a new patch version.
* **Prerelease versions** (e.g. 1.4.6 -> 1.4.7-alpha.1) represent changes that have not yet been made part of an official release. See "Releasing a new version" below for more info.

### Describing changes

When describing changes made in a commit message, we want to be more thorough than usual, since bugs in dependencies are harder to diagnose. Break down the changes into these categories (omitting any categories that don't apply):

* **New features** are changes that add functionality, such as new optional arguments for existing functions or entire new classes/functions. These changes should never require that existing code be changed.
* **Bugfixes** are fairly self-explanatory - bugs that were identified and addressed. If fixing a bug required removing or altering existing features, make sure to list those under "breaking changes" as well.
* **Deprecations** are features that are still usable, but have been marked as deprecated (and thus trigger a warning when used). They are planned to be removed in a future version. Always try to deprecate functionality before it's removed.
* **Breaking changes** are changes that may break existing code using this library, such as renaming, removing, or reordering arguments to a function, deleting functionality (including deprecated functionality), or otherwise altering the library in ways that users will need to account for. Users should be able to use this section as a complete guide to upgrading their applications to be compatible with the new version.

### Releasing a new version

Whenever a new change is merged to master, our CI will automatically cut a new prerelease version and publish it to Artifactory.

To release a new version, determine what type of version increase your changes constitute (see the above guide) and [create a new tag](https://github.com/broadinstitute/dagster-utils/releases/new) for the new version (do not include a `v` in the version number). An action will automatically trigger to publish this new version to Artifactory and update our library version to match.
