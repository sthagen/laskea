"""Calculate (Finnish: laskea) some parts."""
import logging
import os
import pathlib
from typing import Union, no_type_check

# [[[fill git_describe()]]]
__version__ = '2023.12.4+parent.g0a7b0dd4'
# [[[end]]] (checksum: 9292942ca3359173faa7007f070b73a8)
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

FILTER_ORDER_TYPE = list[str]
PAYLOAD_PAIR_TYPE = list[str]
FILTER_PAYLOAD_TYPE = list[PAYLOAD_PAIR_TYPE]
FILTER_MAP_TYPE = dict[str, Union[FILTER_ORDER_TYPE, FILTER_PAYLOAD_TYPE]]

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
DEFAULT_CAPTION = "$NL$$NL$Table: Search '$QUERY_TEXT$' resulted in $ISSUE_COUNT$ issue$SINGULAR$$PLURAL$s$"
DEFAULT_JOIN_STRING = ' <br>'
BASE_MARKERS = os.getenv(f'{APP_ENV}_MARKERS', DEFAULT_MARKERS)
BASE_LF_ONLY = bool(os.getenv(f'{APP_ENV}_LF_ONLY', DEFAULT_LF_ONLY))
BASE_CAPTION = bool(os.getenv(f'{APP_ENV}_CAPTION', DEFAULT_CAPTION))
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

log = logging.getLogger()  # Temporary refactoring: module level logger
LOG_FOLDER = pathlib.Path('logs')
LOG_FILE = f'{APP_ALIAS}.log'
LOG_PATH = pathlib.Path(LOG_FOLDER, LOG_FILE) if LOG_FOLDER.is_dir() else pathlib.Path(LOG_FILE)
LOG_LEVEL = logging.INFO

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
    'FILTER_MAP_TYPE',
    'FILTER_ORDER_TYPE',
    'FILTER_PAYLOAD_TYPE',
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


@no_type_check
def init_logger(name=None, level=None):
    """Initialize module level logger"""
    global log  # pylint: disable=global-statement

    log_format = {
        'format': '%(asctime)s.%(msecs)03d %(levelname)s [%(name)s]: %(message)s',
        'datefmt': '%Y-%m-%dT%H:%M:%S',
        # 'filename': LOG_PATH,
        'level': LOG_LEVEL if level is None else level,
    }
    logging.basicConfig(**log_format)
    log = logging.getLogger(APP_ENV if name is None else name)
    log.propagate = True


init_logger(name=APP_ENV, level=logging.DEBUG if DEBUG else None)
