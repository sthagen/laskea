"""Calculate (Finnish: laskea) some parts."""
from laskea.api.jira import login, markdown_list, markdown_table, query
from laskea.laskea import ol, table, ul

# [[[fill git_describe()]]]
__version__ = '2022.3.5+parent.7806167e'
# [[[end]]] (checksum: dd9ca4af591680785a0acebc61100e47)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)
__all__ = ['login', 'markdown_table', 'markdown_list', 'query', 'ol', 'table', 'ul']
