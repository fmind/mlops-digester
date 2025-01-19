"""Clients for interacting with the external world."""

# %% IMPORTS

import slack_sdk as slack

from mlops_digester import settings

# %% CLIENTS


def to_slack_client(slack_client_settings: settings.SlackClientSettings) -> slack.WebClient:
    """Create a Slack client from settings."""
    return slack.WebClient(
        token=slack_client_settings.bot_token.get_secret_value(),
    )
