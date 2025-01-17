"""Grant access to foundation models."""

# https://ai.pydantic.dev/models/

# %% IMPORTS

from pydantic_ai.models.openai import OpenAIModel

# %% MODELS

openai_model = OpenAIModel(model_name="gpt-4o-mini")

# %% DEFAULTS

default_model = openai_model
