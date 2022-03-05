import laskea
import laskea.api.jqlLexer  # noqa
import laskea.api.jqlListener  # noqa
import laskea.api.jqlParser  # noqa
import laskea.api.jqlVisitor  # noqa


def test_foo():
    assert isinstance(laskea.api.jqlLexer.jqlLexer(), laskea.api.jqlLexer.jqlLexer)


def test_bar():
    assert isinstance(laskea.api.jqlListener.jqlListener(), laskea.api.jqlListener.jqlListener)


def test_baz():
    token_stream = laskea.api.jqlParser.TokenStream()
    assert isinstance(laskea.api.jqlParser.jqlParser(token_stream), laskea.api.jqlParser.jqlParser)


def test_quux():
    assert isinstance(laskea.api.jqlVisitor.jqlVisitor(), laskea.api.jqlVisitor.jqlVisitor)
