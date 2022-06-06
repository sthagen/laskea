# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned,line-too-long
"""JIRA proxy connector API for code generation."""
import copy
import json
import os
import sys
from typing import Iterable, Mapping, Sized, Union, no_type_check

import jmespath
from atlassian import Jira  # type: ignore # noqa
from requests.exceptions import HTTPError

import laskea

API_BASE_URL = 'https://example.com'

DEFAULT_COLUMN_FIELDS = ['Key', 'Summary', ['Priority', 'P'], 'Status', 'Custom Field Wun', 'Custom Field Other (CFO)']

WUN_ID = 'customfield_11501'
ANOTHER_ID = 'customfield_13901'
KNOWN_CI_FIELDS = {
    'key': ['key', 'key'],
    'summary': ['summary', 'fields.summary'],
    'priority': ['priority', 'fields.priority.name'],
    'status': ['status', 'fields.status.name'],
    'custom field name': [WUN_ID, f'fields.{WUN_ID}'],
    'custom field other': [ANOTHER_ID, f'fields.{ANOTHER_ID}[].value'],
}

BASE_USER = os.getenv(f'{laskea.APP_ENV}_USER', '')
BASE_PASS = os.getenv(f'{laskea.APP_ENV}_TOKEN', '')
BASE_URL = os.getenv(f'{laskea.APP_ENV}_BASE_URL', '')
BASE_IS_CLOUD = bool(os.getenv(f'{laskea.APP_ENV}_IS_CLOUD', ''))
BASE_COL_FIELDS = json.loads(os.getenv(f'{laskea.APP_ENV}_COL_FIELDS', json.dumps(DEFAULT_COLUMN_FIELDS)))
BASE_COL_MAPS = json.loads(os.getenv(f'{laskea.APP_ENV}_COL_MAPS', json.dumps(KNOWN_CI_FIELDS)))
BASE_JOIN_STRING = os.getenv(f'{laskea.APP_ENV}_JOIN_STRING', ' <br>')
BASE_LF_ONLY = bool(os.getenv(f'{laskea.APP_ENV}_LF_ONLY', 'YES'))
LF = '\n'


def mock(number: int) -> int:
    """Intermediate for starting the dev env in a valid state."""
    return number


def login(user: str = '', token: str = '', url: str = '', is_cloud: bool = False) -> Jira:  # nosec
    """LatAli"""
    if not user:
        user = BASE_USER
    if not token:
        token = BASE_PASS
    if not url:
        url = BASE_URL
    if not is_cloud:
        is_cloud = BASE_IS_CLOUD
    if not user or not token or not url:
        raise ValueError('User, Token, and URL are all required for login.')
    return Jira(url=url, username=user, password=token, cloud=is_cloud)


@no_type_check
def query(handle: Jira, jql_text: str, column_fields=None) -> dict:
    """EggLayingWoolMilkDear."""

    if not column_fields:
        column_fields = BASE_COL_FIELDS

    if not jql_text.strip():
        return {
            'jql_text': jql_text,
            'error': 'Empty JIRA Query Language text detected',
        }

    completed_column_fields = []
    for entry in column_fields:
        if isinstance(entry, str):
            candidate, concept, label = entry.lower(), entry, entry
        else:
            try:
                concept, label = entry
                candidate = concept.lower()
            except TypeError:
                return {
                    'jql_text': jql_text,
                    'column_fields': column_fields,
                    'parsed_columns': completed_column_fields,
                    'error': f'The column ({entry}) is neither a string nor a pair of (concept, label)',
                }

        for field in BASE_COL_MAPS.keys():
            if field in candidate:
                completed_column_fields.append(
                    {
                        'path': BASE_COL_MAPS[field][1],
                        'id': BASE_COL_MAPS[field][0],
                        'concept': concept,
                        'label': label,
                        'field': field,
                    }
                )

    if not completed_column_fields:
        return {
            'jql_text': jql_text,
            'column_fields': column_fields,
            'error': 'Completed column fields empty (no known fields?)',
        }

    try:
        issues = handle.jql(jql_text, limit=1000)
    except (HTTPError, RuntimeError) as err:
        return {
            'jql_text': jql_text,
            'column_fields': column_fields,
            'parsed_columns': completed_column_fields,
            'error': str(err),
        }

    pairs = [(col['label'], col['path']) for col in completed_column_fields]
    rows = [{label: jmespath.search(path, issue) or [''] for label, path in pairs} for issue in issues['issues']]
    return {
        'jql_text': jql_text,
        'column_fields': column_fields,
        'parsed_columns': completed_column_fields,
        'error': None,
        'rows': rows,
    }


@no_type_check
def markdown_table(
    handle: Jira, jql_text: str, column_fields=None, data: Mapping[str, Union[object, Iterable, Sized]] = None
) -> str:
    """Yes we can ... document later."""
    if data is None:
        data = query(handle, jql_text, column_fields)
    if data.get('error', ''):
        return json.dumps(data, indent=2)

    if not data['rows']:
        if laskea.STRICT:
            message = f'WARNING: received 0 results for JQL ({jql_text}) and table'
            if not laskea.DRY_RUN:
                print(message, file=sys.stderr)
            return message
        else:
            return ''

    table = copy.deepcopy(data['rows'])
    columns = list(table[0].keys())  # noqa
    col_wid = {key: len(key) for key in columns}
    for slot, record in enumerate(table):
        for key, cell in record.items():
            if key.lower() == 'key':
                table[slot][key] = f'[{cell}]({BASE_URL.strip("/")}/browse/{cell})'  # noqa
            if not isinstance(cell, str):
                table[slot][key] = BASE_JOIN_STRING.join(cell)  # noqa
            col_wid[key] = max(len(table[slot][key]), col_wid[key])  # noqa

    header_cells = [key.ljust(col_wid[key]) for key in columns]
    header = f'| {" | ".join(header_cells)} |'

    separator_cells = ['-' * (col_wid[key] + 1) for key in columns]
    separator = f'|:{"|:".join(separator_cells)}|'

    rows = [f'| {" | ".join(str(v).ljust(col_wid[k]) for k, v in line.items())} |' for line in table]
    issues = len(table)
    summary = f'\n\n{issues} issue{"" if issues == 1 else "s"}'
    the_table = '\n'.join([header] + [separator] + rows) + summary
    return the_table.replace('\r', '') if BASE_LF_ONLY else the_table


@no_type_check
def markdown_list(
    handle: Jira,
    jql_text: str,
    column_fields=None,
    list_type: str = 'ul',
    data: Mapping[str, Union[object, Iterable, Sized]] = None,
) -> str:
    """Yes we can ... document later."""
    if data is None:
        data = query(handle, jql_text, column_fields)
    if data.get('error', ''):
        return json.dumps(data, indent=2)

    if not data['rows']:
        if laskea.STRICT:
            message = f'WARNING: received 0 results for JQL ({jql_text}) and {list_type}'
            if not laskea.DRY_RUN:
                print(message, file=sys.stderr)
            return message
        else:
            return ''

    items = []
    for slot, record in enumerate(data['rows']):
        k, v = '', ''
        for key, cell in record.items():
            if key.lower() not in ('key', 'summary'):
                continue
            if key.lower() == 'key':
                k = f'[{cell}]({BASE_URL.strip("/")}/browse/{cell})'
            else:
                v = cell
        items.append((k, v))

    if list_type in ('ol', 'ul'):
        lt = '-' if list_type == 'ul' else '1.'  # implicit 'ol'
        xl = tuple(f'{lt} {key} - {summary}' for key, summary in items)
        the_list = '\n'.join(xl) + '\n'
        return the_list.replace('\r', '') if BASE_LF_ONLY else the_list
    elif list_type == 'dl':
        # 'Term'
        # ':definition of term'
        #
        xl = tuple(f'{key}\n:{summary}\n' for key, summary in items)
        the_list = '\n'.join(xl) + '\n'
        return the_list.replace('\r', '') if BASE_LF_ONLY else the_list
    else:
        return f'Unexpected list type ({list_type}) in markdown_list not in ({("dl", "ol", "ul")})' + '\n'


@no_type_check
def markdown_heading(
    handle: Jira,
    jql_text: str,
    column_fields=None,
    level: int = 1,
    data: Mapping[str, Union[object, Iterable, Sized]] = None,
) -> str:
    """Yes we can ... document later."""
    if data is None:
        data = query(handle, jql_text, column_fields)
    if data.get('error', ''):
        return json.dumps(data, indent=2)

    if not data['rows']:
        if laskea.STRICT:
            message = f'WARNING: received 0 results instead of 1 for JQL ({jql_text}) and h{level}'
            if not laskea.DRY_RUN:
                print(message, file=sys.stderr)
            return message
        else:
            return ''

    items = []
    for slot, record in enumerate(data['rows']):
        k, v = '', ''
        for key, cell in record.items():
            if key.lower() not in ('key', 'summary'):
                continue
            if key.lower() == 'key':
                k = f'[{cell}]({BASE_URL.strip("/")}/browse/{cell})'
            else:
                v = cell
        items.append((k, v))
    received = len(items)
    if received != 1:
        if laskea.STRICT:
            message = f'WARNING: received {received} results instead of 1 for JQL ({jql_text}) and h{level}'
            if not laskea.DRY_RUN:
                print(message, file=sys.stderr)
            return message.replace('\r', '') if BASE_LF_ONLY else message
        else:
            return ''
    level_range = tuple(range(1, 6 + 1))
    if level in level_range:
        heading_token = '#' * level
        xl = tuple(f'{heading_token} {key} - {summary}' for key, summary in items)
        the_heading = '\n'.join(xl)
        return the_heading.replace('\r', '') if BASE_LF_ONLY else the_heading
    else:
        message = f'Unexpected level for heading ({level}) in markdown_heading not in ({level_range})'
        if not laskea.DRY_RUN:
            print(message, file=sys.stderr)
        return message


@no_type_check
def fetch_jql(handle: Jira, jql_text: str) -> dict:
    """Expose the JIRA result structure directly."""
    if not jql_text.strip():
        return {
            'jql_text': jql_text,
            'error': 'Empty JIRA Query Language text detected',
        }

    try:
        issues = handle.jql(jql_text, limit=1000)
    except (HTTPError, RuntimeError) as err:
        return {
            'jql_text': jql_text,
            'error': str(err),
        }

    return {
        'jql_text': jql_text,
        'data': issues,
        'error': None,
    }


@no_type_check
def parent_children_sections(
    handle: Jira,
    parent_jql: str,
    children_jql: str,
    parent_type_name: str,
    children_type_name: str,
    data: Mapping[str, Union[object, Iterable, Sized]] = None,
) -> str:
    """Create sub(sub)section level content representing the issue content from parent children filter results."""
    if data is None:
        data = {
            'parent_data': fetch_jql(handle, jql_text=parent_jql),
            'children_data': fetch_jql(handle, jql_text=children_jql),
        }
    if data['parent_data'].get('error', '') or data['children_data'].get('error', ''):
        return json.dumps(data, indent=2)

    doc = {}
    has_parents = {}

    for parent in data['parent_data']['issues']:
        p_id = parent['id']
        p_key = parent['key']

        p_field = parent['fields']

        p_itn = p_field['issuetype']['name']
        # assert p_itn == parent_type_name
        p_sum = p_field['summary']
        p_des = p_field['description']  # None for parent type names
        p_epic = p_field['customfield_10006']  # TODO assuming here ...
        p_created = p_field['created']  # Textual timestamps like "2019-03-12T10:01:25.000+0100"
        p_updated = p_field['updated']

        doc[p_key] = {
            'id': p_id,
            'type': p_itn,
            'summary': p_sum,
            'description': p_des,
            'epic': p_epic,
            'created': p_created,
            'updated': p_updated,
            'children': {},
        }

        children = p_field['subtasks']

        for child in children:
            c_id = child['id']
            c_key = child['key']

            c_field = child['fields']

            c_itn = c_field['issuetype']['name']
            # assert c_itn == children_type_name
            c_sum = c_field['summary']

            doc[p_key]['children'][c_key] = {
                'id': c_id,
                'type': c_itn,
                'summary': c_sum,
                'description': None,
                'created': None,
                'updated': None,
            }
            if c_key not in has_parents:
                has_parents[c_key] = []
            has_parents[c_key].append(p_key)

    for child in data['children_data']['issues']:
        c_id = child['id']
        c_key = child['key']

        c_field = child['fields']

        p_key = c_field['parent']['key']
        # assert p_key in has_parents[c_key]
        p_itn = c_field['parent']['issuetype']['name']
        # assert p_itn == parent_type_name

        c_itn = c_field['issuetype']['name']
        # assert c_itn == children_type_name
        c_sum = c_field['summary']
        c_des = c_field['description']  # Table or list or notes for children type names
        c_created = c_field['created']
        c_updated = c_field['updated']

        doc[p_key]['children'][c_key]['description'] = c_des
        doc[p_key]['children'][c_key]['created'] = c_created
        doc[p_key]['children'][c_key]['updated'] = c_updated

    return doc_to_markdown(doc, parent_type_name, children_type_name)


@no_type_check
def doc_to_markdown(doc, parent_type_name: str, children_type_name: str) -> str:
    """Transform the document content to markdown."""
    md = []
    for p_key, p_tree in doc.items():
        p_head = f'## {parent_type_name} {p_tree["summary"].title()} ({p_key})'.strip(LF)
        c_count = len(p_tree['children'])
        c_type_disp = f'{children_type_name}{"" if c_count == 1 else "s"}'
        p_para = f'The {p_tree["type"]} consists of {c_count} {c_type_disp}'.strip(LF)

        c_parts = []
        for c_key, c_data in p_tree['children'].items():
            c_head = f'### {children_type_name} {c_data["summary"].title()} ({c_key})'.strip(LF)
            c_content = c_data['description'].strip(LF)
            c_parts.extend([LF, c_head, LF, c_content])

        md.extend([LF, p_head, LF, p_para])
        md.extend(c_parts)

    md.append(LF)
    return LF.join(md)
