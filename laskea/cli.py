#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""Commandline API gateway for laskea."""
import glob
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
DEFAULT_MARKERS = '[[[fill ]]] [[[end]]]'
BASE_MARKERS = os.getenv(f'{APP_ENV}_MARKERS', DEFAULT_MARKERS)

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
) -> int:
    """
    Fill in some parts of the input document.
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

    if DEBUG:
        print(f'Environment(variables):', file=sys.stderr)
        app_env_user = f'{APP_ENV}_USER'
        app_env_token = f'{APP_ENV}_TOKEN'
        app_env_base_url = f'{APP_ENV}_BASE_URL'
        app_env_col_fields = f'{APP_ENV}_COL_FIELDS'
        app_env_col_maps = f'{APP_ENV}_COL_MAPS'
        app_env_markers = f'{APP_ENV}_MARKERS'
        empty = ''
        print(f'- {APP_ENV}_USER: ({os.getenv(app_env_user, empty)})', file=sys.stderr)
        print(f'- {APP_ENV}_TOKEN: ({"*" * len(os.getenv(app_env_token, empty)})', file=sys.stderr)
        print(f'- {APP_ENV}_BASE_URL: ({os.getenv(app_env_base_url, empty)})', file=sys.stderr)
        print(f'- {APP_ENV}R_COL_FIELDS: ({os.getenv(app_env_col_fields, empty)})', file=sys.stderr)
        print(f'- {APP_ENV}_COL_MAPS: ({os.getenv(app_env_col_maps, empty)})', file=sys.stderr)
        print(f'- {APP_ENV}_MARKERS: ({os.getenv(app_env_markers, empty)})', file=sys.stderr)
        print(f'Command: ({command})', file=sys.stderr)
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
) -> int:
    """
    Answer the question if the input document is in good shape.
    """
    # cog -I. -P -c --markers='[[[fill ]]] [[[end]]]' -p "from api import *" files*.md
    command = 'verify'
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

    if DEBUG:
        print(f'Environment(variables):', file=sys.stderr)
        app_env_user = f'{APP_ENV}_USER'
        app_env_token = f'{APP_ENV}_TOKEN'
        app_env_base_url = f'{APP_ENV}_BASE_URL'
        app_env_col_fields = f'{APP_ENV}_COL_FIELDS'
        app_env_col_maps = f'{APP_ENV}_COL_MAPS'
        app_env_markers = f'{APP_ENV}_MARKERS'
        empty = ''
        print(f'- {APP_ENV}_USER: ({os.getenv(app_env_user, empty)})', file=sys.stderr)
        print(f'- {APP_ENV}_TOKEN: ({"*" * len(os.getenv(app_env_token, empty)})', file=sys.stderr)
        print(f'- {APP_ENV}_BASE_URL: ({os.getenv(app_env_base_url, empty)})', file=sys.stderr)
        print(f'- {APP_ENV}R_COL_FIELDS: ({os.getenv(app_env_col_fields, empty)})', file=sys.stderr)
        print(f'- {APP_ENV}_COL_MAPS: ({os.getenv(app_env_col_maps, empty)})', file=sys.stderr)
        print(f'- {APP_ENV}_MARKERS: ({os.getenv(app_env_markers, empty)})', file=sys.stderr)
        print(f'Command: ({command})', file=sys.stderr)
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
