import laskea.transform as tr


def test_init_class():
    c_filter = tr.FilterMap('c', {})
    assert c_filter.order == tr.FilterMap.ORDER


def test_apply_empty():
    c_filter = tr.FilterMap('c', {})
    assert c_filter.apply('') == ''


def test_apply_spaces_only():
    c_filter = tr.FilterMap('c', {})
    assert c_filter.apply(' ') == ''


def test_apply_no_filters():
    c_filter = tr.FilterMap('c', {})
    assert c_filter.apply('foo') == 'foo'


def test_apply_drop_that():
    c_filter = tr.FilterMap('c', {'drop': [['equals', 'that']]})
    assert c_filter.apply('that') == ''


def test_op_equals_hits():
    assert tr.op_equals('entry', 'entry')


def test_op_equals_misses():
    assert not tr.op_equals('entry', 'different')
