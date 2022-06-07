import json
import pathlib

import pytest

import laskea.api.jira as impl

URL_FIXTURE = ''
HEADING_FIXTURE = {
    'rows': [
        {
            'key': 'ABC-42',
            'summary': 'Some issue to show off the headings',
        }
    ]
}
HEADING_PAYLOAD_POSTFIX = (
    f' [{HEADING_FIXTURE["rows"][0]["key"]}]({URL_FIXTURE}/browse/{HEADING_FIXTURE["rows"][0]["key"]})'
    f' - {HEADING_FIXTURE["rows"][0]["summary"]}'
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
    f' [{row["key"]}]({URL_FIXTURE}/browse/{row["key"]}) - {row["summary"]}' for row in UO_LIST_FIXTURE['rows']
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
    f'[{row["key"]}]({URL_FIXTURE}/browse/{row["key"]})\n:{row["summary"]}\n' for row in D_LIST_FIXTURE['rows']
)

P_C_L_FIXTURE_PATH = pathlib.Path('tests', 'fixtures', 'basic', 'p_c_jira.json')


@pytest.mark.parametrize('level', [lv for lv in range(1, 6 + 1)])
def test_impl_headings(level):
    impl.BASE_URL = URL_FIXTURE
    hd = impl.markdown_heading(impl.Jira(''), jql_text='', column_fields=tuple(), level=level, data=HEADING_FIXTURE)
    token = '#' * level
    assert hd == f'{token}{HEADING_PAYLOAD_POSTFIX}'


@pytest.mark.parametrize('kind,marker', [('ol', '1.'), ('ul', '-')])
def test_impl_uo_lists(kind, marker):
    impl.BASE_URL = URL_FIXTURE
    text = impl.markdown_list(impl.Jira(''), jql_text='', column_fields=tuple(), list_type=kind, data=UO_LIST_FIXTURE)
    items = text.strip().split('\n')
    for slot in (0, 1):
        assert items[slot] == f'{marker}{UO_LIST_PAYLOAD_POSTFIXES[slot]}'


def test_impl_d_list():
    impl.BASE_URL = URL_FIXTURE
    text = impl.markdown_list(impl.Jira(''), jql_text='', column_fields=tuple(), list_type='dl', data=D_LIST_FIXTURE)
    assert text == '\n'.join(D_LIST_PAYLOADS) + '\n'


def test_impl_login_no_user():
    impl.BASE_USER = ''
    message = 'User, Token, and URL are all required for login.'
    with pytest.raises(ValueError, match=message):
        _ = impl.login(url='does-not-help-as-user-is-missing')


def test_impl_login_no_token():
    impl.BASE_TOKEN = ''
    message = 'User, Token, and URL are all required for login.'
    with pytest.raises(ValueError, match=message):
        _ = impl.login(user='not-relevant-as-token-is-missing')


def test_impl_login_no_url():
    impl.BASE_URL = ''
    message = 'User, Token, and URL are all required for login.'
    with pytest.raises(ValueError, match=message):
        _ = impl.login(user='not-relevant', token='as-url-is-missing')


def test_impl_login_no_url_server():
    impl.BASE_URL = ''
    message = 'User, Token, and URL are all required for login.'
    with pytest.raises(ValueError, match=message):
        _ = impl.login(user='not-relevant', token='as-url-is-missing', is_cloud=False)


@pytest.mark.parametrize('is_cloud', [True, False])
def test_impl_login_trying_but_bad_non_url(is_cloud, capsys):
    impl.BASE_URL = ''
    impl.BASE_IS_CLOUD = is_cloud
    _ = impl.login(user='not-relevant', token='as-url-is-leading-nowhere', url='/dev/null', is_cloud=is_cloud)
    out, err = capsys.readouterr()
    assert not err
    assert not out


def test_impl_query():
    impl.BASE_COL_FIELDS = ('key', 'summary')
    result = impl.query(impl.Jira(''), jql_text='', column_fields=tuple())
    assert result == {'jql_text': '', 'error': 'Empty JIRA Query Language text detected'}


def test_parent_children_sections():
    with open(P_C_L_FIXTURE_PATH, 'rt', encoding='utf-8') as handle:
        data = json.load(handle)

    doc = impl.parent_children_sections(impl.Jira(''), 'parent_jql', 'children_jql', 'Test Plan', 'Test Case', data)
    assert '## First summary' in doc
