"""Calculate (Finnish: laskea) some parts."""
import os

from laskea.api.jira import login, markdown_list, markdown_table, query
from laskea.embed import ol, table, ul

# [[[fill git_describe()]]]
__version__ = '2022.3.5+parent.7d561a50'
# [[[end]]] (checksum: ab94f68d3d141381d8c17d52c1831302)
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
DEFAULT_MARKERS = '[[[fill ]]] [[[end]]]'
BASE_MARKERS = os.getenv(f'{APP_ENV}_MARKERS', DEFAULT_MARKERS)
FAKE_SECRET = '*' * 13
