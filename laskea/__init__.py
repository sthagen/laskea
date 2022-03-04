"""Calculate (Finnish: laskea) some parts.."""
from laskea.api.jira import login, markdown_table, markdown_unordered_list, query
from laskea.laskea import table, ul

# [[[fill git_describe()]]]
__version__ = '2022.3.4+parent.ec1ce47e'
# [[[end]]] (checksum: 29cf44ab70f2ac50ceb0372326df1ab8)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)
__all__ = ['login', 'markdown_table', 'markdown_unordered_list', 'query', 'table', 'ul']
