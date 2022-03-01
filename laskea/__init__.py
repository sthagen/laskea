"""Calculate (Finnish: laskea) some parts.."""
from laskea.api.jira import login, markdown_table, query
from laskea.laskea import table

# [[[fill git_describe()]]]
__version__ = '2022.3.1+parent.7efa1c89-dirty'
# [[[end]]] (checksum: 58530d5151e77b9024245cb19f2801a7)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)
__all__ = ['login', 'markdown_table', 'query', 'table']
