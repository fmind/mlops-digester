"""Provide context objects to agents."""

# %% IMPORTS

import dataclasses as dc

# %% DEPENDS


@dc.dataclass
class SlackThreadDepends:
    """Dependency for a Slack thread."""

    channel_name: str


@dc.dataclass
class SlackWorkspaceDepends:
    """Dependency for a Slack workspace."""

    workspace_name: str
