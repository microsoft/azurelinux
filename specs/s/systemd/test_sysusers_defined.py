#!/usr/bin/python

import os
import sys

def parse_sysusers_file(filename):
    users, groups = set(), set()

    for line in open(filename):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        words = line.split()
        match words[0]:
            case 'u'|'u!':
                users.add(words[1])
            case 'g':
                groups.add(words[1])
            case 'm'|'r':
                continue
            case _:
                assert False
    return users, groups

setup_users, setup_groups = set(), set()

for arg in sys.argv[1:-1]:
    users, groups = parse_sysusers_file(arg)
    setup_users |= users
    setup_groups |= groups

basic_users, basic_groups = parse_sysusers_file(sys.argv[-1])

ignored = set(os.getenv('IGNORED', '').split())

if d := basic_users - setup_users - ignored:
    exit(f'We have new users: {d}')
if d := basic_groups - setup_groups - ignored:
    exit(f'We have new groups: {d}')
