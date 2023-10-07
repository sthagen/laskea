"""Report environment to support resolution of user issues."""
import sys
from typing import List, no_type_check

import scooby


@no_type_check
def report(shallow: bool = False) -> str:
    """Return either text options for the user to report her env or the report of the environment for support."""
    deep = True
    try:
        import pkg_resources  # noqa
    except (ImportError, ModuleNotFoundError):
        if shallow:
            deep = False
            sys.stdout.write('\nInfo: No setuptools module found and shallow reporting requested. Continuing ...')
        else:
            message = (
                '\n  Report requires setuptools (to identify the version of atlassian-python-api).'
                '\n  You may either add --shallow or install the module via `pip install setuptools`\n\n'
            )
            return message

    if deep:
        import atlassian  # type: ignore # noqa

        packages = pkg_resources.working_set  # noqa
        monkey_atl = [p.version for p in packages if p.project_name == 'atlassian-python-api'][0]  # noqa
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
            optional: List[str] = []

            scooby.Report.__init__(
                self, additional=additional, core=core, optional=optional, ncol=ncol, text_width=text_width, sort=sort
            )

    return str(Report()) + '\n'
