"""Calculate (Finnish: laskea) some parts.."""
# [[[fill git_describe()]]]
__version__ = '2022.2.27+parent.d0500609-dirty'
# [[[end]]] (checksum: c3a40ec31b4476da2163e148ea826146)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)
