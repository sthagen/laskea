# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-docstring,reimported,unused-import,unused-variable
import json

import laskea.api.jqlLexer  # noqa
import laskea.api.jqlListener  # noqa
import laskea.api.jqlParser  # noqa
import laskea.api.jqlVisitor  # noqa
import laskea.cli as cli


def test_foo():
    assert isinstance(laskea.api.jqlLexer.jqlLexer(), laskea.api.jqlLexer.jqlLexer)


def test_bar():
    assert isinstance(laskea.api.jqlListener.jqlListener(), laskea.api.jqlListener.jqlListener)


def test_baz():
    token_stream = laskea.api.jqlParser.TokenStream()
    assert isinstance(laskea.api.jqlParser.jqlParser(token_stream), laskea.api.jqlParser.jqlParser)


def test_quux():
    assert isinstance(laskea.api.jqlVisitor.jqlVisitor(), laskea.api.jqlVisitor.jqlVisitor)


def test_report_context(capsys):
    quiet_flag_restore = cli.QUIET
    cli.QUIET = False
    assert cli.report_context(command='-', transaction_mode='+', vector=['42']) is None
    out, err = capsys.readouterr()
    assert not out
    lines = err.strip().split('\n')
    assert len(lines) == 17
    assert lines[:3] == ['Command: (-)', '- Transaction mode: (+)', 'Environment(variable values):']
    assert lines[9] == 'Effective(variable values):'
    for line in lines[3:9]:
        assert line.startswith(f'- {cli.APP_ENV}_')
    assert lines[-1] == "- CallVector: (['42'])"
    cli.QUIET = quiet_flag_restore


def test_report_context_quiet(capsys):
    quiet_flag_restore = cli.QUIET
    cli.QUIET = True
    assert cli.report_context(command='-', transaction_mode='+', vector=['42']) is None
    out, err = capsys.readouterr()
    assert not out
    assert not err
    cli.QUIET = quiet_flag_restore


def test_report_sources_of_effective_configuration(capsys):
    quiet_flag_restore = cli.QUIET
    cli.QUIET = False
    assert cli.report_sources_of_effective_configuration(source_of={}, header='42') is None
    out, err = capsys.readouterr()
    assert not err
    lines = out.strip().split('\n')
    assert lines == ['42', '# --- BEGIN ---', '{}', '# --- E N D ---']
    cli.QUIET = quiet_flag_restore


def test_report_sources_of_effective_configuration_quiet(capsys):
    quiet_flag_restore = cli.QUIET
    cli.QUIET = True
    assert cli.report_sources_of_effective_configuration(source_of={}, header='42') is None
    out, err = capsys.readouterr()
    assert not out
    assert not err
    cli.QUIET = quiet_flag_restore


def test_safe_report_configuration(capsys):
    quiet_flag_restore = cli.QUIET
    cli.QUIET = False
    assert cli.safe_report_configuration(configuration={}, header='42') is None
    out, err = capsys.readouterr()
    assert not err
    lines = out.strip().split('\n')
    assert lines == ['42', '# --- BEGIN ---', '{}', '# --- E N D ---']
    cli.QUIET = quiet_flag_restore


def test_safe_report_configuration_quiet(capsys):
    quiet_flag_restore = cli.QUIET
    cli.QUIET = True
    assert cli.safe_report_configuration(configuration={}, header='42') is None
    out, err = capsys.readouterr()
    assert not out
    assert not err
    cli.QUIET = quiet_flag_restore


def test_safe_report_configuration_no_leak(capsys):
    quiet_flag_restore = cli.QUIET
    cli.QUIET = False
    thing = {'remote': {'token': 'leak'}}
    gnith = {'remote': {'token': '*************'}}
    assert cli.safe_report_configuration(configuration=thing, header='42') is None
    out, err = capsys.readouterr()
    assert not err
    lines = out.strip().split('\n')
    assert lines == ['42', '# --- BEGIN ---'] + json.dumps(gnith, indent=2).split('\n') + ['# --- E N D ---']
    cli.QUIET = quiet_flag_restore


def test_create_and_report_effective_configuration(capsys):
    quiet_flag_restore = cli.QUIET
    cli.QUIET = False
    assert cli.create_and_report_effective_configuration(header='42') is None
    out, err = capsys.readouterr()
    assert not err
    lines = out.strip().split('\n')
    assert len(lines) == 55
    assert lines[:2] == ['42', '# --- BEGIN ---']
    assert lines[-1] == '# --- E N D ---'
    cli.QUIET = quiet_flag_restore


def test_create_and_report_effective_configuration_quiet(capsys):
    quiet_flag_restore = cli.QUIET
    cli.QUIET = True
    assert cli.create_and_report_effective_configuration(header='42') is None
    out, err = capsys.readouterr()
    assert not out
    assert not err
    cli.QUIET = quiet_flag_restore


def test_load_configuration_empty(capsys):
    quiet_flag_restore = cli.DEBUG
    base_markers_restore = cli.BASE_MARKERS
    cli.DEBUG = False
    assert cli.load_configuration(configuration={}) == {}
    out, err = capsys.readouterr()
    assert not err
    assert out.strip() == 'Warning: Requested load from empty configuration'
    cli.DEBUG = quiet_flag_restore
    cli.BASE_MARKERS = base_markers_restore


def test_load_configuration_remote_token(capsys):
    quiet_flag_restore = cli.DEBUG
    base_markers_restore = cli.BASE_MARKERS
    cli.DEBUG = False
    thing = {'remote': {'token': 'leak'}}
    gnith = {'remote_token': 'config'}
    assert cli.load_configuration(configuration=thing) == gnith
    out, err = capsys.readouterr()
    assert not out
    assert not err
    cli.DEBUG = quiet_flag_restore
    cli.BASE_MARKERS = base_markers_restore
