#!/usr/bin/env python
from __future__ import absolute_import, print_function, unicode_literals

import os
import sys

import nose


def start(argv=None):
    sys.exitfunc = lambda: sys.stderr.write("Shutting down...\n")

    if argv is None:
        argv = [
            "nosetests", "--cover-branches", "--with-coverage",
            "--cover-erase", "--verbose",
            "--cover-package=django_logical_perms",
        ]

    tests_module = os.path.abspath(os.path.dirname(__file__))
    nose.run_exit(argv=argv, defaultTest=tests_module)


if __name__ == "__main__":
    start(sys.argv)
