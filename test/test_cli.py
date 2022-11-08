from typer.testing import CliRunner

import laskea
from laskea.cli import app

runner = CliRunner()


def test_report_command():
    result = runner.invoke(app, ['report'])
    assert result.exit_code == 0
    assert f'laskea : {laskea.__version__}' in result.stdout


def test_template_command():
    result = runner.invoke(app, ['template'])
    assert result.exit_code == 0
    assert '"markers": "[[[fill ]]] [[[end]]]"' in result.stdout


def test_update_command():
    result = runner.invoke(app, ['update', 'not-present'])
    assert result.exit_code == 1
    assert 'Reading from discovered configuration path' in result.stdout
    assert 'Cogging not-present' in result.stdout


def test_csv_command():
    result = runner.invoke(app, ['csv', '--jql-query', ''])
    assert result.exit_code == 2
    assert 'JQL query required.' in result.stdout


def test_version_command():
    result = runner.invoke(app, ['version'])
    assert result.exit_code == 0
    assert 'Calculate (Finnish: laskea) some parts' in result.stdout
    assert f'version {laskea.__version__}' in result.stdout
