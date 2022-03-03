#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""Commandline API gateway for laskea."""
import copy
import json
import os
import pathlib
import sys
from typing import Dict, List, Tuple, Union, no_type_check

import jmespath
import typer
from cogapp import Cog, CogUsageError  # type: ignore

import laskea
import laskea.api.jira as api
import laskea.laskea as fill

# from laskea import login, query, table

APP_NAME = 'Calculate (Finnish: laskea) some parts.'
APP_ALIAS = 'laskea'
APP_ENV = 'ASCIINATOR'
DEBUG = bool(os.getenv(f'{APP_ENV}_DEBUG', ''))
QUIET = False
ENCODING = 'utf-8'
DEFAULT_MARKERS = '[[[fill ]]] [[[end]]]'
BASE_MARKERS = os.getenv(f'{APP_ENV}_MARKERS', DEFAULT_MARKERS)
FAKE_SECRET = '*' * 13
TEMPLATE_EXAMPLE = """\
{
  "table": {
    "column": {
      "fields": [
        "Key",
        "Summary",
        "Custom Field Name",
        "Custom Field Other"
      ],
      "field_map": {
        "key": [
          "key",
          "key"
        ],
        "summary": [
          "summary",
          "fields.summary"
        ],
        "custom field name": [
          "customfield_11501",
          "fields.customfield_11501"
        ],
        "custom field other": [
          "customfield_13901",
          "fields.customfield_13901[].value"
        ]
      }
    }
  },
  "remote": {
    "user": "",
    "token": "",
    "base_url": "https://remote-jira-instance.example.com/"
  },
  "local": {
    "markers": "[[[fill ]]] [[[end]]]",
    "verbose": false
  }
}
"""

app = typer.Typer(
    add_completion=False,
    context_settings={'help_option_names': ['-h', '--help']},
    no_args_is_help=True,
)


@app.callback(invoke_without_command=True)
def callback(
    version: bool = typer.Option(
        False,
        '-V',
        '--version',
        help='Display the laskea version and exit',
        is_eager=True,
    )
) -> None:
    """
    Calculate (Finnish: laskea) some parts.
    """
    if version:
        typer.echo(f'{APP_NAME} version {laskea.__version__}')
        raise typer.Exit()


@app.command('template')
def app_template() -> int:
    """
    Write a template of a well-formed JSON configuration to standard out and exit

    The strategy for looking up configurations is to start at the current working
    directory trying to read a file with the name `.laskea.json` else try to read
    same named file in the user folder (home).

    In case an explicit path is given to the config option of commands that offer
    it, only that path is considered.
    """
    sys.stdout.write(TEMPLATE_EXAMPLE)
    return sys.exit(0)


@no_type_check
def load_configuration(configuration: Dict[str, object]) -> Dict[str, str]:
    """LaterAlligator."""
    if not configuration:
        print('Warning: Requested load from empty configuration')
        return {}

    source_of = {}

    column_fields = jmespath.search('table.column.fields[]', configuration)
    if column_fields:
        source_of['column_fields'] = 'config'
        api.BASE_COL_FIELDS = copy.deepcopy(column_fields)
    column_fields = os.getenv(f'{APP_ENV}_COL_FIELDS', '')
    if column_fields:
        source_of['column_fields'] = 'env'
        api.BASE_COL_FIELDS = json.loads(column_fields)

    field_map = jmespath.search('table.column.field_map', configuration)
    if field_map:
        source_of['field_map'] = 'config'
        api.BASE_COL_MAPS = copy.deepcopy(field_map)
    field_map = os.getenv(f'{APP_ENV}_COL_MAPS', '')
    if field_map:
        source_of['field_map'] = 'env'
        api.BASE_COL_MAPS = json.loads(field_map)

    remote_user = jmespath.search('remote.user', configuration)
    if remote_user:
        source_of['remote_user'] = 'config'
        api.BASE_USER = remote_user
    remote_user = os.getenv(f'{APP_ENV}_USER', '')
    if remote_user:
        source_of['remote_user'] = 'env'
        api.BASE_USER = remote_user

    remote_token = jmespath.search('remote.token', configuration)
    if remote_token:
        source_of['remote_token'] = 'config'
        api.BASE_TOKEN = remote_token
    remote_token = os.getenv(f'{APP_ENV}_TOKEN', '')
    if remote_token:
        source_of['remote_token'] = 'env'
        api.BASE_TOKEN = remote_token

    remote_base_url = jmespath.search('remote.base_url', configuration)
    if remote_base_url:
        source_of['remote_base_url'] = 'config'
        api.BASE_URL = remote_base_url
    remote_base_url = os.getenv(f'{APP_ENV}_BASE_URL', '')
    if remote_base_url:
        source_of['remote_base_url'] = 'env'
        api.BASE_URL = remote_base_url

    global BASE_MARKERS
    local_markers = jmespath.search('local.markers', configuration)
    if local_markers:
        source_of['local_markers'] = 'config'
        BASE_MARKERS = local_markers
    local_markers = os.getenv(f'{APP_ENV}_MARKERS', '')
    if local_markers:
        source_of['local_markers'] = 'env'
        BASE_MARKERS = local_markers

    global DEBUG
    verbose = bool(jmespath.search('local.verbose', configuration))
    if verbose:
        source_of['verbose'] = 'config'
        DEBUG = verbose
    verbose = bool(os.getenv(f'{APP_ENV}_DEBUG', ''))
    if verbose:
        source_of['verbose'] = 'env'
        DEBUG = verbose

    return source_of


@no_type_check
def discover_configuration(conf: str) -> Tuple[Dict[str, object], str]:
    """Try to retrieve the configuration following the "(explicit, local, parents, home)
    first wun wins" strategy."""
    configuration = None
    if conf:
        cp = pathlib.Path(conf)
        if not cp.is_file() or not cp.stat().st_size:
            print('Given configuration path is no file or empty')
            sys.exit(2)
        if not QUIET:
            print(f'Reading configuration file {cp} as requested...')
        configuration = json.load(cp.open())
    else:
        cn = fill.DEFAULT_CONFIG_NAME
        cwd = pathlib.Path.cwd().resolve()
        for pp in cwd.parents:
            cp = pp / cn
            if cp.is_file() and cp.stat().st_size:
                if not QUIET:
                    print(f'Reading from discovered configuration path {cp}')
                configuration = json.load(cp.open())
                return configuration, str(cp)

        cp = pathlib.Path.home() / fill.DEFAULT_CONFIG_NAME
        if cp.is_file() and cp.stat().st_size:
            if not QUIET:
                print(f'Reading configuration file {cp} from home directory at {pathlib.Path.home()} ...')
            configuration = json.load(cp.open())
            return configuration, str(cp)

        if not QUIET:
            print(f'User home configuration path to {cp} is no file or empty - ignoring configuration data')

    return configuration, str(cp)


@no_type_check
def report_context(command: str, transaction_mode: str, vector: List[str]) -> None:
    """DRY."""
    if QUIET:
        return
    print(f'Command: ({command})', file=sys.stderr)
    print(f'- Transaction mode: ({transaction_mode})', file=sys.stderr)
    print('Environment(variable values):', file=sys.stderr)
    app_env_user = f'{APP_ENV}_USER'
    app_env_token = f'{APP_ENV}_TOKEN'
    app_env_base_url = f'{APP_ENV}_BASE_URL'
    app_env_col_fields = f'{APP_ENV}_COL_FIELDS'
    app_env_col_maps = f'{APP_ENV}_COL_MAPS'
    app_env_markers = f'{APP_ENV}_MARKERS'
    empty = ''
    print(f'- {APP_ENV}_USER: ({os.getenv(app_env_user, empty)})', file=sys.stderr)
    print(f'- {APP_ENV}_TOKEN: ({FAKE_SECRET if len(os.getenv(app_env_token, empty)) else empty})', file=sys.stderr)
    print(f'- {APP_ENV}_BASE_URL: ({os.getenv(app_env_base_url, empty)})', file=sys.stderr)
    print(f'- {APP_ENV}_COL_FIELDS: ({os.getenv(app_env_col_fields, empty)})', file=sys.stderr)
    print(f'- {APP_ENV}_COL_MAPS: ({os.getenv(app_env_col_maps, empty)})', file=sys.stderr)
    print(f'- {APP_ENV}_MARKERS: ({os.getenv(app_env_markers, empty)})', file=sys.stderr)
    print('Effective(variable values):', file=sys.stderr)
    print(f'- RemoteUser: ({api.BASE_USER})', file=sys.stderr)
    print(f'- RemoteToken: ({"*" * len(api.BASE_PASS)})', file=sys.stderr)
    print(f'- RemoteBaseURL: ({api.BASE_URL})', file=sys.stderr)
    print(f'- ColumnFields(table): ({api.BASE_COL_FIELDS})', file=sys.stderr)
    print(f'- ColumnMaps(remote->table): ({api.BASE_COL_MAPS})', file=sys.stderr)
    print(f'- Markers(pattern): ({BASE_MARKERS})', file=sys.stderr)
    print(f'- CallVector: ({vector})', file=sys.stderr)


@no_type_check
def report_sources_of_effective_configuration(source_of: Dict[str, str], header: str) -> None:
    """DRY."""
    if QUIET:
        return
    print(header)
    print('# --- BEGIN ---')
    print(json.dumps(source_of, indent=2))
    print('# --- E N D ---')


@no_type_check
def safe_report_configuration(configuration: Dict[str, object], header: str) -> None:
    """DRY."""
    if QUIET:
        return
    print(header)
    print('# --- BEGIN ---')
    fake_configuration = copy.deepcopy(configuration)
    if jmespath.search('remote.token', fake_configuration):
        fake_configuration['remote']['token'] = FAKE_SECRET  # noqa
    print(json.dumps(fake_configuration, indent=2))
    print('# --- E N D ---')


@no_type_check
def create_and_report_effective_configuration(header: str) -> None:
    """DRY."""
    if QUIET:
        return
    effective = {
        'table': {
            'column': {
                'fields': copy.deepcopy(api.BASE_COL_FIELDS),
                'field_map': copy.deepcopy(api.BASE_COL_MAPS),
            },
        },
        'remote': {
            'user': api.BASE_USER,
            'token': '',
            'base_url': api.BASE_URL,
        },
        'local': {
            'markers': BASE_MARKERS,
            'verbose': DEBUG,
        },
    }
    safe_report_configuration(effective, header)


@app.command('update')
def update(
    source: List[str],
    inp: str = typer.Option(
        '',
        '-i',
        '--input',
        help='Path to input file',
        metavar='<sourcepath>',
    ),
    conf: str = typer.Option(
        '',
        '-c',
        '--config',
        help=f'Path to config file (default is $HOME/{fill.DEFAULT_CONFIG_NAME})',
        metavar='<configpath>',
    ),
    verify: bool = typer.Option(
        False,
        '-n',
        '--dry-run',
        help='Dry run (default is False)',
    ),
    verbose: bool = typer.Option(
        False,
        '-v',
        '--verbose',
        help='Verbose output (default is False)',
    ),
    quiet: bool = typer.Option(
        False,
        '-q',
        '--quiet',
        help='Minimal output (default is False)',
    ),
) -> int:
    """
    Fill in some parts of the input document.

    You can set some options per evironment variables:

    \b
    * ASCIINATOR_USER='remote-user'
    * ASCIINATOR_TOKEN='remote-secret'
    * ASCIINATOR_BASE_URL='https://remote-jira-instance.example.com/'
    * ASCIINATOR_COL_FIELDS: '["Key", "Summary", "Custom Field Name"]'
    * ASCIINATOR_COL_MAPS='{"key": ["key", "key"], "summary": ["summary", "fields.summary"],
      "custom field name": ["customfield_123", "fields.customfield_123"]}'
    * ASCIINATOR_MARKERS='[[[fill ]]] [[[end]]]'
    * ASCIINATOR_DEBUG='AnythingTruthy'

    The quiet option (if given) disables any conflicting verbosity setting.
    """
    command = 'update'
    transaction_mode = 'commit' if not verify else 'dry-run'
    global QUIET
    global DEBUG

    if quiet:
        QUIET = True
        DEBUG = False

    configuration, cp = discover_configuration(conf)

    if configuration is not None:
        if DEBUG or verbose:
            safe_report_configuration(configuration, f'Loaded configuration from {cp}:')

        source_of = load_configuration(configuration)

        if DEBUG or verbose:
            report_sources_of_effective_configuration(source_of, f'Configuration source after loading from {cp}:')

        if not QUIET:
            print('Configuration interface requested - Experimental!')

        create_and_report_effective_configuration(f'Effective configuration combining {cp} and environment variables:')

    paths = inp if inp else source
    if not paths:
        print('Usage: laskea update [--help] [-v] [-c config-path] [-n] [-i] source-files*md [other.md]')
        sys.exit(2)

    vector = [
        APP_ALIAS,
        '-P',
        '-c',
        f'--markers={BASE_MARKERS}',
        '-p',
        'from laskea import *',
    ]
    if not verify:
        vector.append('-r')
    if quiet:
        vector.append('--verbosity=0')

    cog = Cog()

    if DEBUG or verbose:
        report_context(command, transaction_mode, vector)

    for path in paths:
        single_vector = vector + [path]
        try:
            cog.callableMain(single_vector)
        except CogUsageError as err:
            print('CodeGen processing usage error:', file=sys.stderr)
            print(str(err))
            return sys.exit(1)

    return sys.exit(0)


@app.command('version')
def app_version() -> None:
    """
    Display the laskea version and exit.
    """
    callback(True)


# pylint: disable=expression-not-assigned
# @app.command()
def main(argv: Union[List[str], None] = None) -> int:
    """Delegate processing to functional module."""
    argv = sys.argv[1:] if argv is None else argv
    return fill.main(argv)
