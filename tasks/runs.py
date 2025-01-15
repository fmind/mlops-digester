"""Run tasks of the project."""

# %% IMPORTS

from invoke.context import Context
from invoke.tasks import task

# %% TASKS


@task
def run(ctx: Context) -> None:
    """Run the project for the given job file."""
    ctx.run(f"uv run {ctx.project.repository}")


@task(pre=[run], default=True)
def all(_: Context) -> None:
    """Run all run tasks."""
