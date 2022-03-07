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
APP_NAME = 'ASCIINATOR'
APP_ENV = APP_NAME

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

BASE_USER = os.getenv(f'{APP_ENV}_USER', '')
BASE_PASS = os.getenv(f'{APP_ENV}_TOKEN', '')
BASE_URL = os.getenv(f'{APP_ENV}_BASE_URL', '')
BASE_IS_CLOUD = bool(os.getenv(f'{APP_ENV}_IS_CLOUD', ''))
BASE_COL_FIELDS = json.loads(os.getenv(f'{APP_ENV}_COL_FIELDS', json.dumps(DEFAULT_COLUMN_FIELDS)))
BASE_COL_MAPS = json.loads(os.getenv(f'{APP_ENV}_COL_MAPS', json.dumps(KNOWN_CI_FIELDS)))


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
    print(f'INFO: Upstream JIRA instance is addressed per {"cloud" if is_cloud else "server"} rules', file=sys.stderr)
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
        issues = handle.jql(jql_text)
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
                table[slot][key] = '<br>'.join(cell)  # noqa
            col_wid[key] = max(len(table[slot][key]), col_wid[key])  # noqa

    header_cells = [key.ljust(col_wid[key]) for key in columns]
    header = f'| {" | ".join(header_cells)} |'

    separator_cells = ['-' * (col_wid[key] + 1) for key in columns]
    separator = f'|:{"|:".join(separator_cells)}|'

    rows = [f'| {" | ".join(str(v).ljust(col_wid[k]) for k, v in line.items())} |' for line in table]
    issues = len(table)
    summary = f'\n\n{issues} issue{"" if issues == 1 else "s"}'
    return '\n'.join([header] + [separator] + rows) + summary


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
        return '\n'.join(xl) + '\n'
    elif list_type == 'dl':
        # 'Term'
        # ':definition of term'
        #
        xl = tuple(f'{key}\n:{summary}\n' for key, summary in items)
        return '\n'.join(xl) + '\n'
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
            return message
        else:
            return ''
    level_range = tuple(range(1, 6 + 1))
    if level in level_range:
        heading_token = '#' * level
        xl = tuple(f'{heading_token} {key} - {summary}' for key, summary in items)
        return '\n'.join(xl)
    else:
        message = f'Unexpected level for heading ({level}) in markdown_heading not in ({level_range})'
        if not laskea.DRY_RUN:
            print(message, file=sys.stderr)
        return message
