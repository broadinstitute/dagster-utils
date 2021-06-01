# Dagster Utils

A collection of common utilities used by the Monster team to develop Dagster pipelines. Each subsection has its own readme explaining its contents.

## How to use this library

This library is hosted on [PyPI](https://pypi.org/) and will work with most Python package managers out of the box. You can reference this package as `broad_dagster_utils`, e.g. for Poetry:

```
# pyproject.toml
[tool.poetry.dependencies]
broad_dagster_utils = "^0.1.0"
```

Note that, despite this name, you'll need to import the package as `dagster_utils`, e.g.:
```python
from dagster_utils.typing import DagsterConfigDict
```

### Local Testing
For development against a local checkout in another project (i.e., a project with a dependency on `dagster_utils`), make the following adjustment to the project's `pyproject.toml`:
```
broad-dagster-utils = {path = "<relative path to your dagster_utils checkout>", develop = true}
```

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

To release a new version, determine what type of version increase your changes constitute (see the above guide) and update the version listed in `pyproject.toml` accordingly. Poetry has several [version bump commands](https://python-poetry.org/docs/cli/#version) to help with this. You can update the version in a dedicated PR or as part of another change. When a PR that updates the version number lands on master, an action will run to create a new tag for that version number, followed by cutting a Git release and publishing the new version to PyPI.
