"""Calculate (Finnish: laskea) some parts."""
import os
import pathlib

# [[[fill git_describe()]]]
__version__ = '2023.10.9+parent.g2e1c540a'
# [[[end]]] (checksum: c3dce072a17daf46efd776c22acd3f56)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)

APP_ALIAS = str(pathlib.Path(__file__).parent.name)
APP_ENV: str = APP_ALIAS.upper()
APP_NAME = locals()['__doc__']
DEBUG = bool(os.getenv(f'{APP_ENV}_DEBUG', ''))
VERBOSE = bool(os.getenv(f'{APP_ENV}_VERBOSE', ''))
QUIET = False
STRICT = bool(os.getenv(f'{APP_ENV}_STRICT', ''))
ENCODING = 'utf-8'
ENCODING_ERRORS_POLICY = 'ignore'
DEFAULT_CONFIG_NAME = f'.{APP_ALIAS}.json'

CACHE_EXPIRY_SECONDS = int(os.getenv(f'{APP_ENV}_CACHE_EXPIRY_SECONDS', '180'))
REQUESTS_TIMEOUT_SECS = 30

FIELD_SEPARATORS = (
    CARET := '^',
    COLON := ':',
    COMMA := ',',
    DASH := '-',
    DOT := '.',
    PIPE := '|',
    PLUS := '+',
    RS := '\x1e',
    SEMI := ';',
    SPACE := ' ',
    TAB := '\t',
    USCORE := '_',
)
FS_SLUG = '$FIELD_SEPARATOR$'

DRY_RUN = False
OPEN_BRACKET = '['
CLOSE_BRACKET = ']'
DEFAULT_MARKERS = f'{OPEN_BRACKET * 3}fill {CLOSE_BRACKET * 3} {OPEN_BRACKET * 3}end{CLOSE_BRACKET * 3}'
DEFAULT_LF_ONLY = 'YES'
DEFAULT_JOIN_STRING = ' <br>'
BASE_MARKERS = os.getenv(f'{APP_ENV}_MARKERS', DEFAULT_MARKERS)
BASE_LF_ONLY = bool(os.getenv(f'{APP_ENV}_LF_ONLY', DEFAULT_LF_ONLY))
BASE_JOIN_STRING = os.getenv(f'{APP_ENV}_JOIN_STRING', DEFAULT_JOIN_STRING)
MASK_DISPLAY = '*' * 13
EXCEL = {'mbom': 'mbom.xlsm'}
TABULATOR = {
    'overview': {
        'base_url': 'https://example.com/metrics/',
        'path': '$year$/kpi-table-$year$.json',
        'years': [2022],
        'matrix': [
            ['section', 'Section', False, 'L'],
            ['name', 'Name', False, 'L'],
            ['unit', 'Unit', False, 'C'],
            ['all', 'ALL', True, 'R'],
            ['pr1', 'PR1', True, 'R'],
            ['pr2', 'PR2', True, 'R'],
            ['pr3', 'PR3', True, 'R'],
            ['description', 'Description', False, 'L'],
        ],
        'verify_server_certificate': False,
    },
    'metrics': {
        'base_url': 'https://example.com/metrics/',
        'paths': {
            'review_effectivity': '$year$/review_effectivity/kpi-review_effectivity-per_product-report-$year$.json',
            'sprint_effectivity': '$year$/sprint_effectivity/kpi-sprint_effectivity-per_product-report-$year$.json',
            'task_traceability': '$year$/task_traceability/kpi-task_traceability-per_product-report-$year$.json',
        },
        'years': [2021, 2022],
        'matrix': [
            ['month', 'Month', False, 'L'],
            ['all', 'ALL', True, 'R'],
            ['pr1', 'PR1', True, 'R'],
            ['pr2', 'PR2', True, 'R'],
            ['pr3', 'PR3', True, 'R'],
            ['trend_all', '±ALL', True, 'R'],
            ['trend_pr1', '±PR1', True, 'R'],
            ['trend_pr2', '±PR2', True, 'R'],
            ['trend_pr3', '±PR3', True, 'R'],
        ],
        'verify_server_certificate': False,
    },
}

from laskea.api.excel import mbom_table  # noqa
from laskea.api.jira import (  # noqa
    login,
    markdown_heading,
    markdown_list,
    markdown_table,
    parent_children_sections,
    query,
    separated_values_list,
)
from laskea.embed import (  # noqa
    dl,
    h1,
    h2,
    h3,
    h4,
    h5,
    h6,
    kpi_table,
    mbom_table,
    metrics_table,
    ol,
    svl,
    table,
    test_plans,
    ul,
)

__all__ = [
    'REQUESTS_TIMEOUT_SECS',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'dl',
    'login',
    'markdown_heading',
    'markdown_table',
    'markdown_list',
    'query',
    'ol',
    'svl',
    'table',
    'ul',
    'kpi_table',
    'mbom_table',
    'metrics_table',
    'parent_children_sections',
    'test_plans',
]
