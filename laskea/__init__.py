"""Calculate (Finnish: laskea) some parts.."""
# [[[fill git_describe()]]]
__version__ = '2022.2.27+parent.23e77923-dirty'
# [[[end]]] (checksum: cee958228a2f2660e9a16aa328d43132)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)
