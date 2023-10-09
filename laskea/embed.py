"""Calculate (Finnish: laskea) some parts - embeddings."""
from typing import Dict, Union, no_type_check

from atlassian import Jira  # type: ignore # noqa

import laskea
import laskea.api.excel as exc
import laskea.api.jira as api
import laskea.api.tabulator as tab

DB: Dict[str, Union[None, Jira]] = {'handle': None}


@no_type_check
def mbom_table(configuration=None) -> None:
    """Public document interface."""
    if configuration is None:
        configuration = laskea.EXCEL['mbom']

    print(exc.mbom_table(configuration))


@no_type_check
def metrics_table(configuration=None) -> None:
    """Public document interface."""
    if configuration is None:
        configuration = laskea.TABULATOR['overview']

    print(tab.tabulator_overview_table(configuration))


@no_type_check
def kpi_table(selected, configuration=None) -> None:
    """Public document interface."""
    if configuration is None:
        configuration = laskea.TABULATOR['metrics']

    print(tab.tabulator_kpi_table(configuration, selected))


@no_type_check
def test_plans(
    parent_jql: str = '',
    children_jql: str = '',
    parent_type: str = 'Test Plan',
    children_type: str = 'Test Case',
    data=None,
) -> None:
    """Public document interface for the sub(sub)section document part generation from JIRA parents with children."""
    if data is None:
        if not DB.get('handle', None):
            DB['handle'] = api.login()

        print(api.parent_children_sections(DB['handle'], parent_jql, children_jql, parent_type, children_type))
    else:
        print(api.parent_children_sections(DB['handle'], parent_jql, children_jql, parent_type, children_type, data))


@no_type_check
def svl(
    query_text: str = '',
    key_magic: bool = False,
    field_sep: str = laskea.PIPE,
    replacement: str = laskea.FS_SLUG,
    data=None,
) -> None:
    """Public separated values list interface."""
    if data is None:
        if not DB.get('handle', None):
            DB['handle'] = api.login()

        print(
            api.separated_values_list(
                DB['handle'], query_text, key_magic=key_magic, field_sep=field_sep, replacement=replacement
            )
        )
    else:
        print(
            api.separated_values_list(
                DB['handle'], query_text, key_magic=key_magic, field_sep=field_sep, replacement=replacement, data=data
            )
        )


@no_type_check
def table(query_text: str = '', show_summary: bool = False, column_fields=None, data=None) -> None:
    """Public document interface."""
    if data is None:
        if not DB.get('handle', None):
            DB['handle'] = api.login()

        print(api.markdown_table(DB['handle'], query_text, show_summary=show_summary, column_fields=column_fields))
    else:
        print(
            api.markdown_table(
                DB['handle'], query_text, show_summary=show_summary, column_fields=column_fields, data=data
            )
        )


@no_type_check
def dl(query_text: str = '', data=None) -> None:
    """Public document interface for definition list."""
    if data is None:
        if not DB.get('handle', None):
            DB['handle'] = api.login()

        print(api.markdown_list(DB['handle'], query_text, list_type='dl'))
    else:
        print(api.markdown_list(DB['handle'], query_text, list_type='dl', data=data))


@no_type_check
def ol(query_text: str = '', data=None) -> None:
    """Public document interface for ordered list."""
    if data is None:
        if not DB.get('handle', None):
            DB['handle'] = api.login()

        print(api.markdown_list(DB['handle'], query_text, list_type='ol'))
    else:
        print(api.markdown_list(DB['handle'], query_text, list_type='ol', data=data))


@no_type_check
def ul(query_text: str = '', data=None) -> None:
    """Public document interface for unordered list."""
    if data is None:
        if not DB.get('handle', None):
            DB['handle'] = api.login()

        print(api.markdown_list(DB['handle'], query_text, list_type='ul'))
    else:
        print(api.markdown_list(DB['handle'], query_text, list_type='ul', data=data))


@no_type_check
def hx(level: int, query_text: str = '', data=None) -> None:
    """Public document interface for headings 1 through 6."""
    if data is None:
        if not DB.get('handle', None):
            DB['handle'] = api.login()

        print(api.markdown_heading(DB['handle'], query_text, level=level))
    else:
        print(api.markdown_heading(api.Jira(''), query_text, level=level, data=data))


@no_type_check
def h1(query_text: str = '', data=None) -> None:
    """Public document interface for heading 1."""
    return hx(1, query_text, data)


@no_type_check
def h2(query_text: str = '', data=None) -> None:
    """Public document interface for heading 2."""
    return hx(2, query_text, data)


@no_type_check
def h3(query_text: str = '', data=None) -> None:
    """Public document interface for heading 3."""
    return hx(3, query_text, data)


@no_type_check
def h4(query_text: str = '', data=None) -> None:
    """Public document interface for heading 4."""
    return hx(4, query_text, data)


@no_type_check
def h5(query_text: str = '', data=None) -> None:
    """Public document interface for heading 5."""
    return hx(5, query_text, data)


@no_type_check
def h6(query_text: str = '', data=None) -> None:
    """Public document interface for heading 6."""
    return hx(6, query_text, data)
