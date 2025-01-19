"""Scripts of the application."""

# %% IMPORTS

import pydantic_settings as pdts

from mlops_digester import settings, tasks

# %% FUNCTIONS


def main(argv: list[str] | None = None) -> int:
    """Run the main script of the application."""
    digest_settings = pdts.CliApp.run(model_cls=settings.DigestSettings, cli_args=argv)
    slack_digest = tasks.digest(digest_settings=digest_settings)
    if slack_digest_data := slack_digest.get("digest"):
        print(slack_digest_data.model_dump_json(indent=2))
        return 0  # success
    else:
        slack_digest_error = slack_digest.get("digest_error", "Unknown Error")
        print(f"Slack Digest Error: {slack_digest_error}")
        return 1  # failure
