"""Calculate (Finnish: laskea) some parts.."""
from laskea.api.jira import login, markdown_table, query
from laskea.laskea import table

# [[[fill git_describe()]]]
__version__ = '2022.3.1+parent.989851d8'
# [[[end]]] (checksum: 2ec216157bdb20fe4e2f061d2ea05498)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)
__all__ = ['login', 'markdown_table', 'query', 'table']
