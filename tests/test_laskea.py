# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-docstring,reimported,unused-import,unused-variable
import laskea.laskea as fill
from tests import conftest


def test_fill_init():
    assert fill.init() is None
