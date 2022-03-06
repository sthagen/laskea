import pytest

import laskea.api.jira as impl
import laskea.embed as emb

URL_FIXTURE = 'https://remote-jira-instance.example.com'
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
    f'{URL_FIXTURE}/browse/{HEADING_FIXTURE["rows"][0]["key"]})'
    f' - {HEADING_FIXTURE["rows"][0]["summary"]}\n'
)
HEADING_WARN_TOO_MANY_FIXTURE = {
    'rows': [
        {
            'key': 'ABC-42',
            'summary': 'Some issue to show off the headings',
        },
        {
            'key': 'ABC-1001',
            'summary': 'Some additional issue to show off the headings warning',
        },
    ]
}
HEADING_WARN_TOO_MANY_FIXTURE_COUNT = len(HEADING_WARN_TOO_MANY_FIXTURE['rows'])
HEADING_WARN_TOO_FEW_FIXTURE = {'rows': []}

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
    f' [{row["key"]}]({URL_FIXTURE}/browse/{row["key"]})' f' - {row["summary"]}' for row in UO_LIST_FIXTURE['rows']
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
    f'[{row["key"]}]({URL_FIXTURE}/browse/{row["key"]})\n' f':{row["summary"]}\n' for row in D_LIST_FIXTURE['rows']
)

TABLE_FIXTURE = {
    'rows': [
        {
            'key': 'ABC-42',
            'summary': 'First issue to show off the tables',
        },
        {
            'key': 'ABC-1001',
            'summary': 'Second issue to show off the tables',
        },
    ]
}
TABLE_FIXTURE_PAYLOADS = (
    '| key                                                                  | summary                             |',
    '|:---------------------------------------------------------------------|:------------------------------------|',
    '| [ABC-42](https://remote-jira-instance.example.com/browse/ABC-42)     | First issue to show off the tables  |',
    '| [ABC-1001](https://remote-jira-instance.example.com/browse/ABC-1001) | Second issue to show off the tables |',
    '',
    '2 issues',
)


@pytest.mark.parametrize('level', [lv for lv in range(1, 6 + 1)])
def test_embed_headings(level, capsys):
    impl.BASE_URL = URL_FIXTURE
    hx = [None, emb.h1, emb.h2, emb.h3, emb.h4, emb.h5, emb.h6]
    token = '#' * level
    assert hx[level](query_text='', data=HEADING_FIXTURE) is None
    out, err = capsys.readouterr()
    assert not err
    assert out.strip() == f'{token}{HEADING_PAYLOAD_POSTFIX}'.strip()


@pytest.mark.parametrize('kind,marker', [('ol', '1.'), ('ul', '-')])
def test_embed_uo_lists(kind, marker, capsys):
    impl.BASE_URL = URL_FIXTURE
    lx = {'ol': emb.ol, 'ul': emb.ul}
    expected = '\n'.join(f'{marker}{UO_LIST_PAYLOAD_POSTFIXES[slot]}' for slot in (0, 1))
    assert lx[kind](query_text='', data=UO_LIST_FIXTURE) is None
    out, err = capsys.readouterr()
    assert not err
    assert out.strip() == expected


def test_embed_d_list(capsys):
    impl.BASE_URL = URL_FIXTURE
    expected = '\n'.join(D_LIST_PAYLOADS) + '\n' + '\n'
    assert emb.dl(query_text='', data=D_LIST_FIXTURE) is None
    out, err = capsys.readouterr()
    assert not err
    assert out == expected


@pytest.mark.parametrize('level', [lv for lv in range(1, 6 + 1)])
def test_embed_headings_too_few(level, capsys):
    impl.BASE_URL = URL_FIXTURE
    hx = [None, emb.h1, emb.h2, emb.h3, emb.h4, emb.h5, emb.h6]
    query_text = ''
    assert hx[level](query_text=query_text, data=HEADING_WARN_TOO_FEW_FIXTURE) is None
    out, err = capsys.readouterr()
    assert f'WARNING: received 0 results instead of 1 for JQL ({query_text}) and h{level}' in err
    assert not out.strip()


@pytest.mark.parametrize('level', [lv for lv in range(1, 6 + 1)])
def test_embed_headings_too_many(level, capsys):
    impl.BASE_URL = URL_FIXTURE
    hx = [None, emb.h1, emb.h2, emb.h3, emb.h4, emb.h5, emb.h6]
    query_text = ''
    mis_count = HEADING_WARN_TOO_MANY_FIXTURE_COUNT
    assert hx[level](query_text=query_text, data=HEADING_WARN_TOO_MANY_FIXTURE) is None
    out, err = capsys.readouterr()
    assert f'WARNING: received {mis_count} results instead of 1 for JQL ({query_text}) and h{level}' in err
    assert out


def test_embed_table(capsys):
    impl.BASE_URL = URL_FIXTURE
    expected = '\n'.join(TABLE_FIXTURE_PAYLOADS)
    assert emb.table(query_text='', data=TABLE_FIXTURE) is None
    out, err = capsys.readouterr()
    assert not err
    assert out.strip() == expected


def test_embed_table_no_result(capsys):
    impl.BASE_URL = URL_FIXTURE
    query_text = ''
    expected = f'WARNING: received 0 results for JQL ({query_text}) and table'
    assert emb.table(query_text='', data=HEADING_WARN_TOO_FEW_FIXTURE) is None
    out, err = capsys.readouterr()
    assert not err
    assert out.strip() == expected
