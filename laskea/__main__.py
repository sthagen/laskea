# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned,line-too-long,missing-module-docstring
import sys

from laskea.cli import app

if __name__ == '__main__':
    sys.exit(app(prog_name='laskea'))  # pragma: no cover
