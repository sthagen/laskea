"""Calculate (Finnish: laskea) some parts."""
import os

from laskea.api.jira import login, markdown_list, markdown_table, query
from laskea.embed import ol, table, ul

# [[[fill git_describe()]]]
__version__ = '2022.3.5+parent.fc48b537'
# [[[end]]] (checksum: 3e532f17eb2bd6ca5389ed717eb859d1)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)
__all__ = ['login', 'markdown_table', 'markdown_list', 'query', 'ol', 'table', 'ul']

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
