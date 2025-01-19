"""Handle interactions with foundation models."""

# %% IMPORTS

import os
import typing as T

import pydantic_ai as pdtai

from mlops_digester import depends, results, settings

# %% TYPES

SlackThreadDigestAgent: T.TypeAlias = pdtai.Agent[
    depends.SlackThreadDepends, results.SlackThreadDigest
]
SlackWorkspaceDigestAgent: T.TypeAlias = pdtai.Agent[
    depends.SlackWorkspaceDepends, results.SlackWorkspaceDigest
]

# %% FIXES

# fixes jupyter notebook errors in VS Code:
# https://ai.pydantic.dev/troubleshooting/#runtimeerror-this-event-loop-is-already-running

if "VSCODE_PID" in os.environ:
    import nest_asyncio

    nest_asyncio.apply()

# %% AGENTS


def to_slack_thread_digest_agent(
    slack_thread_digest_agent_settings: settings.SlackThreadDigesterAgentSettings,
) -> SlackThreadDigestAgent:
    """Create an agent for digesting Slack threads from settings."""
    agent = pdtai.Agent(
        name=slack_thread_digest_agent_settings.name,
        model_settings=slack_thread_digest_agent_settings.model_settings,
        deps_type=depends.SlackThreadDepends,
        result_type=results.SlackThreadDigest,
    )

    @agent.system_prompt
    def agent_system_prompt(ctx: pdtai.RunContext[depends.SlackThreadDepends]) -> str:
        """Define the system prompt for the agent."""
        slack_channel_name = ctx.deps.channel_name
        system_prompt = f"""{slack_thread_digest_agent_settings.system_prompt}

        The Slack Channel Name is: {slack_channel_name}
        """
        return system_prompt

    return agent


def to_slack_workspace_digest_agent(
    slack_workspace_digest_agent_settings: settings.SlackWorkspaceDigesterAgentSettings,
) -> SlackWorkspaceDigestAgent:
    """Create an agent for digesting Slack workspace from settings."""
    agent = pdtai.Agent(
        name=slack_workspace_digest_agent_settings.name,
        model_settings=slack_workspace_digest_agent_settings.model_settings,
        deps_type=depends.SlackWorkspaceDepends,
        result_type=results.SlackWorkspaceDigest,
    )

    @agent.system_prompt
    def agent_system_prompt(ctx: pdtai.RunContext[depends.SlackWorkspaceDepends]) -> str:
        """Define the system prompt for the agent."""
        slack_workspace_name = ctx.deps.workspace_name
        system_prompt = f"""{slack_workspace_digest_agent_settings.system_prompt}

        The Slack Workspace Name is: {slack_workspace_name}
        """
        return system_prompt

    return agent
