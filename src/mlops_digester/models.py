"""Grant access to foundation models."""

# %% IMPORTS

from pydantic_ai.models.openai import OpenAIModel

from mlops_digester import settings

# %% MODELS


def to_openai_model(openai_model_settings: settings.OpenAIModelSettings) -> OpenAIModel:
    """Create an OpenAI model from settings."""
    return OpenAIModel(
        model_name=openai_model_settings.model_name,
        api_key=openai_model_settings.api_key.get_secret_value(),
    )
