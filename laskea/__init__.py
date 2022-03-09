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

from laskea.api.jira import login, markdown_heading, markdown_list, markdown_table, query  # noqa
from laskea.embed import dl, h1, h2, h3, h4, h5, h6, ol, table, ul  # noqa

# [[[fill git_describe()]]]
__version__ = '2022.3.9+parent.838249fb'
# [[[end]]] (checksum: 7aa3f7bd97d3b07d73c0c20d48e33e1b)
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
]
