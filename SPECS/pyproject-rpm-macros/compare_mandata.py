'''Check whether the manpage extensions and directories list hardcoded in brp-compress
are the same as the lists stored in pyproject_save_files.py.
There is an open issue for RPM to provide them both as macros:
https://github.com/rpm-software-management/rpm/issues/1865
Once that happens, this script can be removed.
'''

import argparse
import re
import sys

from pathlib import PosixPath

from pyproject_buildrequires import print_err
from pyproject_save_files import prepend_mandirs, MANPAGE_EXTENSIONS



def read_brp_compress(filename):

    contents = filename.read_text()
    # To avoid duplicity of the manpage extensions which are listed a few times
    # in the source file, they are stored in set and then retyped to a sorted list
    manpage_exts = sorted(
        set(re.findall(r'\(?(\w+)\\+\)?\$?', contents))
    )

    # Get rid of ${PREFIX} when extracting the manpage directories
    mandirs = [
        entry.replace('.${PREFIX}', '/PREFIX')
        for entry in contents.split()
        if entry.startswith('.${PREFIX}')
    ]

    return manpage_exts, sorted(mandirs)


def compare_mandirs(brp_compress_mandirs):
    '''
    Check whether each of brp-compress mandirs entry is present in the list
    stored in pyproject_save_files.py
    '''

    pyp_save_files_mandirs = sorted(prepend_mandirs(prefix='/PREFIX'))
    if brp_compress_mandirs == pyp_save_files_mandirs:
        return True
    else:
        print_err('Mandir lists don\'t match, update the list in pyproject_save_files.py')
        print_err('brp-compress list:', brp_compress_mandirs)
        print_err('pyproject_save_files list:', pyp_save_files_mandirs)
        return False


def compare_manpage_extensions(brp_compress_manpage_exts):
    '''
    Check whether each of brp-compress manpage extension is present in the list
    stored in pyproject_save_files.py
    '''

    if brp_compress_manpage_exts == sorted(MANPAGE_EXTENSIONS):
        return True
    else:
        print_err('Manpage extension lists don\'t match, update the list in pyproject_save_files.py')
        print_err('brp-compress list:', brp_compress_manpage_exts)
        print_err('pyproject_save_files list:', sorted(MANPAGE_EXTENSIONS))
        return False


def main(args):
    src_manpage_exts, src_mandirs = read_brp_compress(args.filename)
    extension_check_successful = compare_manpage_extensions(src_manpage_exts)
    mandir_check_successful = compare_mandirs(src_mandirs)
    if extension_check_successful and mandir_check_successful:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=PosixPath, required=True,
                        help='Provide location of brp-compress file')
    main(parser.parse_args())
