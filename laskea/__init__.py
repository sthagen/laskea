"""Calculate (Finnish: laskea) some parts.."""
# [[[fill git_describe()]]]
__version__ = '2022.2.27+sha1.b9032cc2'
# [[[end]]] (checksum: 9b326e7e541db02c1424e9a1b36a7c2f)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'sha1'
)
