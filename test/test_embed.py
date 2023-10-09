import pathlib

import pytest

import laskea
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

MBOM_FIXTURE_PATH = pathlib.Path('test', 'fixtures', 'basic', 'mbom.xlsx')
MBOM_TABLE = f"""\
<!-- anchor: ('0', '1233333', 'asdasd', '')-->
| Level | P/N | Item Name | SW Version |
|:------|:----|:----------|:-----------|
| 1     | 124 | a a       | 1          |
| 2     | 123 | b b       | 2          |
<!-- source: {MBOM_FIXTURE_PATH}-->
<!-- s-hash: sha512:98f49a212325387c2a800c000f6892879a38cae9fde357cca3de57bfcc18bb28\
5d34ad81f19fae1df735ec85e8ada40e7f4ae06ffb5bfb4f89bc7592c8d63111-->"""


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
def test_embed_headings_too_few_strict(level, capsys):
    impl.BASE_URL = URL_FIXTURE
    strictness = laskea.STRICT
    laskea.STRICT = True
    hx = [None, emb.h1, emb.h2, emb.h3, emb.h4, emb.h5, emb.h6]
    query_text = ''
    assert hx[level](query_text=query_text, data=HEADING_WARN_TOO_FEW_FIXTURE) is None
    out, err = capsys.readouterr()
    assert f'WARNING: received 0 results instead of 1 for JQL ({query_text}) and h{level}' in err
    assert f'WARNING: received 0 results instead of 1 for JQL () and h{level}\n' in out
    laskea.STRICT = strictness


@pytest.mark.parametrize('level', [lv for lv in range(1, 6 + 1)])
def test_embed_headings_too_many_strict(level, capsys):
    impl.BASE_URL = URL_FIXTURE
    strictness = laskea.STRICT
    laskea.STRICT = True
    hx = [None, emb.h1, emb.h2, emb.h3, emb.h4, emb.h5, emb.h6]
    query_text = ''
    mis_count = HEADING_WARN_TOO_MANY_FIXTURE_COUNT
    assert hx[level](query_text=query_text, data=HEADING_WARN_TOO_MANY_FIXTURE) is None
    out, err = capsys.readouterr()
    assert f'WARNING: received {mis_count} results instead of 1 for JQL ({query_text}) and h{level}' in err
    assert out
    laskea.STRICT = strictness


def test_embed_table(capsys):
    impl.BASE_URL = URL_FIXTURE
    expected = '\n'.join(TABLE_FIXTURE_PAYLOADS)
    assert emb.table(query_text='', show_summary=True, data=TABLE_FIXTURE) is None
    out, err = capsys.readouterr()
    assert not err
    assert out.strip() == expected


def test_embed_svl(capsys):
    expected = 'key|summary\nABC-42|First issue to show off the tables\nABC-1001|Second issue to show off the tables'
    assert emb.svl(query_text='', data=TABLE_FIXTURE) is None
    out, err = capsys.readouterr()
    assert not err
    assert out.strip() == expected


def test_embed_svl_field_sep_substitute(capsys):
    expected = 'keyusummary\nABC-42uFirst issue to show off the tables\nABC-1001uSecond issue to show off the tables'
    assert emb.svl(query_text='', field_sep='u', replacement='u', data=TABLE_FIXTURE) is None
    out, err = capsys.readouterr()
    assert not err
    assert out.strip() == expected


def test_embed_table_no_result_strict(capsys):
    impl.BASE_URL = URL_FIXTURE
    strictness = laskea.STRICT
    laskea.STRICT = True
    query_text = ''
    expected = f'WARNING: received 0 results for JQL ({query_text}) and table'
    assert emb.table(query_text=query_text, data=HEADING_WARN_TOO_FEW_FIXTURE) is None
    out, err = capsys.readouterr()
    assert 'WARNING: received 0 results for JQL () and table\n' in err
    assert out.strip() == expected
    laskea.STRICT = strictness


def test_embed_table_no_result_non_strict(capsys):
    impl.BASE_URL = URL_FIXTURE
    strictness = laskea.STRICT
    laskea.STRICT = False
    query_text = ''
    expected = ''
    assert emb.table(query_text=query_text, data=HEADING_WARN_TOO_FEW_FIXTURE) is None
    out, err = capsys.readouterr()
    assert not err
    assert out.strip() == expected
    laskea.STRICT = strictness


@pytest.mark.parametrize('level', [lv for lv in range(1, 6 + 1)])
def test_embed_headings_too_few_non_strict(level, capsys):
    impl.BASE_URL = URL_FIXTURE
    strictness = laskea.STRICT
    laskea.STRICT = False
    hx = [None, emb.h1, emb.h2, emb.h3, emb.h4, emb.h5, emb.h6]
    query_text = ''
    assert hx[level](query_text=query_text, data=HEADING_WARN_TOO_FEW_FIXTURE) is None
    out, err = capsys.readouterr()
    assert not err
    assert not out.strip()
    laskea.STRICT = strictness


@pytest.mark.parametrize('level', [lv for lv in range(1, 6 + 1)])
def test_embed_headings_too_many_non_strict(level, capsys):
    impl.BASE_URL = URL_FIXTURE
    strictness = laskea.STRICT
    laskea.STRICT = False
    hx = [None, emb.h1, emb.h2, emb.h3, emb.h4, emb.h5, emb.h6]
    query_text = ''
    assert hx[level](query_text=query_text, data=HEADING_WARN_TOO_MANY_FIXTURE) is None
    out, err = capsys.readouterr()
    assert not err
    assert not out.strip()
    laskea.STRICT = strictness


def test_embed_mbom_table_basic(capsys):
    assert emb.mbom_table(str(MBOM_FIXTURE_PATH)) is None
    out, err = capsys.readouterr()
    assert not err
    assert MBOM_TABLE in out
