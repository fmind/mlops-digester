"""Settings of the application."""

# %% IMPORTS

import os

import pydantic as pdt
import pydantic_ai.settings
import pydantic_settings as pdts

# %% SETTINGS

# %% - Services


class LoguruServiceSettings(pdts.BaseSettings):
    """Settings for the loguru service."""

    level: str = "DEBUG"
    colorize: bool = True
    serialize: bool = True


class LogfireServiceSettings(pdts.BaseSettings):
    """Settings for the logfire service."""

    console: bool = False
    environment: str = "dev"


# %% - Models


class OpenAIModelSettings(pdts.BaseSettings):
    """Settings for an OpenAI model."""

    # config
    model_config = pdts.SettingsConfigDict(env_prefix="OPENAI_")
    # required
    api_key: pdt.SecretStr = pdt.SecretStr(os.environ["OPENAI_API_KEY"])
    model_name: str = "gpt-4o-mini"


# %% - Clients


class SlackClientSettings(pdts.BaseSettings):
    """Settings for a Slack client."""

    # config
    model_config = pdts.SettingsConfigDict(env_prefix="SLACK_")
    # required
    bot_token: pdt.SecretStr = pdt.SecretStr(os.environ["SLACK_BOT_TOKEN"])


# %% - Agents


class SlackThreadDigesterAgentSettings(pdts.BaseSettings):
    """Settings for a Slack thread digester agent."""

    # optional
    name: str = "Slack Thread Digester Agent"
    system_prompt: str = """You are a helpful assistant that summarizes conversations about AI, ML and MLOps.
        You will be given the content of a Slack thread, and you should return the following information:
        - title: should be a one-sentence descriptive title given to the discussion
        - summary: should be a few paragraphs summary of the overall discussion.
        - takeaways: should be a list of the most important points discussed.
        - tags: should be a list of tags related to the discussion.
        - links: should be a list of any links shared in the thread.
        - tools: should be a list with tools mentioned in the thread.
        """
    model_settings: pydantic_ai.settings.ModelSettings = {
        "temperature": 0.0,
    }


class SlackWorkspaceDigesterAgentSettings(pdts.BaseSettings):
    """Settings for a Slack workspace digester agent."""

    # optional
    name: str = "Slack Workspace Digester Agent"
    system_prompt: str = """You are a helpful assistant that highlight conversation summaries about AI, ML and MLOps.
        You will be given summary structures from a Slack workspace, and you should return the following information:
        - tops: should be a list of the most discussed topics.
        - flops: should be a list of the least discussed topics.
        - moods: should be a list of the most common moods.
        - topics: should be a list all the topics mentioned.
        - sharing: should be a list of content worth sharing.
        """
    model_settings: pydantic_ai.settings.ModelSettings = {
        "temperature": 0.0,
    }


# %% - Steps


class FetchSlackContentStepSettings(pdts.BaseSettings):
    """Settings for a fetch Slack content step."""

    # optional
    since_last_days: int = 7
    max_replies_per_message: int = 1000
    max_messages_per_channel: int = 1000
    max_channels_per_workspace: int = 1000
    exclude_archived_channels: bool = True
    channels: list[str] | None = None


class DigestSlackContentStepSettings(pdts.BaseSettings):
    """Settings for a digest Slack content step."""

    workspace_name: str = "MLOps Community"


# %% - Tasks


class DigestSettings(pdts.BaseSettings):
    """Digest settings of the application."""

    # services
    loguru_service: LoguruServiceSettings = LoguruServiceSettings()
    logfire_service: LogfireServiceSettings = LogfireServiceSettings()
    # models
    openai_model: OpenAIModelSettings = OpenAIModelSettings()
    # clients
    slack_client: SlackClientSettings = SlackClientSettings()
    # agents
    slack_thread_digest_agent: SlackThreadDigesterAgentSettings = SlackThreadDigesterAgentSettings()
    slack_workspace_digest_agent: SlackWorkspaceDigesterAgentSettings = (
        SlackWorkspaceDigesterAgentSettings()
    )
    # steps
    fetch_slack_content_step: FetchSlackContentStepSettings = FetchSlackContentStepSettings()
    digest_slack_content_step: DigestSlackContentStepSettings = DigestSlackContentStepSettings()
