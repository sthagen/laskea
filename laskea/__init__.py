"""Calculate (Finnish: laskea) some parts."""
import os

from laskea.api.jira import login, markdown_heading, markdown_list, markdown_table, query
from laskea.embed import dl, h1, h2, h3, h4, h5, h6, ol, table, ul

# [[[fill git_describe()]]]
__version__ = '2022.3.6+parent.0d08af64'
# [[[end]]] (checksum: 3e7e748efd160fd5bd7ca3fee55e660a)
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

APP_NAME = 'Calculate (Finnish: laskea) some parts.'
APP_ALIAS = 'laskea'
APP_ENV = 'ASCIINATOR'
DEBUG = bool(os.getenv(f'{APP_ENV}_DEBUG', ''))
QUIET = False
ENCODING = 'utf-8'
ENCODING_ERRORS_POLICY = 'ignore'
DEFAULT_CONFIG_NAME = '.laskea.json'
OPEN_BRACKET = '['
CLOSE_BRACKET = ']'
DEFAULT_MARKERS = f'{OPEN_BRACKET * 3}fill {CLOSE_BRACKET * 3} {OPEN_BRACKET * 3}end{CLOSE_BRACKET * 3}'
BASE_MARKERS = os.getenv(f'{APP_ENV}_MARKERS', DEFAULT_MARKERS)
FAKE_SECRET = '*' * 13
