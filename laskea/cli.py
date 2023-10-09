#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Commandline API gateway for laskea."""
import sys
from typing import List

import requests_cache
import typer

import laskea
import laskea.config as cfg
import laskea.laskea as fill
from laskea import env

app = typer.Typer(
    add_completion=False,
    context_settings={'help_option_names': ['-h', '--help']},
    no_args_is_help=True,
)

Version = typer.Option(
    False,
    '-V',
    '--version',
    help='Display the laskea version and exit',
    is_eager=True,
)

Input = typer.Option(
    '',
    '-i',
    '--input',
    help='Path to input file',
    metavar='<sourcepath>',
)

ConfigurationPath = typer.Option(
    '',
    '-c',
    '--config',
    help=f'Path to config file (default is $HOME/{laskea.DEFAULT_CONFIG_NAME})',
    metavar='<configpath>',
)

Dryness = typer.Option(
    False,
    '-n',
    '--dry-run',
    help='Dry run (default is False)',
)

Verbosity = typer.Option(
    False,
    '-v',
    '--verbose',
    help='Verbose output (default is False)',
)

Quietness = typer.Option(
    False,
    '-q',
    '--quiet',
    help='Minimal output (default is False)',
)

Strictness = typer.Option(
    False,
    '-s',
    '--strict',
    help='Ouput noisy warnings on console and in the processed document (default is False)',
)

CacheExpiry = typer.Option(
    180,
    '-x',
    '--cache-expiry-seconds',
    help='Request cache expiry in seconds',
)


@app.callback(invoke_without_command=True)
def callback(version: bool = Version) -> None:
    """Calculate (Finnish: laskea) some parts."""
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
def update(  # noqa
    source: List[str],
    inp: str = Input,
    conf: str = ConfigurationPath,
    verify: bool = Dryness,
    verbose: bool = Verbosity,
    quiet: bool = Quietness,
    strict: bool = Strictness,
    expires: int = CacheExpiry,
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


@app.command('csv')
def svl_cmd(  # noqa
    query: str = typer.Argument(''),
    jql_query: str = typer.Option(
        '',
        '-j',
        '--jql-query',
        help=(
            'The query in JQL format.'
            '\nFor example given a project YES and two issues 123 and 124:'
            "\n'project = YES and key in (YES-123, YES-124) order by created DESC'"
        ),
        metavar='<jql-query>',
    ),
    conf: str = ConfigurationPath,
    key_magic: bool = typer.Option(
        False,
        '-k',
        '--key-magic',
        help='Apply magic to key by replacing with markdown like link (default is False)',
    ),
    field_sep: str = typer.Option(
        laskea.PIPE,
        '-d',
        '--delimiter',
        help=(
            'Delimiter / field separator'
            '\nOn output, header and data cell values will have any occurences'
            '\nof the field separator replaced with the replacement string'
        ),
        metavar='<field-separator>',
    ),
    replacement: str = typer.Option(
        laskea.FS_SLUG,
        '-r',
        '--replacement',
        help=(
            'Replacement string for occurences of FS in text\n'
            '\nOn output, header and data cell values will have any occurences'
            '\nof the field separator replaced with the replacement string'
        ),
        metavar='<replacement-text>',
    ),
    verify: bool = Dryness,
    verbose: bool = typer.Option(
        False,
        '-v',
        '--verbose',
        help='Verbose output (default is False)',
    ),
    strict: bool = Strictness,
    expires: int = CacheExpiry,
) -> int:
    """
    Export query result as separated values list.

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
    transaction_mode = 'commit' if not verify else 'dry-run'
    jql = jql_query.strip()
    if not jql and query:
        jql = query
    if not jql:
        print('JQL query required.', file=sys.stderr)
        return sys.exit(2)
    quiet = True
    laskea.QUIET = True
    laskea.DEBUG = False
    laskea.VERBOSE = False
    if verbose:
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
    if conf:
        cfg.process(conf, options)

    return sys.exit(laskea.svl(jql, key_magic=key_magic, field_sep=field_sep, replacement=replacement))


@app.command('version')
def app_version() -> None:
    """
    Display the laskea version and exit.
    """
    callback(True)
