import laskea.transform as tr


def test_op_contains_hits():
    assert tr.op_contains('entry', 'nt')


def test_op_contains_misses():
    assert not tr.op_contains('entry', 'NT')


def test_op_endswith_hits():
    assert tr.op_endswith('entry', 'try')


def test_op_endswith_misses():
    assert not tr.op_endswith('entry', 'different')


def test_op_equals_hits():
    assert tr.op_equals('entry', 'entry')


def test_op_equals_misses():
    assert not tr.op_equals('entry', 'different')


def test_op_icontains_hits():
    assert tr.op_icontains('entry', 'NT')


def test_op_icontains_misses():
    assert not tr.op_icontains('entry', 'different')


def test_op_iendswith_hits():
    assert tr.op_iendswith('entry', 'TRY')


def test_op_iendswith_misses():
    assert not tr.op_iendswith('entry', 'different')


def test_op_iequals_hits():
    assert tr.op_iequals('entry', 'ENTRY')


def test_op_iequals_misses():
    assert not tr.op_iequals('entry', 'different')


def test_op_istartswith_hits():
    assert tr.op_istartswith('entry', 'EN')


def test_op_istartswith_misses():
    assert not tr.op_istartswith('entry', 'different')


def test_op_matches_hits():
    assert tr.op_matches('entry', 'e.*')


def test_op_matches_misses():
    assert not tr.op_matches('entry', 'd.*')


def test_op_startswith_hits():
    assert tr.op_startswith('entry', 'en')


def test_op_startswith_misses():
    assert not tr.op_startswith('entry', 'different')


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


def test_apply_drop_that_miss():
    c_filter = tr.FilterMap('c', {'drop': [['equals', 'that']]})
    assert c_filter.apply('else') == 'else'


def test_apply_keep_drop_that():
    c_filter = tr.FilterMap('c', {'keep': [['iequals', 'that']], 'drop': [['equals', 'THAT']]})
    assert c_filter.apply('THAT') == 'THAT'


def test_apply_replace_keep_drop_that():
    c_filter = tr.FilterMap(
        'c',
        {
            'order': ['replace', 'keep', 'drop'],
            'replace': [['THAT', 'that']],
            'keep': [['equals', 'THAT']],
            'drop': [['equals', 'that']],
        },
    )
    assert c_filter.apply('THAT') == ''


def test_apply_multiple_replace_keep_drop_that():
    c_filter = tr.FilterMap(
        'c',
        {
            'order': ['replace', 'keep', 'drop'],
            'replace': [['THAT', 'that'], ['that', 'SOMETHING_COMPLETELY_DIFFERENT']],
            'keep': [['equals', 'THAT']],
            'drop': [['equals', 'that']],
        },
    )
    assert c_filter.apply('THAT') == 'SOMETHING_COMPLETELY_DIFFERENT'
