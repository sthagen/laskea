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

    print(api.markdown_list(DB['handle'], query_text))
