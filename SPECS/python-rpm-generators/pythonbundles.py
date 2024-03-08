#!/usr/bin/python3 -sB
#                  (imports pythondistdeps from /usr/lib/rpm, hence -B)
#
# This program is free software.
#
# It is placed in the public domain or under the CC0-1.0-Universal license,
# whichever you choose.
#
# Alternatively, it may be redistributed and/or modified under the terms of
# the LGPL version 2.1 (or later) or GPL version 2 (or later).
#
# Use this script to generate bundled provides, e.g.:
# ./pythonbundles.py setuptools-47.1.1/pkg_resources/_vendor/vendored.txt

import pathlib
import sys

from packaging import requirements

import pythondistdeps

def generate_bundled_provides(paths, namespace):
    provides = set()

    for path in paths:
        for line in path.read_text().splitlines():
            line, _, comment = line.partition('#')
            if comment.startswith('egg='):
                # not a real comment
                # e.g. git+https://github.com/monty/spam.git@master#egg=spam&...
                egg, *_ = comment.strip().partition(' ')
                egg, *_ = egg.strip().partition('&')
                name = pythondistdeps.normalize_name(egg[4:])
                provides.add(f'Provides: bundled({namespace}({name}))')
                continue
            line = line.strip()
            if line:
                requirement = requirements.Requirement(line)
                for spec in requirement.specifier:
                    if spec.operator == '==':
                        version = spec.version
                        break
                else:
                    raise ValueError('pythonbundles.py only handles exactly one == requirement')
                name = pythondistdeps.normalize_name(requirement.name)
                bundled_name = f"bundled({namespace}({name}))"
                python_provide = pythondistdeps.convert(bundled_name, '==', version)
                provides.add(f'Provides: {python_provide}')

    return provides


def compare(expected, given):
    stripped = (l.strip() for l in given)
    no_comments = set(l for l in stripped if not l.startswith('#'))
    no_comments.discard('')
    if expected == no_comments:
        return True
    extra_expected = expected - no_comments
    extra_given = no_comments - expected
    if extra_expected:
        print('Missing expected provides:', file=sys.stderr)
        for provide in sorted(extra_expected):
            print(f'    - {provide}', file=sys.stderr)
    if extra_given:
        print('Redundant unexpected provides:', file=sys.stderr)
        for provide in sorted(extra_given):
            print(f'    + {provide}', file=sys.stderr)
    return False


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(prog=sys.argv[0],
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('vendored', metavar='VENDORED.TXT', nargs='+', type=pathlib.Path,
                        help='Upstream information about vendored libraries')
    parser.add_argument('-c', '--compare-with', action='store',
                        help='A string value to compare with and verify')
    parser.add_argument('-n', '--namespace', action='store',
                        help='What namespace of provides will used', default='python3dist')
    args = parser.parse_args()

    provides = generate_bundled_provides(args.vendored, args.namespace)

    if args.compare_with:
        given = args.compare_with.splitlines()
        same = compare(provides, given)
        if not same:
            sys.exit(1)
    else:
        for provide in sorted(provides):
            print(provide)
