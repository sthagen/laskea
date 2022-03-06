"""Calculate (Finnish: laskea) some parts - embeddings."""
from typing import Dict, Union, no_type_check

from atlassian import Jira  # type: ignore # noqa

import laskea.api.jira as api

DB: Dict[str, Union[None, Jira]] = {'handle': None}


@no_type_check
def table(query_text: str = '') -> None:
    """Public document interface."""
    if not DB.get('handle', None):
        DB['handle'] = api.login()

    print(api.markdown_table(DB['handle'], query_text))


@no_type_check
def dl(query_text: str = '') -> None:
    """Public document interface for definition list."""
    if not DB.get('handle', None):
        DB['handle'] = api.login()

    print(api.markdown_list(DB['handle'], query_text, list_type='dl'))


@no_type_check
def ol(query_text: str = '') -> None:
    """Public document interface for ordered list."""
    if not DB.get('handle', None):
        DB['handle'] = api.login()

    print(api.markdown_list(DB['handle'], query_text, list_type='ol'))


@no_type_check
def ul(query_text: str = '') -> None:
    """Public document interface for unordered list."""
    if not DB.get('handle', None):
        DB['handle'] = api.login()

    print(api.markdown_list(DB['handle'], query_text, list_type='ul'))


@no_type_check
def h1(query_text: str = '') -> None:
    """Public document interface for heading 1."""
    if not DB.get('handle', None):
        DB['handle'] = api.login()

    print(api.markdown_heading(DB['handle'], query_text, level=1))


@no_type_check
def h2(query_text: str = '') -> None:
    """Public document interface for heading 2."""
    if not DB.get('handle', None):
        DB['handle'] = api.login()

    print(api.markdown_heading(DB['handle'], query_text, level=2))


@no_type_check
def h3(query_text: str = '') -> None:
    """Public document interface for heading 3."""
    if not DB.get('handle', None):
        DB['handle'] = api.login()

    print(api.markdown_heading(DB['handle'], query_text, level=3))


@no_type_check
def h4(query_text: str = '') -> None:
    """Public document interface for heading 4."""
    if not DB.get('handle', None):
        DB['handle'] = api.login()

    print(api.markdown_heading(DB['handle'], query_text, level=4))


@no_type_check
def h5(query_text: str = '') -> None:
    """Public document interface for heading 5."""
    if not DB.get('handle', None):
        DB['handle'] = api.login()

    print(api.markdown_heading(DB['handle'], query_text, level=6))


@no_type_check
def h6(query_text: str = '') -> None:
    """Public document interface for heading 6."""
    if not DB.get('handle', None):
        DB['handle'] = api.login()

    print(api.markdown_heading(DB['handle'], query_text, level=6))
