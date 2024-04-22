"""This module is called after project is created."""
import textwrap
from pathlib import Path
from shutil import move, rmtree
from typing import List

PROJECT_NAME = "{{ cookiecutter.project_name }}"
PACKAGE_NAME = "{{ cookiecutter.package_name }}"
PROJECT_MODE = "{{ cookiecutter.project_mode }}"

# Project root directory
PROJECT_DIRECTORY = Path.cwd().absolute()

# Values to generate correct license
LICENSE = "{{ cookiecutter.license }}"
ORGANIZATION = "{{ cookiecutter.organization }}"

# Values to generate github repository
GITHUB_USER = "{{ cookiecutter.github_name }}"

licences_dict = {
    "MIT": "mit",
    "BSD-3": "bsd3",
    "GNU GPL v3.0": "gpl3",
    "Apache Software License 2.0": "apache",
}


def generate_license(directory: Path, licence: str) -> None:
    """Generate license file for the project.

    Args:
        directory: path to the project directory
        licence: chosen licence
    """
    move(str(directory / "_licences" /
         f"{licence}.txt"), str(directory / "LICENSE"))
    rmtree(str(directory / "_licences"))


def remove_unused_files(
    directory: Path, package_name: str, need_to_remove_cli: bool
) -> None:
    """Remove unused files.

    Args:
        directory: path to the project directory
        package_name: current project package name
        need_to_remove_cli: flag for removing CLI related files
    """
    files_to_delete: List[Path] = []

    def _cli_specific_files() -> List[Path]:
        return [directory / package_name / "__main__.py"]

    if need_to_remove_cli:
        files_to_delete.extend(_cli_specific_files())

    for path in files_to_delete:
        path.unlink()


def print_further_instructions(project_name: str, github: str) -> None:
    """Show user what to do next after project creation.

    Args:
        project_name: current project name
        github: GitHub username
    """
    message = f"""
    Your project {project_name} is created.

    1) Now you can start working on it:

        $ cd {project_name} && git init

    2) If you don't have Poetry installed run:

        $ pip install poetry

    3) Initialize poetry and install pre-commit hooks:

        $ make install

    4) Run codestyle:

        $ make formatting

    5) Upload initial code to GitHub:

        $ git add .
        $ git commit -m ":tada: Initial commit"
        $ git branch -M main
        $ git remote add origin https://github.com/{github}/{project_name}.git
        $ git push -u origin main
    """
    print(textwrap.dedent(message))


def main() -> None:
    generate_license(directory=PROJECT_DIRECTORY,
                     licence=licences_dict[LICENSE])
    remove_unused_files(
        directory=PROJECT_DIRECTORY,
        package_name=PACKAGE_NAME,
        need_to_remove_cli=PROJECT_MODE != 'bin',
    )
    print_further_instructions(project_name=PROJECT_NAME, github=GITHUB_USER)


if __name__ == "__main__":
    main()
