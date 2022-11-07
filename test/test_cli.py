import re

import pytest

import laskea
import laskea.cli as cli


def test_report_command(capsys):
    with pytest.raises(SystemExit):
        cli.report()
    out, err = capsys.readouterr()
    assert f'laskea : {laskea.__version__}' in out
    assert not err


def test_template_command(capsys):
    with pytest.raises(SystemExit):
        cli.app_template()
    out, err = capsys.readouterr()
    assert '"markers": "[[[fill ]]] [[[end]]]"' in out
    assert not err


def test_update_command(capsys):
    with pytest.raises(TypeError):
        cli.update(source=['not-present'])
    out, err = capsys.readouterr()
    assert not out
    assert not err


def test_csv_command(capsys):
    with pytest.raises(SystemExit):
        cli.svl_cmd(jql_query='')  # type: ignore
    out, err = capsys.readouterr()
    assert not out
    assert 'JQL query required.' in err


def test_version_command(capsys):
    with pytest.raises(Exception):
        cli.callback(version=True)
    out, err = capsys.readouterr()
    assert 'Calculate (Finnish: laskea) some parts' in out
    assert f'version {laskea.__version__}' in out
    assert not err
    with pytest.raises(Exception):
        cli.callback()
    out, err = capsys.readouterr()
    assert 'Calculate (Finnish: laskea) some parts' in out
    assert f'version {laskea.__version__}' in out
    assert not err
