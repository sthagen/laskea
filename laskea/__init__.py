"""Calculate (Finnish: laskea) some parts."""
import os

APP_NAME = 'Calculate (Finnish: laskea) some parts.'
APP_ALIAS = 'laskea'
APP_ENV = 'LASKEA'
CACHE_EXPIRY_SECONDS = int(os.getenv(f'{APP_ENV}_CACHE_EXPIRY_SECONDS', '180'))
DEBUG = bool(os.getenv(f'{APP_ENV}_DEBUG', ''))
DRY_RUN = False
VERBOSE = bool(os.getenv(f'{APP_ENV}_VERBOSE', ''))
QUIET = False
STRICT = bool(os.getenv(f'{APP_ENV}_STRICT', ''))
ENCODING = 'utf-8'
ENCODING_ERRORS_POLICY = 'ignore'
DEFAULT_CONFIG_NAME = '.laskea.json'
OPEN_BRACKET = '['
CLOSE_BRACKET = ']'
DEFAULT_MARKERS = f'{OPEN_BRACKET * 3}fill {CLOSE_BRACKET * 3} {OPEN_BRACKET * 3}end{CLOSE_BRACKET * 3}'
DEFAULT_LF_ONLY = 'YES'
DEFAULT_JOIN_STRING = ' <br>'
BASE_MARKERS = os.getenv(f'{APP_ENV}_MARKERS', DEFAULT_MARKERS)
BASE_LF_ONLY = bool(os.getenv(f'{APP_ENV}_LF_ONLY', DEFAULT_LF_ONLY))
BASE_JOIN_STRING = os.getenv(f'{APP_ENV}_JOIN_STRING', DEFAULT_JOIN_STRING)
FAKE_SECRET = '*' * 13
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

from laskea.api.jira import (  # noqa
    login,
    markdown_heading,
    markdown_list,
    markdown_table,
    parent_children_sections,
    query,
)
from laskea.embed import dl, h1, h2, h3, h4, h5, h6, kpi_table, metrics_table, ol, table, test_plans, ul  # noqa

# [[[fill git_describe()]]]
__version__ = '2022.6.8+parent.6698b850'
# [[[end]]] (checksum: fce1e9233e2cddbb01ab14888cfccfa8)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)
__all__ = [
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
    'table',
    'ul',
    'kpi_table',
    'metrics_table',
    'parent_children_sections',
    'test_plans',
]
