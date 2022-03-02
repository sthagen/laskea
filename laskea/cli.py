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
DEFAULT_MARKERS = '"[[[fill ]]] [[[end]]]"'
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
        "'from laskea import *'",
    ] + paths
    if DEBUG:
        print(f'ACTION: ({command})', file=sys.stderr)
        print(f'ASCIINATOR_USER: ({api.BASE_USER})', file=sys.stderr)
        print(f'ASCIINATOR_TOKEN: ({"*" * len(api.BASE_PASS)})', file=sys.stderr)
        print(f'ASCIINATOR_BASE_URL: ({api.BASE_URL})', file=sys.stderr)
        print(f'ASCIINATOR_COL_FIELDS: ({api.BASE_COL_FIELDS})', file=sys.stderr)
        print(f'ASCIINATOR_COL_MAPS: ({api.BASE_COL_MAPS})', file=sys.stderr)
        print(f'ASCIINATOR_MARKERS: ({BASE_MARKERS})', file=sys.stderr)
        print(f'Vector: ({vector})', file=sys.stderr)

    return sys.exit(Cog().main(vector))


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
        "'from laskea import *'",
    ] + paths

    cog = Cog()

    if DEBUG:
        print(f'ACTION: ({command})', file=sys.stderr)
        print(f'ASCIINATOR_USER: ({api.BASE_USER})', file=sys.stderr)
        print(f'ASCIINATOR_TOKEN: ({"*" * len(api.BASE_PASS)})', file=sys.stderr)
        print(f'ASCIINATOR_BASE_URL: ({api.BASE_URL})', file=sys.stderr)
        print(f'ASCIINATOR_COL_FIELDS: ({api.BASE_COL_FIELDS})', file=sys.stderr)
        print(f'ASCIINATOR_COL_MAPS: ({api.BASE_COL_MAPS})', file=sys.stderr)
        print(f'ASCIINATOR_MARKERS: ({BASE_MARKERS})', file=sys.stderr)
        print(f'Vector: ({vector})', file=sys.stderr)
    
        print(f'CodeGen option states of {cog.options}):', file=sys.stderr)
        print(f'- {cog.options.args=} (default=[])', file=sys.stderr)
        print(f'- {cog.options.includePath=} (default=[])', file=sys.stderr)
        print(f'- {cog.options.defines=} (default={{}})', file=sys.stderr)
        print(f'- {cog.options.bShowVersion=} (default=False)', file=sys.stderr)
        print(f'- {cog.options.sMakeWritableCmd=} (default=None)', file=sys.stderr)
        print(f'- {cog.options.bReplace=} (default=False)', file=sys.stderr)
        print(f'- {cog.options.bNoGenerate=} (default=False)', file=sys.stderr)
        print(f'- {cog.options.sOutputName=} (default=None)', file=sys.stderr)
        print(f'- {cog.options.bWarnEmpty=} (default=False)', file=sys.stderr)
        print(f'- {cog.options.bHashOutput=} (default=False)', file=sys.stderr)
        print(f'- {cog.options.bDeleteCode=} (default=False)', file=sys.stderr)
        print(f'- {cog.options.bEofCanBeEnd=} (default=False)', file=sys.stderr)
        print(f'- {cog.options.sSuffix=} (default=None)', file=sys.stderr)
        print(f'- {cog.options.bNewlines=} (default=False)', file=sys.stderr)
        print(f"- {cog.options.sBeginSpec=} (default='[[[cog')", file=sys.stderr)
        print(f"- {cog.options.sEndSpec=} (default=']]]')", file=sys.stderr)
        print(f"- {cog.options.sEndOutput=} (default='[[[end]]]')", file=sys.stderr)
        print(f'- {cog.options.sEncoding=} (default="utf-8")', file=sys.stderr)
        print(f'- {cog.options.verbosity=} (default=2)', file=sys.stderr)
        print(f"- {cog.options.sPrologue=} (default='')", file=sys.stderr)
        print(f'- {cog.options.bPrintOutput=} (default=False)', file=sys.stderr)
        print(f'- {cog.options.bCheck=} (default=False)', file=sys.stderr)

        print(' Calling cog.options.parseArgs(vector)', file=sys.stderr)

    try:
        cog.options.parseArgs(vector)
    except CogError as err:
        print(f'CodeGen option parsing error:', file=sys.stderr)
        print(str(err))
        return sys.exit(2)

    if DEBUG:
        print(' Calling cog.callableMain(vector)', file=sys.stderr)

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
