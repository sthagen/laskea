import pytest

import laskea.embed as emb

HEADING_FIXTURE = {
    'rows': [
        {
            'key': 'ABC-42',
            'summary': 'Some issue to show off the headings',
        }
    ]
}
HEADING_PAYLOAD_POSTFIX = (
    f' [{HEADING_FIXTURE["rows"][0]["key"]}]('
    f'https://remote-jira-instance.example.com/browse/{HEADING_FIXTURE["rows"][0]["key"]})'
    f' - {HEADING_FIXTURE["rows"][0]["summary"]}\n'
)

UO_LIST_FIXTURE = {
    'rows': [
        {
            'key': 'ABC-42',
            'summary': 'First issue to show off the ordered and unordered lists',
        },
        {
            'key': 'ABC-1001',
            'summary': 'Second issue to show off the ordered and unordered lists',
        },
    ]
}
UO_LIST_PAYLOAD_POSTFIXES = tuple(
    f' [{row["key"]}](https://remote-jira-instance.example.com/browse/{row["key"]})' f' - {row["summary"]}'
    for row in UO_LIST_FIXTURE['rows']
)

D_LIST_FIXTURE = {
    'rows': [
        {
            'key': 'ABC-42',
            'summary': 'First issue to show off the definition lists',
        },
        {
            'key': 'ABC-1001',
            'summary': 'Second issue to show off the definition lists',
        },
    ]
}
D_LIST_PAYLOADS = tuple(
    f'[{row["key"]}](https://remote-jira-instance.example.com/browse/{row["key"]})\n' f':{row["summary"]}\n'
    for row in D_LIST_FIXTURE['rows']
)


@pytest.mark.parametrize('level', [lv for lv in range(1, 7 - 1)])
def test_embed_headings(level, capsys):
    hx = [None, emb.h1, emb.h2, emb.h3, emb.h4, emb.h5, emb.h6]
    token = '#' * level
    assert hx[level](query_text='', data=HEADING_FIXTURE) is None
    out, err = capsys.readouterr()
    assert not err
    assert out.strip() == f'{token}{HEADING_PAYLOAD_POSTFIX}'.strip()


@pytest.mark.parametrize('kind,marker', [('ol', '1.'), ('ul', '-')])
def test_embed_uo_lists(kind, marker, capsys):
    lx = {'ol': emb.ol, 'ul': emb.ul}
    expected = '\n'.join(f'{marker}{UO_LIST_PAYLOAD_POSTFIXES[slot]}' for slot in (0, 1))
    assert lx[kind](query_text='', data=UO_LIST_FIXTURE) is None
    out, err = capsys.readouterr()
    assert not err
    assert out.strip() == expected


def test_embed_d_list(capsys):
    expected = '\n'.join(D_LIST_PAYLOADS) + '\n' + '\n'
    assert emb.dl(query_text='', data=D_LIST_FIXTURE) is None
    out, err = capsys.readouterr()
    assert not err
    assert out == expected
