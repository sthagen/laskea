#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""Commandline API gateway for laskea."""
import pathlib
import sys
from typing import List, Union

import typer

import laskea
import laskea.laskea as fill

APP_NAME = 'Calculate (Finnish: laskea) some parts.'
APP_ALIAS = 'laskea'
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
    command = 'update'
    incoming = inp if inp else source
    config = conf if conf else pathlib.Path.home() / fill.DEFAULT_CONFIG_NAME
    action = [command, str(incoming), str(config)]
    return sys.exit(fill.main(action))


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
    command = 'verify'
    incoming = inp if inp else source
    if not incoming:
        callback(False)
    config = conf if conf else pathlib.Path.home() / fill.DEFAULT_CONFIG_NAME
    action = [command, str(incoming), str(config)]
    return sys.exit(fill.main(action))


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
