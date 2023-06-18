# -*- coding: utf-8 -*-
"""Tabulator style REST/JSON data proxy connector API for code generation."""
from typing import Mapping, no_type_check

import jmespath
import requests  # noqa
from urllib3.exceptions import InsecureRequestWarning  # noqa

import laskea

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)  # type: ignore


@no_type_check
def parse_matrix(configuration: Mapping[str, object]) -> Mapping[str, object]:
    """DRY."""
    matrix = configuration['matrix']
    parsed = {
        'columns': tuple(key for key, _, _, _ in matrix),  # noqa
        'labels': tuple(label for _, label, _, _ in matrix),  # noqa
        'is_numeric': [key for key, _, is_num, _ in matrix if is_num],  # noqa
        'align': [lcr for _, _, _, lcr in matrix],  # noqa
    }

    parsed['out_round'] = tuple(
        (key, 1 if key in parsed['is_numeric'] else 0) for key, _ in zip(parsed['columns'], parsed['labels'])
    )
    parsed['out_format'] = tuple(
        (key, '5.1f' if key in parsed['is_numeric'] else '') for key, _ in zip(parsed['columns'], parsed['labels'])
    )
    parsed['column_fields'] = tuple((key, label) for key, label in zip(parsed['columns'], parsed['labels']))

    return parsed


@no_type_check
def tabulator_overview_table(configuration: Mapping[str, object]) -> str:
    """Because we can ... document later."""
    m = parse_matrix(configuration)
    over_view = f'{configuration["base_url"]}{configuration["path"]}'
    http_options = {'timeout': laskea.REQUESTS_TIMEOUT_SECS}

    data = []
    data_version = ''
    for year in configuration['years']:  # noqa
        source = over_view.replace('$year$', str(year))
        r = requests.get(source, verify=configuration['verify_server_certificate'], **http_options)  # nosec B113
        as_json = r.json()
        data_version = jmespath.search('data_version', as_json)
        for entry in jmespath.search('data[]', as_json):
            record = [entry[key] for key, _ in m['column_fields']]  # noqa
            for i, (l, f) in enumerate(m['out_format']):  # noqa
                if i and f:
                    if record[i] is not None:
                        try:
                            v = float(record[i])
                            record[i] = f'{round(v, m["out_round"][i][1]): {f}}'  # noqa
                        except ValueError:
                            pass
                    else:
                        record[i] = ''

            data.append(record)

    header_widths = [len(label) for _, label in m['column_fields']]  # noqa
    widths = header_widths[:]
    selection = data[:]
    for record in selection:
        for i, s in enumerate(record):
            if s is not None:
                widths[i] = max(widths[i], len(s))

    header_cells = [
        m['labels'][key].rjust(widths[key])  # noqa
        if m['align'][key] == 'R'  # noqa
        else (
            m['labels'][key].ljust(widths[key])  # noqa
            if m['align'][key] == 'L'  # noqa
            else m['labels'][key].center(widths[key])  # noqa
        )  # noqa
        for key in range(len(m['column_fields']))  # noqa
    ]
    header = f'| {" | ".join(header_cells)} |'

    separator_cells = ['-' * (widths[key] + 1) for key in range(len(m['column_fields']))]  # noqa
    separator = [
        f':{v}' if lcr == 'L' else (f'{v}:' if lcr == 'R' else f':{v[:-1]}:')
        for lcr, v in zip(m['align'], separator_cells)  # noqa
    ]
    separator_display = f'|{"|".join(separator)}|'

    rows = []
    for row in selection:
        rows.append(
            [
                str(v).rjust(widths[k])
                if m['align'][k] == 'R'  # noqa
                else (str(v).ljust(widths[k]) if m['align'][k] == 'L' else str(v).center(widths[k]))  # noqa
                for k, v in enumerate(row)
            ]
        )

    rows_display = [f'| {" | ".join(v for v in row)} |' for row in rows]

    summary = f'\n\nData version: {data_version}'
    the_table = '\n'.join([header] + [separator_display] + rows_display) + summary

    return the_table.replace('\r', '') if laskea.BASE_LF_ONLY else the_table


@no_type_check
def tabulator_kpi_table(configuration: Mapping[str, object], selected: str) -> str:
    """Because we can too ... document later."""
    m = parse_matrix(configuration)
    http_options = {'timeout': laskea.REQUESTS_TIMEOUT_SECS}
    data = []
    data_version = ''
    for year in configuration['years']:  # noqa
        the_path = configuration['paths'][selected].replace('$year$', str(year))  # noqa
        source = f'{configuration["base_url"]}{the_path}'
        r = requests.get(source, configuration['verify_server_certificate'], **http_options)  # nosec B113
        as_json = r.json()
        data_version = jmespath.search('data_version', as_json)
        for entry in jmespath.search('data[]', as_json):
            record = [entry[key] for key, _ in m['column_fields']]  # noqa
            for i, (l, f) in enumerate(m['out_format']):  # noqa
                if i and f and record[i] is not None:
                    record[i] = f'{round(record[i], m["out_round"][i][1]): {f}}'  # noqa
            data.append(record)

    header_widths = [len(label) for _, label in m['column_fields']]  # noqa
    widths = header_widths[:]
    selection = sorted(data, reverse=True)[:12]
    for record in selection:
        for i, s in enumerate(record):
            widths[i] = max(widths[i], len(s))

    header_cells = [
        m['labels'][key].rjust(widths[key]) if key else m['labels'][key].ljust(widths[key])  # noqa
        for key in range(len(m['column_fields']))  # noqa
    ]
    header = f'| {" | ".join(header_cells)} |'

    separator_cells = ['-' * (widths[key] + 1) for key in range(len(m['column_fields']))]  # noqa
    separator = f'|:{separator_cells[0]}|{":|".join(separator_cells[1:])}:|'

    rows = [f'| {" | ".join(str(v).rjust(widths[k]) for k, v in enumerate(line))} |' for line in selection]

    summary = f'\n\nData version: {data_version}'
    the_table = '\n'.join([header] + [separator] + rows) + summary

    return the_table.replace('\r', '') if laskea.BASE_LF_ONLY else the_table
