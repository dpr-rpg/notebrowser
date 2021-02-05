"""Generate static site from GM notes."""
from pathlib import Path

import click

from notebrowser import building


@click.group()
@click.option(
    "-d",
    "--directory",
    default=Path("."),
    help="the root directory of your project",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
)
@click.pass_context
def cli(ctx, directory: str):
    """Command-line interface."""
    ctx.obj = Path(directory)


@cli.command(help="Initialize project directory.")
@click.pass_obj
def init(base_dir):
    """Initialize project directory."""
    click.echo(f"TODO: initializing site at {base_dir.absolute()}")


@cli.command(help="Make site pages.")
@click.pass_obj
def make(base_dir):
    """Make site."""
    site_data = building.make_site(base_dir)
    click.echo(f"making site at {site_data.site_dir.absolute()}")


@cli.command(help="Make site pages and start local http server.")
@click.pass_obj
def serve(base_dir):
    """Serve site."""
    site_data = building.make_site(base_dir)
    click.echo(f"making site at {site_data.site_dir.absolute()}")
    click.echo(f"TODO: serving site at {site_data.site_dir.absolute()}")
