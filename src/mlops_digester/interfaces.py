"""Graphical user interface for the application."""

# %% IMPORTS

import asyncio
import json

import gradio as gr

from mlops_digester import settings, tasks

# %% DEFAULTS

DEFAULT_DIGEST_EXCLUDE = {"openai_model": {"api_key"}, "slack_client": {"bot_token"}}
DEFAULT_DIGEST_SETTINGS = settings.DigestSettings().model_dump_json(
    indent=2, exclude=DEFAULT_DIGEST_EXCLUDE
)
DEFAULT_DIGEST_DESCRIPTION = (
    f"""Note: {DEFAULT_DIGEST_EXCLUDE} are automatically set by environment variables."""
)

# %% FUNCTIONS


def digest_fn(digest_config: str) -> dict:
    """Execute the digest task with settings."""
    # required to set an event loop in this thread
    asyncio.set_event_loop(asyncio.new_event_loop())
    digest_obj = json.loads(s=digest_config)  # convert to object
    digest_settings = settings.DigestSettings.model_validate(obj=digest_obj)
    slack_digest = tasks.digest(digest_settings=digest_settings)
    if slack_digest_data := slack_digest.get("digest"):
        return slack_digest_data.model_dump()
    else:
        slack_digest_error = slack_digest.get("digest_error", "Unknown Error")
        raise gr.Error(message=f"Slack Digest Error: {slack_digest_error}")


# %% INTERFACES

digest_interface = gr.Interface(
    fn=digest_fn,
    title="MLOps Digester",
    inputs=gr.Code(
        language="json",
        label="Digest Config",
        value=DEFAULT_DIGEST_SETTINGS,
        max_lines=30,
    ),
    outputs=gr.JSON(label="Digest Output", open=True),
    clear_btn=None,
    flagging_mode="never",
    description=DEFAULT_DIGEST_DESCRIPTION,
)

# %% ENTRYPOINTS


def main(argv: list[str] | None = None) -> None:
    """Run the main interface of the application."""
    digest_interface.launch()


if __name__ == "__main__":
    main()
