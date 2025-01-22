"""Result types for agents."""

# %% IMPORTS

import pydantic as pdt

# %% RESULTS


class SlackThreadDigest(pdt.BaseModel):
    """Digest of a Slack thread."""

    title: str
    summary: str
    takeaways: list[str]
    tags: list[str]
    links: list[str]
    tools: list[str]


class SlackWorkspaceDigest(pdt.BaseModel):
    """Digest of a Slack workspace."""

    tops: list[str]
    flops: list[str]
    moods: list[str]
    topics: list[str]
    sharing: list[str]
