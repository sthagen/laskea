# pylint: disable=line-too-long
"""Configuration API for laskea."""
import copy
import json
import os
import pathlib
import sys
from typing import Dict, List, Mapping, Tuple, no_type_check

import jmespath

import laskea
import laskea.api.jira as api

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
    "is_cloud": false,
    "user": "",
    "token": "",
    "base_url": "https://remote-jira-instance.example.com/"
  },
  "local": {
    "markers": "[[[fill ]]] [[[end]]]",
    "quiet": false,
    "verbose": false,
    "strict": false
  }
}
"""


def generate_template() -> str:
    """Return template of a well-formed JSON configuration."""
    return TEMPLATE_EXAMPLE


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
    column_fields = os.getenv(f'{laskea.APP_ENV}_COL_FIELDS', '')
    if column_fields:
        source_of['column_fields'] = 'env'
        api.BASE_COL_FIELDS = json.loads(column_fields)

    field_map = jmespath.search('table.column.field_map', configuration)
    if field_map:
        source_of['field_map'] = 'config'
        api.BASE_COL_MAPS = copy.deepcopy(field_map)
    field_map = os.getenv(f'{laskea.APP_ENV}_COL_MAPS', '')
    if field_map:
        source_of['field_map'] = 'env'
        api.BASE_COL_MAPS = json.loads(field_map)

    remote_user = jmespath.search('remote.user', configuration)
    if remote_user:
        source_of['remote_user'] = 'config'
        api.BASE_USER = remote_user
    remote_user = os.getenv(f'{laskea.APP_ENV}_USER', '')
    if remote_user:
        source_of['remote_user'] = 'env'
        api.BASE_USER = remote_user

    remote_token = jmespath.search('remote.token', configuration)
    if remote_token:
        source_of['remote_token'] = 'config'  # nosec
        api.BASE_TOKEN = remote_token
    remote_token = os.getenv(f'{laskea.APP_ENV}_TOKEN', '')
    if remote_token:
        source_of['remote_token'] = 'env'  # nosec
        api.BASE_TOKEN = remote_token

    remote_base_url = jmespath.search('remote.base_url', configuration)
    if remote_base_url:
        source_of['remote_base_url'] = 'config'
        api.BASE_URL = remote_base_url
    remote_base_url = os.getenv(f'{laskea.APP_ENV}_BASE_URL', '')
    if remote_base_url:
        source_of['remote_base_url'] = 'env'
        api.BASE_URL = remote_base_url

    local_markers = jmespath.search('local.markers', configuration)
    if local_markers:
        source_of['local_markers'] = 'config'
        laskea.BASE_MARKERS = local_markers
    local_markers = os.getenv(f'{laskea.APP_ENV}_MARKERS', '')
    if local_markers:
        source_of['local_markers'] = 'env'
        laskea.BASE_MARKERS = local_markers

    verbose = bool(jmespath.search('local.verbose', configuration))
    if verbose:
        source_of['verbose'] = 'config'
        laskea.DEBUG = verbose
    verbose = bool(os.getenv(f'{laskea.APP_ENV}_DEBUG', ''))
    if verbose:
        source_of['verbose'] = 'env'
        laskea.DEBUG = verbose

    is_cloud = bool(jmespath.search('remote.is_cloud', configuration))
    if is_cloud:
        source_of['is_cloud'] = 'config'
        laskea.IS_CLOUD = is_cloud
    is_cloud = bool(os.getenv(f'{laskea.APP_ENV}_IS_CLOUD', ''))
    if is_cloud:
        source_of['is_cloud'] = 'env'
        laskea.IS_CLOUD = is_cloud

    strict = bool(jmespath.search('local.strict', configuration))
    if strict:
        source_of['strict'] = 'config'
        laskea.STRICT = strict
    strict = bool(os.getenv(f'{laskea.APP_ENV}_STRICT', ''))
    if strict:
        source_of['strict'] = 'env'
        laskea.STRICT = strict

    quiet = bool(jmespath.search('local.quiet', configuration))
    if quiet:
        source_of['quiet'] = 'config'
        laskea.QUIET = quiet
        if source_of['verbose'] == 'config':
            laskea.DEBUG = quiet
    quiet = bool(os.getenv(f'{laskea.APP_ENV}_QUIET', ''))
    if quiet:
        source_of['quiet'] = 'env'
        laskea.QUIET = quiet
        source_of['verbose'] = 'env'
        laskea.DEBUG = quiet

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
        if not laskea.QUIET:
            print(f'Reading configuration file {cp} as requested...')
        with cp.open() as handle:
            configuration = json.load(handle)
    else:
        cn = laskea.DEFAULT_CONFIG_NAME
        cwd = pathlib.Path.cwd().resolve()
        for pp in cwd.parents:
            cp = pp / cn
            if cp.is_file() and cp.stat().st_size:
                if not laskea.QUIET:
                    print(f'Reading from discovered configuration path {cp}')
                with cp.open() as handle:
                    configuration = json.load(handle)
                return configuration, str(cp)

        cp = pathlib.Path.home() / laskea.DEFAULT_CONFIG_NAME
        if cp.is_file() and cp.stat().st_size:
            if not laskea.QUIET:
                print(f'Reading configuration file {cp} from home directory at {pathlib.Path.home()} ...')
            with cp.open() as handle:
                configuration = json.load(handle)
            return configuration, str(cp)

        if not laskea.QUIET:
            print(f'User home configuration path to {cp} is no file or empty - ignoring configuration data')

    return configuration, str(cp)


@no_type_check
def report_context(command: str, transaction_mode: str, vector: List[str]) -> None:
    """DRY."""
    if laskea.QUIET:
        return
    print(f'Command: ({command})', file=sys.stderr)
    print(f'- Transaction mode: ({transaction_mode})', file=sys.stderr)
    print('Environment(variable values):', file=sys.stderr)
    app_env_user = f'{laskea.APP_ENV}_USER'
    app_env_token = f'{laskea.APP_ENV}_TOKEN'
    app_env_base_url = f'{laskea.APP_ENV}_BASE_URL'
    app_env_col_fields = f'{laskea.APP_ENV}_COL_FIELDS'
    app_env_col_maps = f'{laskea.APP_ENV}_COL_MAPS'
    app_env_markers = f'{laskea.APP_ENV}_MARKERS'
    empty = ''
    print(f'- {laskea.APP_ENV}_USER: ({os.getenv(app_env_user, empty)})', file=sys.stderr)
    print(
        f'- {laskea.APP_ENV}_TOKEN: ({laskea.FAKE_SECRET if len(os.getenv(app_env_token, empty)) else empty})',
        file=sys.stderr,
    )
    print(f'- {laskea.APP_ENV}_BASE_URL: ({os.getenv(app_env_base_url, empty)})', file=sys.stderr)
    print(f'- {laskea.APP_ENV}_COL_FIELDS: ({os.getenv(app_env_col_fields, empty)})', file=sys.stderr)
    print(f'- {laskea.APP_ENV}_COL_MAPS: ({os.getenv(app_env_col_maps, empty)})', file=sys.stderr)
    print(f'- {laskea.APP_ENV}_MARKERS: ({os.getenv(app_env_markers, empty)})', file=sys.stderr)
    print('Effective(variable values):', file=sys.stderr)
    print(f'- RemoteUser: ({api.BASE_USER})', file=sys.stderr)
    print(f'- RemoteToken: ({"*" * len(api.BASE_PASS)})', file=sys.stderr)
    print(f'- RemoteBaseURL: ({api.BASE_URL})', file=sys.stderr)
    print(f'- ColumnFields(table): ({api.BASE_COL_FIELDS})', file=sys.stderr)
    print(f'- ColumnMaps(remote->table): ({api.BASE_COL_MAPS})', file=sys.stderr)
    print(f'- Markers(pattern): ({laskea.BASE_MARKERS})', file=sys.stderr)
    print(f'- CallVector: ({vector})', file=sys.stderr)


@no_type_check
def report_sources_of_effective_configuration(source_of: Dict[str, str], header: str) -> None:
    """DRY."""
    if laskea.QUIET:
        return
    print(header)
    print('# --- BEGIN ---')
    print(json.dumps(source_of, indent=2))
    print('# --- E N D ---')


@no_type_check
def safe_report_configuration(configuration: Dict[str, object], header: str) -> None:
    """DRY."""
    if laskea.QUIET:
        return
    print(header)
    print('# --- BEGIN ---')
    fake_configuration = copy.deepcopy(configuration)
    if jmespath.search('remote.token', fake_configuration):
        fake_configuration['remote']['token'] = laskea.FAKE_SECRET  # noqa
    print(json.dumps(fake_configuration, indent=2))
    print('# --- E N D ---')


@no_type_check
def create_and_report_effective_configuration(header: str) -> None:
    """DRY."""
    if laskea.QUIET:
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
            'markers': laskea.BASE_MARKERS,
            'verbose': laskea.DEBUG,
        },
    }
    safe_report_configuration(effective, header)


def process(conf: str, options: Mapping[str, bool]) -> None:
    """SPOC."""
    configuration, cp = discover_configuration(conf)

    verbose = bool(options.get('verbose', ''))
    if configuration is not None:
        if laskea.DEBUG or verbose:
            safe_report_configuration(configuration, f'Loaded configuration from {cp}:')

        source_of = load_configuration(configuration)

        if laskea.DEBUG or verbose:
            report_sources_of_effective_configuration(source_of, f'Configuration source after loading from {cp}:')

        if not laskea.QUIET:
            print('Configuration interface combined file, environment, and commandline values!')

        create_and_report_effective_configuration(f'Effective configuration combining {cp} and environment variables:')
