"""High-level tasks of the application."""

# %% IMPORTS

import datetime
import typing as T

import slack_sdk as slack
import slack_sdk.errors as slack_errors
from loguru import logger

from mlops_digester import agents, clients, depends, models, services, settings

# %% TYPES

SlackContent: T.TypeAlias = dict[str, T.Any]
SlackDigest: T.TypeAlias = dict[str, T.Any]

# %% SUBTASKS


def fetch_slack_content(
    fetch_slack_content_step_settings: settings.FetchSlackContentStepSettings,
    slack_client: slack.WebClient,
) -> SlackContent:
    """Fetch MLOps content from Slack channels, messages, and replies."""
    # dates
    end_date = datetime.datetime.now()
    logger.debug(f"Fetch Slack Content - End Date: {end_date}")
    start_date = end_date - datetime.timedelta(
        days=fetch_slack_content_step_settings.since_last_days
    )
    logger.debug(f"Fetch Slack Content - Start Date: {start_date}")
    # channels
    slack_channels = {}
    if fetch_slack_content_step_settings.channels:
        logger.debug(f"Fetching Slack Channels: {fetch_slack_content_step_settings.channels}")
        for slack_channel_id in fetch_slack_content_step_settings.channels:
            logger.debug(f"Fetching Slack Channel: {slack_channel_id}")
            slack_channel_result = slack_client.conversations_info(channel=slack_channel_id)
            slack_channel = slack_channel_result["channel"]  # extract channel data
            logger.debug(f"Fetched Slack Channel: {slack_channel_result['ok']}")
            logger.trace(f"Slack Channel: {slack_channel}")
            slack_channels[slack_channel["id"]] = slack_channel
    else:
        logger.debug("Fetching Slack Channels: ALL")
        slack_conversations = slack_client.conversations_list(
            limit=fetch_slack_content_step_settings.max_channels_per_workspace,
            exclude_archived=fetch_slack_content_step_settings.exclude_archived_channels,
        )
        logger.debug(f"Fetched Slack Channels: {slack_conversations['ok']}")
        for slack_channel in slack_conversations["channels"]:
            logger.trace(f"Slack Channel: {slack_channel}")
            slack_channels[slack_channel["id"]] = slack_channel
    logger.debug(f"Fetched Slack Channels Count: {len(slack_channels)}")
    # messages
    for slack_channel_id, slack_channel in slack_channels.items():
        logger.debug(f"Fetching Slack Channel Messages: {slack_channel_id}")
        slack_channel_messages = slack_channel.setdefault("messages", {})
        try:
            slack_conversation_history = slack_client.conversations_history(
                channel=slack_channel_id,
                oldest=str(start_date.timestamp()),
                limit=fetch_slack_content_step_settings.max_messages_per_channel,
            )
            logger.debug(f"Fetched Slack Channel Messages: {slack_conversation_history['ok']}")
            for slack_channel_message in slack_conversation_history["messages"]:
                logger.trace(f"Slack Channel Message: {slack_channel_message}")
                slack_channel_messages[slack_channel_message["ts"]] = slack_channel_message
            logger.debug(f"Fetched Slack Channel Messages Count: {len(slack_channel_messages)}")
        except slack_errors.SlackApiError as slack_api_error:
            logger.warning(f"Error while Fetching Slack Channel Messages: {slack_api_error}")
    # replies
    for slack_channel_id, slack_channel in slack_channels.items():
        logger.debug(f"Fetching Slack Channel Replies: {slack_channel_id}")
        for slack_message_ts, slack_message in slack_channel["messages"].items():
            logger.debug(f"Fetching Slack Message Replies: {slack_message_ts}")
            slack_message_replies = slack_message.setdefault("replies", {})
            slack_message_thread = slack_client.conversations_replies(
                ts=slack_message_ts,
                channel=slack_channel_id,
                limit=fetch_slack_content_step_settings.max_replies_per_message,
            )
            logger.debug(f"Fetched Slack Message Replies: {slack_message_thread['ok']}")
            for slack_message_reply in slack_message_thread["messages"]:
                logger.trace(f"Slack Message Reply: {slack_message_reply}")
                slack_message_replies[slack_message_reply["ts"]] = slack_message_reply
            logger.debug(f"Fetched Slack Message Replies Count: {len(slack_message_replies)}")
    return slack_channels


def digest_slack_content(
    digest_slack_content_step_settings: settings.DigestSlackContentStepSettings,
    slack_workspace_digest_agent: agents.SlackWorkspaceDigestAgent,
    slack_thread_digest_agent: agents.SlackThreadDigestAgent,
    slack_content: SlackContent,
) -> SlackDigest:
    """Digest MLOps content from Slack channels, messages, and replies."""
    slack_digests = []
    for slack_channel_id, slack_channel in slack_content.items():
        logger.debug(f"Digesting Slack Channel: {slack_channel_id}")
        slack_thread_depends = depends.SlackThreadDepends(channel_name=slack_channel["name"])
        for slack_message_id, slack_message in slack_channel["messages"].items():
            logger.debug(f"Digesting Slack Message: {slack_message_id}")
            slack_thread_prompt_parts = [
                f"[Message:{i}] {slack_reply['text']}"
                for i, slack_reply in enumerate(slack_message["replies"].values())
            ]
            logger.trace(f"Slack Thread Prompt: {slack_thread_prompt_parts}")
            slack_thread_prompt = "\n".join(slack_thread_prompt_parts)
            try:
                slack_thread_digest_result = slack_thread_digest_agent.run_sync(
                    user_prompt=slack_thread_prompt,
                    deps=slack_thread_depends,
                )
                slack_thread_digest_usage = slack_thread_digest_result.usage()
                slack_thread_digest_data = slack_thread_digest_result.data
                logger.trace(f"Slack Thread Usage: {slack_thread_digest_usage}")
                logger.trace(f"Slack Thread Digest: {slack_thread_digest_data}")
                logger.debug(f"Digested Slack Message: {slack_message_id}")
                slack_message["digest_usage"] = slack_thread_digest_usage
                slack_message["digest"] = slack_thread_digest_data
                slack_digests.append(slack_thread_digest_data)
            except Exception as slack_thread_digest_error:
                logger.error(
                    f"Error while Digesting Slack Message {slack_message_id}: {slack_thread_digest_error}"
                )
                slack_message["digest_error"] = slack_thread_digest_error
        logger.debug(f"Digested Slack Channel: {slack_channel_id}")
    logger.debug(f"Digested Slack Content Count: {len(slack_digests)}")
    slack_workspace_depends = depends.SlackWorkspaceDepends(
        workspace_name=digest_slack_content_step_settings.workspace_name
    )
    slack_prompt_parts = [slack_digest.model_dump_json() for slack_digest in slack_digests]
    slack_prompt = "\n".join(slack_prompt_parts)
    logger.trace(f"Slack Workspace Prompt: {slack_prompt}")
    try:
        slack_workspace_digest_result = slack_workspace_digest_agent.run_sync(
            user_prompt=slack_prompt,
            deps=slack_workspace_depends,
        )
        slack_workspace_digest_usage = slack_workspace_digest_result.usage()
        slack_workspace_digest_data = slack_workspace_digest_result.data
        logger.trace(f"Slack Workspace Usage: {slack_workspace_digest_usage}")
        logger.trace(f"Slack Workspace Digest: {slack_workspace_digest_data}")
        slack_content["digest_usage"] = slack_workspace_digest_usage
        slack_content["digest"] = slack_workspace_digest_data
    except Exception as slack_workspace_digest_error:
        logger.error(f"Error while Digesting Slack Content: {slack_workspace_digest_error}")
        slack_content["digest_error"] = slack_workspace_digest_error
    return slack_content


# %% TASKS


def digest(digest_settings: settings.DigestSettings) -> SlackDigest:
    """Digest MLOps content from various sources."""
    # settings
    logger.info(f"Digest Settings: {digest_settings}")
    # services
    logger.info("Initializing Loguru Service")
    services.configure_loguru(loguru_settings=digest_settings.loguru_service)
    logger.info("Initializing Logfire Service")
    services.configure_logfire(logfire_settings=digest_settings.logfire_service)
    # models
    logger.info("Initializing OpenAI Model")
    openai_model = models.to_openai_model(openai_model_settings=digest_settings.openai_model)
    logger.info(f"Initialized OpenAI Model: {openai_model}")
    # agents
    logger.info("Initializing Slack Thread Digest Agent")
    slack_thread_digest_agent = agents.to_slack_thread_digest_agent(
        slack_thread_digest_agent_settings=digest_settings.slack_thread_digest_agent,
    )
    slack_thread_digest_agent.model = openai_model  # assign agent model at runtime
    logger.info(f"Initialized Slack Thread Digest Agent: {slack_thread_digest_agent}")
    logger.info("Initializing Slack Workspace Digest Agent")
    slack_workspace_digest_agent = agents.to_slack_workspace_digest_agent(
        slack_workspace_digest_agent_settings=digest_settings.slack_workspace_digest_agent,
    )
    slack_workspace_digest_agent.model = openai_model  # assign agent model at runtime
    logger.info(f"Initialized Slack Workspace Digest Agent: {slack_workspace_digest_agent}")
    # clients
    logger.info("Initializing Slack Web Client")
    slack_client = clients.to_slack_client(slack_client_settings=digest_settings.slack_client)
    logger.info(f"Initialized Slack Web Client: {slack_client.base_url}")
    # contents
    logger.info("Fetching Slack Content")
    slack_content = fetch_slack_content(
        fetch_slack_content_step_settings=digest_settings.fetch_slack_content_step,
        slack_client=slack_client,
    )
    logger.info(f"Fetched Slack Content Count: {len(slack_content)}")
    # digests
    logger.info("Digesting Slack Content")
    slack_digest = digest_slack_content(
        digest_slack_content_step_settings=digest_settings.digest_slack_content_step,
        slack_workspace_digest_agent=slack_workspace_digest_agent,
        slack_thread_digest_agent=slack_thread_digest_agent,
        slack_content=slack_content,
    )
    logger.info(f"Digested Slack Content Count: {len(slack_digest)}")
    # return
    return slack_digest
