#!/usr/bin/env python

'''
pycparser examples all contain the following boiler plate code
for running in tree. This script removes them:

# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
#
sys.path.extend(['.', '..'])
'''

import sys
import os

boiler_plate = "sys.path.extend(['.', '..'])\n"
d = sys.argv[1]
for (root, dirs, files) in os.walk(d):
    for i in files:
        if not i.endswith('.py'):
            continue
        fname = os.path.join(root, i)
        lines = open(fname).readlines()
        try:
            start = lines.index(boiler_plate)
            end = start
        except ValueError:
            start = None
            end = start
        if start is not None:
            while lines[start-1].startswith('#'):
                start -= 1

        if start is not None and end is not None:
            f = open(fname, 'w')
            f.writelines(lines[:start])
            f.writelines(lines[end+1:])
            f.close()
