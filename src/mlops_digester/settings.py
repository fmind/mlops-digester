"""Settings of the application."""

# %% IMPORTS

import pydantic as pdt
import pydantic_settings as pdts

# %% SETTINGS


class DigestSettings(pdts.BaseSettings):
    """Digest settings of the application."""

    # required
    openai_api_key: pdt.SecretStr
    slack_bot_token: pdt.SecretStr
    # optional
    since_last_days: int = 7
    max_replies_per_message: int = 10  # 1000
    max_messages_per_channel: int = 10  # 1000
    max_channels_per_workspace: int = 10  # 1000
    exclude_archived_channels: bool = True
    slack_channels: list[str] | None = ["C015J2Y9RLM"]  # None
