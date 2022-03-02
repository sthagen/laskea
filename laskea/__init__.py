"""Calculate (Finnish: laskea) some parts.."""
from laskea.api.jira import login, markdown_table, query
from laskea.laskea import table

# [[[fill git_describe()]]]
__version__ = '2022.3.2+parent.f99aa559'
# [[[end]]] (checksum: 49924d52a2e326cf6e443c04627907bc)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)
__all__ = ['login', 'markdown_table', 'query', 'table']
