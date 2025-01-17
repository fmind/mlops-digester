"""Command-Line Interface scripts."""

# %% IMPORTS

import pydantic_settings as pdts

from mlops_digester import settings, tasks

# %% FUNCTIONS


def main(argv: list[str] | None = None) -> int:
    """Run the main script of the application."""
    digest_settings = pdts.CliApp.run(settings.DigestSettings)
    tasks.digest(digest_settings=digest_settings)
    return 0
