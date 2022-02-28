"""Calculate (Finnish: laskea) some parts.."""
# [[[fill git_describe()]]]
__version__ = '2022.2.28+parent.39977ab5'
# [[[end]]] (checksum: 0fa8d9244fa668303dc9fc7395bfb5a9)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)
