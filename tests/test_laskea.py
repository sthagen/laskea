import pytest

import laskea.laskea as fill


def test_process_wrong_command(capsys):
    err_msg = 'Usage: laskea update [--help] [-v] [-c config-path] [-n] [-i] source-files*md [other.md]'
    with pytest.raises(SystemExit):
        fill.process('wrong', 'ignore', ('ignore',), {})
    out, err = capsys.readouterr()
    assert not err
    assert err_msg in out


def test_process_empty_paths(capsys):
    err_msg = 'Usage: laskea update [--help] [-v] [-c config-path] [-n] [-i] source-files*md [other.md]'
    with pytest.raises(SystemExit):
        fill.process('update', 'ignore', tuple(), {})
    out, err = capsys.readouterr()
    assert not err
    assert err_msg in out
