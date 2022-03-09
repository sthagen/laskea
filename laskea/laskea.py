"""Calculate (Finnish: laskea) some parts."""
import sys
from typing import Mapping, Sequence

from atlassian import Jira  # type: ignore # noqa
from cogapp import Cog, CogUsageError  # type: ignore

import laskea
import laskea.config as cfg


def process(command: str, transaction_mode: str, paths: Sequence[str], options: Mapping[str, bool]) -> int:
    """Drive the lookup."""

    if command != 'update' or not paths:
        print('Usage: laskea update [--help] [-v] [-c config-path] [-n] [-i] source-files*md [other.md]')
        sys.exit(2)

    quiet = bool(options.get('quiet', ''))
    verbose = bool(options.get('verbose', ''))

    vector = [
        laskea.APP_ALIAS,
        '-P',
        '-c',
        f'--markers={laskea.BASE_MARKERS}',
        '-p',
        'from laskea import *',
    ]
    if transaction_mode == 'commit':
        vector.append('-r')
    if quiet:
        vector.append('--verbosity=0')

    cog = Cog()

    if laskea.DEBUG or verbose:
        cfg.report_context(command, transaction_mode, vector)

    for path in paths:
        single_vector = vector + [path]
        try:
            cog.callableMain(single_vector)
        except CogUsageError as err:
            print('CodeGen processing usage error:', file=sys.stderr)
            print(str(err))
            return 1
    return 0
