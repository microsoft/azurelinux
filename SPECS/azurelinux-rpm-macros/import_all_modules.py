'''Script to perform import of each module given to %%py_check_import
'''
import argparse
import importlib
import fnmatch
import os
import re
import site
import sys

from contextlib import contextmanager
from pathlib import Path


def read_modules_files(file_paths):
    '''Read module names from the files (modules must be newline separated).

    Return the module names list or, if no files were provided, an empty list.
    '''

    if not file_paths:
        return []

    modules = []
    for file in file_paths:
        file_contents = file.read_text()
        modules.extend(file_contents.split())
    return modules


def read_modules_from_cli(argv):
    '''Read module names from command-line arguments (space or comma separated).

    Return the module names list.
    '''

    if not argv:
        return []

    # %%py3_check_import allows to separate module list with comma or whitespace,
    # we need to unify the output to a list of particular elements
    modules_as_str = ' '.join(argv)
    modules = re.split(r'[\s,]+', modules_as_str)
    # Because of shell expansion in some less typical cases it may happen
    # that a trailing space will occur at the end of the list.
    # Remove the empty items from the list before passing it further
    modules = [m for m in modules if m]
    return modules


def filter_top_level_modules_only(modules):
    '''Filter out entries with nested modules (containing dot) ie. 'foo.bar'.

    Return the list of top-level modules.
    '''

    return [module for module in modules if '.' not in module]


def any_match(text, globs):
    '''Return True if any of given globs fnmatchcase's the given text.'''

    return any(fnmatch.fnmatchcase(text, g) for g in globs)


def exclude_unwanted_module_globs(globs, modules):
    '''Filter out entries which match the either of the globs given as argv.

    Return the list of filtered modules.
    '''

    return [m for m in modules if not any_match(m, globs)]


def read_modules_from_all_args(args):
    '''Return a joined list of modules from all given command-line arguments.
    '''

    modules = read_modules_files(args.filename)
    modules.extend(read_modules_from_cli(args.modules))
    if args.exclude:
        modules = exclude_unwanted_module_globs(args.exclude, modules)

    if args.top_level:
        modules = filter_top_level_modules_only(modules)

    # Error when someone accidentally managed to filter out everything
    if len(modules) == 0:
        raise ValueError('No modules to check were left')

    return modules


def import_modules(modules):
    '''Procedure to perform import check for each module name from the given list of modules.
    '''

    for module in modules:
        print('Check import:', module, file=sys.stderr)
        importlib.import_module(module)


def argparser():
    parser = argparse.ArgumentParser(
        description='Generate list of all importable modules for import check.'
    )
    parser.add_argument(
        'modules', nargs='*',
        help=('Add modules to check the import (space or comma separated).'),
    )
    parser.add_argument(
        '-f', '--filename', action='append', type=Path,
        help='Add importable module names list from file.',
    )
    parser.add_argument(
        '-t', '--top-level', action='store_true',
        help='Check only top-level modules.',
    )
    parser.add_argument(
        '-e', '--exclude', action='append',
        help='Provide modules globs to be excluded from the check.',
    )
    return parser


@contextmanager
def remove_unwanteds_from_sys_path():
    '''Remove cwd and this script's parent from sys.path for the import test.
    Bring the original contents back after import is done (or failed)
    '''

    cwd_absolute = Path.cwd().absolute()
    this_file_parent = Path(__file__).parent.absolute()
    old_sys_path = list(sys.path)
    for path in old_sys_path:
        if Path(path).absolute() in (cwd_absolute, this_file_parent):
            sys.path.remove(path)
    try:
        yield
    finally:
        sys.path = old_sys_path


def addsitedirs_from_environ():
    '''Load directories from the _PYTHONSITE environment variable (separated by :)
    and load the ones already present in sys.path via site.addsitedir()
    to handle .pth files in them.

    This is needed to properly import old-style namespace packages with nspkg.pth files.
    See https://bugzilla.redhat.com/2018551 for a more detailed rationale.'''
    for path in os.getenv('_PYTHONSITE', '').split(':'):
        if path in sys.path:
            site.addsitedir(path)


def main(argv=None):

    cli_args = argparser().parse_args(argv)

    if not cli_args.modules and not cli_args.filename:
        raise ValueError('No modules to check were provided')

    modules = read_modules_from_all_args(cli_args)

    with remove_unwanteds_from_sys_path():
        addsitedirs_from_environ()
        import_modules(modules)


if __name__ == '__main__':
    main()
