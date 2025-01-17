"""Provide tools to the foundation model."""

# %% IMPORTS

import datetime
import os

from slack_sdk import WebClient

# %% SLACKS

client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

# %% CONFIGS

today = datetime.datetime.now()
last_week = today - datetime.timedelta(weeks=1)
last_week_timestamp = last_week.timestamp()

# %%

conversations = client.conversations_list(limit=1000, exclude_archived=True)
channels = conversations["channels"]
channel = channels[0]

# %%

# should add bot to the channel
# https://stackoverflow.com/questions/60198159/slack-api-conversations-history-returns-error-not-in-channel

channel_id = "C015J2Y9RLM"

history = client.conversations_history(
    channel=channel_id,
    limit=1000,
    oldest=str(last_week_timestamp),
)
print(len(history["messages"]))
messages = history["messages"]
message = messages[0]
message["text"]

# %%

thread_id = "1737014464.851169"
thread = client.conversations_replies(channel=channel_id, ts=thread_id, limit=1000)
replies = thread["messages"]
reply = replies[0]
reply["text"]
