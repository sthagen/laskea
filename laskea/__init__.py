"""Calculate (Finnish: laskea) some parts.."""
# [[[fill git_describe()]]]
__version__ = '2022.2.27+sha1.6d5d53ba-dirty'
# [[[end]]] (checksum: 09441222a47fbf41a0b3e49fe3cc8c61)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'sha1'
)
