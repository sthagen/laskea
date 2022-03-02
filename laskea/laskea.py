# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned,line-too-long
"""Calculate (Finnish: laskea) some parts."""
import json
import os
import pathlib
import sys
from typing import Dict, List, Optional, Tuple, Union, no_type_check

from atlassian import Jira  # type: ignore # noqa

import laskea.api.jira as api

DEBUG_VAR = 'LASKEA_DEBUG'
DEBUG = os.getenv(DEBUG_VAR)

ENCODING = 'utf-8'
ENCODING_ERRORS_POLICY = 'ignore'

DEFAULT_CONFIG_NAME = '.laskea.json'

DB: Dict[str, Union[None, Jira]] = {'handle': None}


@no_type_check
def table(query_text: str = '') -> str:
    """Public document interface."""
    if not DB.get('handle', None):
        DB['handle'] = api.login()

    print(api.markdown_table(DB['handle'], query_text))


def init() -> None:
    """Minimize boilerplate in the target documents."""
    pass


def verify_request(argv: Optional[List[str]]) -> Tuple[int, str, List[str]]:
    """Fail with grace."""
    if not argv or len(argv) != 3:
        return 2, 'received wrong number of arguments', ['']

    command, inp, config = argv

    if command not in ('update', 'verify'):
        return 2, 'received unknown command', ['']

    if inp:
        if not pathlib.Path(str(inp)).is_file():
            return 1, 'source is no file', ['']

    if not config:
        return 2, 'configuration missing', ['']

    config_path = pathlib.Path(str(config))
    if not config_path.is_file():
        return 1, f'config ({config_path}) is no file', ['']
    if not ''.join(config_path.suffixes).lower().endswith('.json'):
        return 1, 'config has no .json extension', ['']

    return 0, '', argv


def main(argv: Union[List[str], None] = None) -> int:
    """Drive the lookup."""
    error, message, strings = verify_request(argv)
    if error:
        print(message, file=sys.stderr)
        return error

    command, inp, config = strings

    with open(config, 'rt', encoding=ENCODING) as handle:
        configuration = json.load(handle)

    print(f'using configuration ({configuration})')
    print(f'Would act on {command =}, {inp =}, and {config =}')
    print('NotImplemented (yet)')
    return 0
