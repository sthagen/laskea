import pathlib
import subprocess

__all__ = ['git_describe']

ENCODING = 'utf-8'
TARGET = """\
__version__ = '$version$+sha1.$hash_8$'\
"""


def git_describe(always: bool=True) -> None:
    """Fill in the data."""
    with open(pathlib.Path('setup.cfg'), 'rt', encoding=ENCODING) as handle:
        for line in handle:
            if line.strip().startswith('version'):
                version = line.strip().split('=')[1].strip()
    vector = ['git', 'describe']
    if always:
        vector.append('--always')
    revision = subprocess.run(vector, capture_output=True, encoding=ENCODING, text=True).stdout
    hash_8 = hash_full[:8]
    print(TARGET.replace('$hash_8$', hash_8).replace('$hash_full$', hash_full))
