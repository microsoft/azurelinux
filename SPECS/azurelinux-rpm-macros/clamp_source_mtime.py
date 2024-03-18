"""Module/script to clamp the mtimes of all .py files to $SOURCE_DATE_EPOCH

When called as a script with arguments, this compiles the directories
given as arguments recursively.

If upstream is interested, this can be later integrated to the compileall module
as an additional option (e.g. --clamp-source-mtime).

License:
This has been derived from the Python's compileall module
and it follows Python licensing. For more info see: https://www.python.org/psf/license/
"""
from __future__ import print_function
import os
import sys

# Python 3.6 and higher
PY36 = sys.version_info[0:2] >= (3, 6)

__all__ = ["clamp_dir", "clamp_file"]


def _walk_dir(dir, maxlevels, quiet=0):
    if PY36 and quiet < 2 and isinstance(dir, os.PathLike):
        dir = os.fspath(dir)
    else:
        dir = str(dir)
    if not quiet:
        print('Listing {!r}...'.format(dir))
    try:
        names = os.listdir(dir)
    except OSError:
        if quiet < 2:
            print("Can't list {!r}".format(dir))
        names = []
    names.sort()
    for name in names:
        if name == '__pycache__':
            continue
        fullname = os.path.join(dir, name)
        if not os.path.isdir(fullname):
            yield fullname
        elif (maxlevels > 0 and name != os.curdir and name != os.pardir and
              os.path.isdir(fullname) and not os.path.islink(fullname)):
                for result in _walk_dir(fullname, maxlevels=maxlevels - 1,
                                        quiet=quiet):
                    yield result


def clamp_dir(dir, source_date_epoch, quiet=0):
    """Clamp the mtime of all modules in the given directory tree.

    Arguments:

    dir:       the directory to byte-compile
    source_date_epoch: integer parsed from $SOURCE_DATE_EPOCH
    quiet:     full output with False or 0, errors only with 1,
               no output with 2
    """
    maxlevels = sys.getrecursionlimit()
    files = _walk_dir(dir, quiet=quiet, maxlevels=maxlevels)
    success = True
    for file in files:
        if not clamp_file(file, source_date_epoch, quiet=quiet):
            success = False
    return success


def clamp_file(fullname, source_date_epoch, quiet=0):
    """Clamp the mtime of one file.

    Arguments:

    fullname:  the file to byte-compile
    source_date_epoch: integer parsed from $SOURCE_DATE_EPOCH
    quiet:     full output with False or 0, errors only with 1,
               no output with 2
    """
    if PY36 and quiet < 2 and isinstance(fullname, os.PathLike):
        fullname = os.fspath(fullname)
    else:
        fullname = str(fullname)
    name = os.path.basename(fullname)

    if os.path.isfile(fullname) and not os.path.islink(fullname):
        if name[-3:] == '.py':
            try:
                mtime = int(os.stat(fullname).st_mtime)
                atime = int(os.stat(fullname).st_atime)
            except OSError as e:
                if quiet >= 2:
                    return False
                elif quiet:
                    print('*** Error checking mtime of {!r}...'.format(fullname))
                else:
                    print('*** ', end='')
                print(e.__class__.__name__ + ':', e)
                return False
            if mtime > source_date_epoch:
                if not quiet:
                    print('Clamping mtime of {!r}'.format(fullname))
                try:
                    os.utime(fullname, (atime, source_date_epoch))
                except OSError as e:
                    if quiet >= 2:
                        return False
                    elif quiet:
                        print('*** Error clamping mtime of {!r}...'.format(fullname))
                    else:
                        print('*** ', end='')
                    print(e.__class__.__name__ + ':', e)
                    return False
    return True


def main():
    """Script main program."""
    import argparse

    source_date_epoch = os.getenv('SOURCE_DATE_EPOCH')
    if not source_date_epoch:
        print("Not clamping source mtimes, $SOURCE_DATE_EPOCH not set")
        return True  # This is a success, no action needed
    try:
        source_date_epoch = int(source_date_epoch)
    except ValueError:
        print("$SOURCE_DATE_EPOCH must be an integer")
        return False

    parser = argparse.ArgumentParser(
        description='Clamp .py source mtime to $SOURCE_DATE_EPOCH.')
    parser.add_argument('-q', action='count', dest='quiet', default=0,
                        help='output only error messages; -qq will suppress '
                             'the error messages as well.')
    parser.add_argument('clamp_dest', metavar='FILE|DIR', nargs='+',
                        help=('zero or more file and directory paths '
                              'to clamp'))

    args = parser.parse_args()
    clamp_dests = args.clamp_dest

    success = True
    try:
        for dest in clamp_dests:
            if os.path.isfile(dest):
                if not clamp_file(dest, quiet=args.quiet,
                                  source_date_epoch=source_date_epoch):
                    success = False
            else:
                if not clamp_dir(dest, quiet=args.quiet,
                                 source_date_epoch=source_date_epoch):
                    success = False
        return success
    except KeyboardInterrupt:
        if args.quiet < 2:
            print("\n[interrupted]")
        return False
    return True


if __name__ == '__main__':
    exit_status = int(not main())
    sys.exit(exit_status)
