"""High-level tasks of the application."""

# %% IMPORTS

import datetime

import slack_sdk as slack
from loguru import logger

from mlops_digester import settings

# %% SUBTASKS

# %% TASKS


def digest(digest_settings: settings.DigestSettings) -> None:
    """Digest MLOps information from Slack channels."""
    # settings
    logger.debug(f"Digest Settings: {digest_settings}")
    # periods
    end_date = datetime.datetime.now()
    logger.info(f"End Date: {end_date}")
    start_date = end_date - datetime.timedelta(days=digest_settings.since_last_days)
    logger.info(f"Start Date: {start_date}")
    # slack
    logger.debug("Initializing Slack Web Client")
    slack_client = slack.WebClient(token=digest_settings.slack_bot_token.get_secret_value())
    logger.debug(f"Slack Web Client Initialized: {slack_client.base_url}")
    # - channels
    slack_channels = {}
    if digest_settings.slack_channels:
        logger.debug(f"Fetching Slack Channels: {digest_settings.slack_channels}")
        for channel_id in digest_settings.slack_channels:
            logger.debug(f"Fetching Slack Channel: {channel_id} ...")
            slack_channel_result = slack_client.conversations_info(channel=channel_id)
            slack_channel = slack_channel_result["channel"]  # extract channel data
            logger.debug(f"Slack Channel Fetched: {slack_channel_result['ok']}")
            logger.trace(f"Slack Channel: {slack_channel}")
            slack_channels[slack_channel["id"]] = slack_channel
    else:
        logger.debug("Fetching Slack Channels: ALL")
        slack_conversations = slack_client.conversations_list(
            limit=digest_settings.max_channels_per_workspace,
            exclude_archived=digest_settings.exclude_archived_channels,
        )
        logger.debug(f"Slack Channels Fetched: {slack_conversations['ok']}")
        for slack_channel in slack_conversations["channels"]:
            logger.trace(f"Slack Channel: {slack_channel}")
            slack_channels[slack_channel["id"]] = slack_channel
    logger.debug(f"Slack Channels Count: {len(slack_channels)}")
    # - messages
    for slack_channel_id, slack_channel in slack_channels.items():
        logger.debug(f"Fetching Slack Channel Messages: {slack_channel_id}")
        slack_channel_messages = slack_channel.setdefault("messages", {})
        slack_conversation_history = slack_client.conversations_history(
            channel=channel_id,
            oldest=str(start_date.timestamp()),
            limit=digest_settings.max_messages_per_channel,
        )
        logger.debug(f"Slack Channel Messages Fetched: {slack_conversation_history['ok']}")
        for slack_channel_message in slack_conversation_history["messages"]:
            logger.trace(f"Slack Channel Message: {slack_channel_message}")
            slack_channel_messages[slack_channel_message["ts"]] = slack_channel_message
        logger.debug(f"Slack Channel Messages Count: {len(slack_channel_messages)}")
    # - replies
    for slack_channel_id, slack_channel in slack_channels.items():
        logger.debug(f"Fetching Slack Channel Replies: {slack_channel_id}")
        for slack_message_ts, slack_message in slack_channel["messages"].items():
            logger.debug(f"Fetching Slack Message Replies: {slack_message_ts}")
            slack_message_replies = slack_message.setdefault("replies", {})
            slack_message_thread = slack_client.conversations_replies(
                channel=channel_id,
                ts=slack_message_ts,
                limit=digest_settings.max_replies_per_message,
            )
            logger.debug(f"Slack Message Replies Fetched: {slack_message_thread['ok']}")
            for slack_message_reply in slack_message_thread["messages"]:
                logger.trace(f"Slack Message Reply: {slack_message_reply}")
                slack_message_replies[slack_message_reply["ts"]] = slack_message_reply
            logger.debug(f"Slack Message Replies Count: {len(slack_message_replies)}")
