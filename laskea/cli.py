#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""Commandline API gateway for laskea."""
import sys
from typing import List

import requests_cache
import typer

import laskea
import laskea.config as cfg
import laskea.env as env
import laskea.laskea as fill

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
        typer.echo(f'{laskea.APP_NAME} version {laskea.__version__}')
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
    sys.stdout.write(cfg.generate_template())
    return sys.exit(0)


@app.command('report')
def report(
    shallow: bool = typer.Option(
        False,
        '-s',
        '--shallow',
        help='Shallow reporting - no setuptools required (default is False)',
    ),
) -> int:
    """Output either text options for the user to report her env or the report of the environment for support."""
    sys.stdout.write(env.report(shallow))
    return sys.exit(0)


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
        help=f'Path to config file (default is $HOME/{laskea.DEFAULT_CONFIG_NAME})',
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
    strict: bool = typer.Option(
        False,
        '-s',
        '--strict',
        help='Ouput noisy warnings on console and in the processed document (default is False)',
    ),
    expires: int = typer.Option(
        180,
        '-x',
        '--cache-expiry-seconds',
        help='Request cache expiry in seconds (default is 180)',
    ),
) -> int:
    """
    Fill in some parts of the input document.

    You can set some options per evironment variables:

    \b
    * LASKEA_USER='remote-user'
    * LASKEA_TOKEN='remote-secret'
    * LASKEA_BASE_URL='https://remote-jira-instance.example.com/'
    * LASKEA_CACHE_EXPIRY_SECONDS=180
    * LASKEA_COL_FIELDS: '["Key", "Summary", "Custom Field Name"]'
    * LASKEA_COL_MAPS='{"key": ["key", "key"], "summary": ["summary", "fields.summary"],
      "custom field name": ["customfield_123", "fields.customfield_123"]}'
    * LASKEA_JOIN_STRING=' <br>'
    * LASKEA_LF_ONLY='AnythingTruthy'
    * LASKEA_IS_CLOUD='WhenNotConnectingToJiraServerButJiraCloud'
    * LASKEA_MARKERS='[[[fill ]]] [[[end]]]'
    * LASKEA_DEBUG='AnythingTruthy'
    * LASKEA_VERBOSE='AnythingTruthy'
    * LASKEA_STRICT='AnythingTruthy'

    The quiet option (if given) disables any conflicting verbosity setting.
    """
    command = 'update'
    transaction_mode = 'commit' if not verify else 'dry-run'
    if quiet:
        laskea.QUIET = True
        laskea.DEBUG = False
        laskea.VERBOSE = False
    elif verbose:
        laskea.VERBOSE = True

    if strict:
        laskea.STRICT = True

    if transaction_mode == 'dry-run':
        laskea.DRY_RUN = True

    requests_cache.install_cache(cache_name='.laskea_cache', backend='sqlite', expire_after=expires)
    laskea.CACHE_EXPIRY_SECONDS = expires
    options = {
        'quiet': quiet,
        'strict': strict,
        'verbose': verbose,
    }
    cfg.process(conf, options)

    paths = (inp,) if inp else tuple(source)
    return sys.exit(fill.process(command, transaction_mode, paths, options))


@app.command('version')
def app_version() -> None:
    """
    Display the laskea version and exit.
    """
    callback(True)
