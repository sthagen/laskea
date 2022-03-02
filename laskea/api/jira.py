# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned,line-too-long
"""JIRA proxy connector API for code generation."""
import copy
import json
import os
from typing import no_type_check

import jmespath
from atlassian import Jira  # type: ignore # noqa

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
BASE_COL_FIELDS = json.loads(os.getenv(f'{APP_ENV}_COL_FIELDS', json.dumps(DEFAULT_COLUMN_FIELDS)))
BASE_COL_MAPS = json.loads(os.getenv(f'{APP_ENV}_COL_MAPS', json.dumps(KNOWN_CI_FIELDS)))


def mock(number: int) -> int:
    """Intermediate for starting the dev env in a valid state."""
    return number


def login(user: str = '', token: str = '', url: str = '') -> Jira:
    """LatAli"""
    if not user:
        user = BASE_USER
    if not token:
        token = BASE_PASS
    if not url:
        url = BASE_URL
    if not user or not token or not url:
        raise ValueError('User, Token, and URL are all required for login.')

    return Jira(url=url, username=user, password=token)


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

    # dynamics below
    try:
        handle.user(handle.username)['name'] == handle.username
    except RuntimeError as err:
        return {
            'jql_text': jql_text,
            'column_fields': column_fields,
            'parsed_columns': completed_column_fields,
            'error': str(err),
        }

    issues = handle.jql(jql_text)
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
def markdown_table(handle: Jira, jql_text: str, column_fields=None) -> str:
    """Yes we can ... document later."""
    data = query(handle, jql_text, column_fields)
    if data.get('error', ''):
        return json.dumps(data, indent=2)

    if not data['rows']:
        return 'WARNING: Empty table!'

    table = copy.deepcopy(data['rows'])
    columns = list(table[0].keys())
    col_wid = {key: len(key) for key in columns}
    for slot, record in enumerate(table):
        for key, cell in record.items():
            if key.lower() == 'key':
                table[slot][key] = f'[{cell}]({BASE_URL.strip("/")}/browse/{cell})'
            if not isinstance(cell, str):
                table[slot][key] = '<br>'.join(cell)
            col_wid[key] = max(len(table[slot][key]), col_wid[key])

    header_cells = [key.ljust(col_wid[key]) for key in columns]
    header = f'| {" | ".join(header_cells)} |'

    separator_cells = ['-' * (col_wid[key] + 1) for key in columns]
    separator = f'|:{"|:".join(separator_cells)}|'

    rows = [f'| {" | ".join(str(v).ljust(col_wid[k]) for k, v in line.items())} |' for line in table]
    issues = len(table)
    summary = f'\n\n{issues} issue{"" if issues == 1 else "s"}'
    return '\n'.join([header] + [separator] + rows) + summary
