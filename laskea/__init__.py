"""Calculate (Finnish: laskea) some parts.."""
# [[[fill git_describe()]]]
__version__ = '2022.2.27+parent.3ebde2bc-dirty'
# [[[end]]] (checksum: 8bc15bda8a66809a6ea8904ad12e4a32)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)
