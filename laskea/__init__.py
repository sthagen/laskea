"""Calculate (Finnish: laskea) some parts.."""
from laskea.api.jira import login, markdown_table, query
from laskea.laskea import table

# [[[fill git_describe()]]]
__version__ = '2022.3.3+parent.22b5b468'
# [[[end]]] (checksum: 45ca77c568dddeda3a8004c2106a7422)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)
__all__ = ['login', 'markdown_table', 'query', 'table']
