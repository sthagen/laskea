import pytest

import laskea
import laskea.api.jira as impl
import laskea.api.jqlLexer  # noqa
import laskea.api.jqlListener  # noqa
import laskea.api.jqlParser  # noqa
import laskea.api.jqlVisitor  # noqa

HEADING_FIXTURE = {
    'rows': [
        {
            'key': 'ABC-42',
            'summary': 'Some issue to show off the headings',
        }
    ]
}
HEADING_PAYLOAD_POSTFIX = (
    f' [{HEADING_FIXTURE["rows"][0]["key"]}](/browse/{HEADING_FIXTURE["rows"][0]["key"]})'
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
    f' [{row["key"]}](/browse/{row["key"]}) - {row["summary"]}' for row in UO_LIST_FIXTURE['rows']
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
D_LIST_PAYLOADS = tuple(f'[{row["key"]}](/browse/{row["key"]})\n:{row["summary"]}\n' for row in D_LIST_FIXTURE['rows'])


def test_foo():
    assert isinstance(laskea.api.jqlLexer.jqlLexer(), laskea.api.jqlLexer.jqlLexer)


def test_bar():
    assert isinstance(laskea.api.jqlListener.jqlListener(), laskea.api.jqlListener.jqlListener)


def test_baz():
    token_stream = laskea.api.jqlParser.TokenStream()
    assert isinstance(laskea.api.jqlParser.jqlParser(token_stream), laskea.api.jqlParser.jqlParser)


def test_quux():
    assert isinstance(laskea.api.jqlVisitor.jqlVisitor(), laskea.api.jqlVisitor.jqlVisitor)


@pytest.mark.parametrize('level', [lv for lv in range(1, 7 - 1)])
def test_impl_headings(level):
    hd = impl.markdown_heading(impl.Jira(''), jql_text='', column_fields=tuple(), level=level, data=HEADING_FIXTURE)
    token = '#' * level
    assert hd == f'{token}{HEADING_PAYLOAD_POSTFIX}'


@pytest.mark.parametrize('kind,marker', [('ol', '1.'), ('ul', '-')])
def test_impl_uo_lists(kind, marker):
    text = impl.markdown_list(impl.Jira(''), jql_text='', column_fields=tuple(), list_type=kind, data=UO_LIST_FIXTURE)
    items = text.strip().split('\n')
    for slot in (0, 1):
        assert items[slot] == f'{marker}{UO_LIST_PAYLOAD_POSTFIXES[slot]}'


def test_impl_d_list():
    text = impl.markdown_list(impl.Jira(''), jql_text='', column_fields=tuple(), list_type='dl', data=D_LIST_FIXTURE)
    assert text == '\n'.join(D_LIST_PAYLOADS) + '\n'
