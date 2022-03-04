# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-docstring,reimported,unused-import,unused-variable
import laskea.laskea as fill


def test_fill_init():
    assert fill.init() is None


def test_verify_request_wrong_number_of_args():
    assert fill.verify_request([]) == (2, 'received wrong number of arguments', [''])


def test_verify_request_bogus_command():
    assert fill.verify_request(['foo', 'bar', 'baz']) == (2, 'received unknown command', [''])


def test_verify_request_bogus_inp():
    assert fill.verify_request(['update', 'not-present', 'baz']) == (1, 'source is no file', [''])


def test_verify_request_no_config():
    assert fill.verify_request(['update', 'README.md', '']) == (2, 'configuration missing', [''])


def test_verify_request_config_as_folder():
    assert fill.verify_request(['update', 'README.md', 'laskea']) == (1, 'config (laskea) is no file', [''])


def test_verify_request_config_no_json_extension():
    assert fill.verify_request(['update', 'README.md', 'README.md']) == (1, 'config has no .json extension', [''])
