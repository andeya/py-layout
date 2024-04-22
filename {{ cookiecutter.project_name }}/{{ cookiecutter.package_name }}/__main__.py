# type: ignore[attr-defined]
from enum import Enum
from random import choice
from typing import Optional

import typer
from rich.console import Console

from {{ cookiecutter.package_name }}.config import app_config, wrap_log, logger
from {{ cookiecutter.package_name }} import version
from {{ cookiecutter.package_name }}.example import hello

logger.info(f"{app_config}")

hello = wrap_log(hello)


class Color(str, Enum):
    white = "white"
    red = "red"
    cyan = "cyan"
    magenta = "magenta"
    yellow = "yellow"
    green = "green"



console = Console()


def version_callback(print_version: bool) -> None:
    """Print the version of the package."""
    if print_version:
        console.print(
            f"[yellow]{{ cookiecutter.package_name }}[/] version: [bold blue]{version}[/]")
        raise typer.Exit()

main = typer.Typer(
    name="{{ cookiecutter.package_name }}",
    help="{{ cookiecutter.project_description }}",
    add_completion=False,
)

@main.command(name="")
def app(
    name: str = typer.Option(..., help="Person to greet."),
    color: Optional[Color] = typer.Option(
        None,
        "-c",
        "--color",
        "--colour",
        case_sensitive=False,
        help="Color for print. If not specified then choice will be random.",
    ),
    print_version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the {{ cookiecutter.package_name }} package.",
    ),
) -> None:
    """Print a greeting with a giving name."""
    if color is None:
        color = choice(list(Color))

    greeting: str = hello(name)
    console.print(f"[bold {color}]{greeting}[/]")


if __name__ == "__main__":
    main()
