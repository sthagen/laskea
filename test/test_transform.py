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
