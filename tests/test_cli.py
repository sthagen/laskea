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
