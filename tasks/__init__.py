"""Task collections of the project."""

# mypy: ignore-errors

# %% IMPORTS

from invoke import Collection

from . import (
    checks,
    cleans,
    commits,
    containers,
    docs,
    formats,
    installs,
    packages,
    runs,
)

# %% NAMESPACES

ns = Collection()

# %% COLLECTIONS

ns.add_collection(checks)
ns.add_collection(cleans)
ns.add_collection(commits)
ns.add_collection(containers)
ns.add_collection(docs)
ns.add_collection(formats)
ns.add_collection(installs)
ns.add_collection(packages)
ns.add_collection(runs, default=True)
