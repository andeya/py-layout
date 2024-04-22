# type: ignore[attr-defined]
"""
Top-level package for {{ cookiecutter.package_name }}.

{{ cookiecutter.project_description }}
"""

import sys

if sys.version_info >= (3, 8):
    from importlib import metadata as importlib_metadata
else:
    import importlib_metadata

__email__ = '{{ cookiecutter.email }}'


def get_version() -> str:
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"


version: str = get_version()
