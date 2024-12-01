"""Report environment to support resolution of user issues."""

import pathlib
from typing import no_type_check

import scooby


@no_type_check
def report(shallow: bool = False) -> str:
    """Return either text options for the user to report her env or the report of the environment for support."""
    import importlib.resources  # noqa
    import atlassian  # type: ignore # noqa

    version_path = pathlib.Path(importlib.resources.files('atlassian')) / 'VERSION'  # noqa
    monkey_atl = '... should register a version - workaround failed (VERSION)'
    if version_path.is_file():
        with open(version_path) as version_file:
            try:
                monkey_atl = version_file.read().strip()
            except Exception:  # noqa
                pass
    atlassian.__version__ = monkey_atl

    class Report(scooby.Report):
        def __init__(self, additional=None, ncol=3, text_width=80, sort=False):
            """Initiate a scooby.Report instance."""

            # Mandatory packages.
            core = [
                'laskea',
                'atlassian',  # has version in VERSION text file in package info only?
                'cogapp.cogapp',
                'jmespath',
                'pydantic',
                'requests_cache',
                'scooby',
                'typer',
            ]

            # Optional packages.
            optional: list[str] = []

            scooby.Report.__init__(
                self, additional=additional, core=core, optional=optional, ncol=ncol, text_width=text_width, sort=sort
            )

    return str(Report()) + '\n'
