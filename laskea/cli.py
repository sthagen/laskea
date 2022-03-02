#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""Commandline API gateway for laskea."""
import glob
import json
import os
import pathlib
import sys
from typing import List, Union

import typer
from cogapp import Cog, CogUsageError  # type: ignore
from cogapp.cogapp import CogError, CogOptions  # type: ignore

import laskea
import laskea.api.jira as api
import laskea.laskea as fill

# from laskea import login, query, table

APP_NAME = 'Calculate (Finnish: laskea) some parts.'
APP_ALIAS = 'laskea'
APP_ENV = 'ASCIINATOR'
DEBUG = bool(os.getenv(f'{APP_ENV}_DEBUG', ''))
ENCODING = 'utf-8'
DEFAULT_MARKERS = '[[[fill ]]] [[[end]]]'
BASE_MARKERS = os.getenv(f'{APP_ENV}_MARKERS', DEFAULT_MARKERS)

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


@app.command('update')
def update(
    source: str = typer.Argument(default=''),
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
    verbose: bool = typer.Option(
        False,
        '-v',
        '--verbose',
        help='Verbose output (default is False)',
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
    * ASCIINATOR_COL_MAPS='{"key": ["key", "key"], "summary": ["summary", "fields.summary"], "custom field name": ["customfield_123", "fields.customfield_123"]}'
    * ASCIINATOR_MARKERS='[[[fill ]]] [[[end]]]'
    * ASCIINATOR_DEBUG='AnythingTruthy'
    
    """
    # cog -I. -P -c -r --markers='[[[fill ]]] [[[end]]]' -p "from api import *" files*.md
    command = 'update'
    incoming = inp if inp else source
    paths = glob.glob(incoming)
    if not paths:
        print('Usage: asciinator "source-files*md"')
        sys.exit(2)
    # config = conf if conf else pathlib.Path.home() / fill.DEFAULT_CONFIG_NAME
    # action = [command, str(incoming), str(config)]
    vector = [
        APP_ALIAS,
        '-P',
        '-c',
        '-r',
        f'--markers={BASE_MARKERS}',
        '-p',
        'from laskea import *',
    ] + paths

    cog = Cog()

    if DEBUG or verbose:
        print(f'Command: ({command})', file=sys.stderr)
        print(f'Environment(variable values):', file=sys.stderr)
        app_env_user = f'{APP_ENV}_USER'
        app_env_token = f'{APP_ENV}_TOKEN'
        app_env_base_url = f'{APP_ENV}_BASE_URL'
        app_env_col_fields = f'{APP_ENV}_COL_FIELDS'
        app_env_col_maps = f'{APP_ENV}_COL_MAPS'
        app_env_markers = f'{APP_ENV}_MARKERS'
        empty = ''
        print(f'- {APP_ENV}_USER: ({os.getenv(app_env_user, empty)})', file=sys.stderr)
        print(f'- {APP_ENV}_TOKEN: ({"*" * len(os.getenv(app_env_token, empty))})', file=sys.stderr)
        print(f'- {APP_ENV}_BASE_URL: ({os.getenv(app_env_base_url, empty)})', file=sys.stderr)
        print(f'- {APP_ENV}R_COL_FIELDS: ({os.getenv(app_env_col_fields, empty)})', file=sys.stderr)
        print(f'- {APP_ENV}_COL_MAPS: ({os.getenv(app_env_col_maps, empty)})', file=sys.stderr)
        print(f'- {APP_ENV}_MARKERS: ({os.getenv(app_env_markers, empty)})', file=sys.stderr)
        print(f'Effective(variable values):', file=sys.stderr)
        print(f'- RemoteUser: ({api.BASE_USER})', file=sys.stderr)
        print(f'- RemoteToken: ({"*" * len(api.BASE_PASS)})', file=sys.stderr)
        print(f'- RemoteBaseURL: ({api.BASE_URL})', file=sys.stderr)
        print(f'- ColumnFields(table): ({api.BASE_COL_FIELDS})', file=sys.stderr)
        print(f'- ColumnMaps(remote->table): ({api.BASE_COL_MAPS})', file=sys.stderr)
        print(f'- Markers(pattern): ({BASE_MARKERS})', file=sys.stderr)
        print(f'- CallVector: ({vector})', file=sys.stderr)

    try:
        cog.callableMain(vector)
    except CogUsageError as err:
        print(f'CodeGen processing usage error:', file=sys.stderr)
        print(str(err))
        return sys.exit(1)

    return sys.exit(0)


@app.command('verify')
def verify(
    source: str = typer.Argument(default=''),
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
    verbose: bool = typer.Option(
        False,
        '-v',
        '--verbose',
        help='Verbose output (default is False)',
    ),    
) -> int:
    """
    Answer the question if the input document is in good shape.
    
    You can set some options per evironment variables:
    
    \b
    * ASCIINATOR_USER='remote-user'
    * ASCIINATOR_TOKEN='remote-secret'
    * ASCIINATOR_BASE_URL='https://remote-jira-instance.example.com/'
    * ASCIINATOR_COL_FIELDS: '["Key", "Summary", "Custom Field Name"]'
    * ASCIINATOR_COL_MAPS='{"key": ["key", "key"], "summary": ["summary", "fields.summary"], "custom field name": ["customfield_123", "fields.customfield_123"]}'
    * ASCIINATOR_MARKERS='[[[fill ]]] [[[end]]]'
    * ASCIINATOR_DEBUG='AnythingTruthy'

    """
    # cog -I. -P -c --markers='[[[fill ]]] [[[end]]]' -p "from api import *" files*.md
    command = 'verify'
    configuration, conf_source = None, ''
    if conf:
        cp = pathlib.Path(conf)
        if not cp.is_file() or not cp.stat().st_size:
            print(f'Given configuration path is no file or empty')
            sys.exit(2)
        print(f'Reading configuration file {cp} as requested...')
        configuration = json.load(cp.open())
    else:
        cp = pathlib.Path(fill.DEFAULT_CONFIG_NAME)
        if not cp.is_file() or not cp.stat().st_size:
            print(f'Configuration path {cp} in current working directory is no file or empty')
            cp = pathlib.Path.home() / fill.DEFAULT_CONFIG_NAME
            if not cp.is_file() or not cp.stat().st_size:
                print(f'User home configuration path to {cp} is no file or empty - ignoring configuration data')
            else:
                print(f'Reading configuration file {cp} from home directory at {pathlib.Path.home()} ...')
                configuration = json.load(cp.open())
        else:
            print(f'Reading configuration file {cp} from current working directory at {pathlib.Path.cwd()}...')
            configuration = json.load(cp.open())

    if configuration is not None:
        if DEBUG or verbose:
            print(f'Loaded configuration from {cp}:')
            print('# --- BEGIN ---')
            print(json.dumps(configuration, indent=2))
            print('# --- E N D ---')
        print('Configuration interface requested - NotImplemented')

    incoming = inp if inp else source
    if not incoming:
        callback(False)
    paths = glob.glob(incoming)
    if not paths:
        print('Usage: asciinator "source-files*md"')
        sys.exit(2)
    # config = conf if conf else pathlib.Path.home() / fill.DEFAULT_CONFIG_NAME
    # action = [command, str(incoming), str(config)]
    vector = [
        APP_ALIAS,
        '-P',
        '-c',
        f'--markers={BASE_MARKERS}',
        '-p',
        'from laskea import *',
    ] + paths

    cog = Cog()

    if DEBUG or verbose:
        print(f'Command: ({command})', file=sys.stderr)
        print(f'Environment(variable values):', file=sys.stderr)
        app_env_user = f'{APP_ENV}_USER'
        app_env_token = f'{APP_ENV}_TOKEN'
        app_env_base_url = f'{APP_ENV}_BASE_URL'
        app_env_col_fields = f'{APP_ENV}_COL_FIELDS'
        app_env_col_maps = f'{APP_ENV}_COL_MAPS'
        app_env_markers = f'{APP_ENV}_MARKERS'
        empty = ''
        print(f'- {APP_ENV}_USER: ({os.getenv(app_env_user, empty)})', file=sys.stderr)
        print(f'- {APP_ENV}_TOKEN: ({"*" * len(os.getenv(app_env_token, empty))})', file=sys.stderr)
        print(f'- {APP_ENV}_BASE_URL: ({os.getenv(app_env_base_url, empty)})', file=sys.stderr)
        print(f'- {APP_ENV}R_COL_FIELDS: ({os.getenv(app_env_col_fields, empty)})', file=sys.stderr)
        print(f'- {APP_ENV}_COL_MAPS: ({os.getenv(app_env_col_maps, empty)})', file=sys.stderr)
        print(f'- {APP_ENV}_MARKERS: ({os.getenv(app_env_markers, empty)})', file=sys.stderr)
        print(f'Effective(variable values):', file=sys.stderr)
        print(f'- RemoteUser: ({api.BASE_USER})', file=sys.stderr)
        print(f'- RemoteToken: ({"*" * len(api.BASE_PASS)})', file=sys.stderr)
        print(f'- RemoteBaseURL: ({api.BASE_URL})', file=sys.stderr)
        print(f'- ColumnFields(table): ({api.BASE_COL_FIELDS})', file=sys.stderr)
        print(f'- ColumnMaps(remote->table): ({api.BASE_COL_MAPS})', file=sys.stderr)
        print(f'- Markers(pattern): ({BASE_MARKERS})', file=sys.stderr)
        print(f'- CallVector: ({vector})', file=sys.stderr)

    try:
        cog.callableMain(vector)
    except CogUsageError as err:
        print(f'CodeGen processing usage error:', file=sys.stderr)
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
