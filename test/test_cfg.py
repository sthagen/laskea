import json
import pathlib

import pytest

import laskea
import laskea.config as cfg


def test_generate_template_command():
    json_string = cfg.generate_template()
    assert '"markers": "[[[fill ]]] [[[end]]]"' in json_string


def test_process_spoc_no_file(capsys):
    with pytest.raises(SystemExit):
        cfg.process('no-file', {})
    out, err = capsys.readouterr()
    assert 'Given configuration path is no file or empty' in err
    assert not out


def test_process_spoc_template_file(capsys):
    fixture_config = pathlib.Path('test', 'fixtures', 'basic', 'dot.laskea.json')
    assert cfg.process(str(fixture_config), {'quiet': laskea.QUIET, 'verbose': True}) is None
    out, err = capsys.readouterr()
    assert 'Configuration interface combined file, environment, and commandline values!' in err
    assert not out


def test_report_context(capsys):
    quiet_flag_restore = laskea.QUIET
    laskea.QUIET = False
    assert cfg.report_context(command='-', transaction_mode='+', vector=['42']) is None
    out, err = capsys.readouterr()
    assert not out
    lines = err.strip().split('\n')
    assert len(lines) == 21
    assert lines[:3] == ['Command: (-)', '- Transaction mode: (+)', 'Environment(variable values):']
    assert lines[11] == 'Effective(variable values):'
    for line in lines[3:11]:
        assert line.startswith(f'- {laskea.APP_ENV}_')
    assert lines[-1] == "- CallVector: (['42'])"
    laskea.QUIET = quiet_flag_restore


def test_report_context_quiet(capsys):
    quiet_flag_restore = laskea.QUIET
    laskea.QUIET = True
    assert cfg.report_context(command='-', transaction_mode='+', vector=['42']) is None
    out, err = capsys.readouterr()
    assert not out
    assert not err
    laskea.QUIET = quiet_flag_restore


def test_report_sources_of_effective_configuration(capsys):
    quiet_flag_restore = laskea.QUIET
    laskea.QUIET = False
    assert cfg.report_sources_of_effective_configuration(source_of={}, header='42') is None
    out, err = capsys.readouterr()
    assert not out
    lines = err.strip().split('\n')
    assert lines == ['42', '# --- BEGIN ---', '{}', '# --- E N D ---']
    laskea.QUIET = quiet_flag_restore


def test_report_sources_of_effective_configuration_quiet(capsys):
    quiet_flag_restore = laskea.QUIET
    laskea.QUIET = True
    assert cfg.report_sources_of_effective_configuration(source_of={}, header='42') is None
    out, err = capsys.readouterr()
    assert not out
    assert not err
    laskea.QUIET = quiet_flag_restore


def test_safe_report_configuration(capsys):
    quiet_flag_restore = laskea.QUIET
    laskea.QUIET = False
    assert cfg.safe_report_configuration(configuration={}, header='42') is None
    out, err = capsys.readouterr()
    assert not out
    lines = err.strip().split('\n')
    assert lines == ['42', '# --- BEGIN ---', '{}', '# --- E N D ---']
    laskea.QUIET = quiet_flag_restore


def test_safe_report_configuration_quiet(capsys):
    quiet_flag_restore = laskea.QUIET
    laskea.QUIET = True
    assert cfg.safe_report_configuration(configuration={}, header='42') is None
    out, err = capsys.readouterr()
    assert not out
    assert not err
    laskea.QUIET = quiet_flag_restore


def test_safe_report_configuration_no_leak(capsys):
    quiet_flag_restore = laskea.QUIET
    laskea.QUIET = False
    thing = {'remote': {'token': 'leak'}}
    gnith = {'remote': {'token': '*************'}}
    assert cfg.safe_report_configuration(configuration=thing, header='42') is None
    out, err = capsys.readouterr()
    assert not out
    lines = err.strip().split('\n')
    assert lines == ['42', '# --- BEGIN ---'] + json.dumps(gnith, indent=2).split('\n') + ['# --- E N D ---']
    laskea.QUIET = quiet_flag_restore


def test_create_and_report_effective_configuration(capsys):
    quiet_flag_restore = laskea.QUIET
    laskea.QUIET = False
    assert cfg.create_and_report_effective_configuration(header='42') is None
    out, err = capsys.readouterr()
    assert not out
    lines = err.strip().split('\n')
    assert len(lines) == 47
    assert lines[:2] == ['42', '# --- BEGIN ---']
    assert lines[-1] == '# --- E N D ---'
    print(lines)
    laskea.QUIET = quiet_flag_restore


def test_create_and_report_effective_configuration_quiet(capsys):
    quiet_flag_restore = laskea.QUIET
    laskea.QUIET = True
    assert cfg.create_and_report_effective_configuration(header='42') is None
    out, err = capsys.readouterr()
    assert not out
    assert not err
    laskea.QUIET = quiet_flag_restore


def test_load_configuration_empty(capsys):
    quiet_flag_restore = laskea.DEBUG
    base_markers_restore = laskea.BASE_MARKERS
    laskea.DEBUG = False
    assert cfg.load_configuration(configuration={}) == {}
    out, err = capsys.readouterr()
    assert not out
    assert err.strip() == 'Warning: Requested load from empty configuration'
    laskea.DEBUG = quiet_flag_restore
    laskea.BASE_MARKERS = base_markers_restore


def test_load_configuration_remote_token(capsys):
    quiet_flag_restore = laskea.DEBUG
    base_markers_restore = laskea.BASE_MARKERS
    laskea.DEBUG = False
    thing = {'remote': {'token': 'leak'}}
    gnith = {'is_cloud': 'env', 'remote_base_url': 'env', 'remote_token': 'env', 'remote_user': 'env'}
    assert cfg.load_configuration(configuration=thing) == gnith
    out, err = capsys.readouterr()
    assert not out
    assert not err
    laskea.DEBUG = quiet_flag_restore
    laskea.BASE_MARKERS = base_markers_restore
