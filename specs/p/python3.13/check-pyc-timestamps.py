"""Checks if all *.pyc files have later mtime than their *.py files."""

import os
import sys
from importlib.util import cache_from_source
from pathlib import Path


RPM_BUILD_ROOT = os.environ.get('RPM_BUILD_ROOT', '')

# ...cpython-3X.pyc
# ...cpython-3X.opt-1.pyc
# ...cpython-3X.opt-2.pyc
LEVELS = (None, 1, 2)

# list of globs of test and other files that we expect not to have bytecode
not_compiled = [
    '/usr/bin/*',
    '*/test/*/bad_coding.py',
    '*/test/*/bad_coding2.py',
    '*/test/*/badsyntax_*.py',
    '*/test_future_stmt/badsyntax_*.py',
    '*.debug-gdb.py',
]


def bytecode_expected(path):
    path = Path(path[len(RPM_BUILD_ROOT):])
    for glob in not_compiled:
        if path.match(glob):
            return False
    return True


failed = 0
compiled = (path for path in sys.argv[1:] if bytecode_expected(path))
for path in compiled:
    to_check = (cache_from_source(path, optimization=opt) for opt in LEVELS)
    f_mtime = os.path.getmtime(path)
    for pyc in to_check:
        c_mtime = os.path.getmtime(pyc)
        if c_mtime < f_mtime:
            print('Failed bytecompilation timestamps check: '
                  f'Bytecode file {pyc} is older than source file {path}',
                  file=sys.stderr)
            failed += 1

if failed:
    print(f'\n{failed} files failed bytecompilation timestamps check.',
          file=sys.stderr)
    sys.exit(1)
