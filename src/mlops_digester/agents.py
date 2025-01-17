"""Handle complex tasks using models."""

# %% IMPORTS

import os

from pydantic_ai import Agent

from mlops_digester import models

# %% FIXES

# fixes jupyter notebook errors:
# https://ai.pydantic.dev/troubleshooting/#runtimeerror-this-event-loop-is-already-running

if "VSCODE_PID" in os.environ:
    import nest_asyncio

    nest_asyncio.apply()

# %% AGENTS


agent = Agent(
    model=models.default_model,
    system_prompt="Be concise, reply with one sentence.",
)
