"""Run tasks of the project."""

# %% IMPORTS

from invoke.context import Context
from invoke.tasks import task

# %% TASKS


@task
def cli(ctx: Context) -> None:
    """Run the project command line interface."""
    ctx.run(f"uv run {ctx.project.repository}")


@task
def gui(ctx: Context) -> None:
    """Run the project graphical user interface."""
    ctx.run(f"uv run {ctx.project.repository}-gui", pty=True)


@task(pre=[cli], default=True)
def all(_: Context) -> None:
    """Run all run tasks."""
