#!/usr/bin/python3
# SPDX-License-Identifier: GPL-2.0
# Author: Clark Williams <williams@redhat.com>
# Copyright (C) 2022 Red Hat, Inc.
#
# merge.py - a direct replacement for merge.pl in the redhat/configs directory
#
# invocation:   python merge.py overrides baseconfig [arch]
#
# This script merges two kernel configuration files, an override file and a
# base config file and writes the results to stdout.
#
# The script reads the overrides into a dictionary, then reads the baseconfig
# file, looking for overrides and replacing any found, then printing the result
# to stdout. Finally any remaining (new) configs in the override are appended to the
# end of the output

import sys
import re
import os.path

def usage(msg):
    '''print a usage message and exit'''
    sys.stderr.write(msg + "\n")
    sys.stderr.write("usage: merge.py overrides baseconfig [arch]\n")
    sys.exit(1)

isset = re.compile(r'^(CONFIG_\w+)=')
notset = re.compile(r'^#\s+(CONFIG_\w+)\s+is not set')

# search an input line for a config (set or notset) pattern
# if we get a match return the config that is being changed
def find_config(line):
    '''find a configuration line in the input and return the config name'''
    m = isset.match(line)
    if (m is not None):
        return m.group(1)

    m = notset.match(line)
    if (m is not None):
        return m.group(1)

    return None

#########################################################

if len(sys.argv) < 3:
    usage("must have two input files")

override_file = sys.argv[1]
baseconfig_file = sys.argv[2]

if not os.path.exists(override_file):
    usage(f"overrides config file {override_file:s} does not exist!")

if not os.path.exists(baseconfig_file):
    usage(f"base configs file {baseconfig_file:s} does not exist")

if len(sys.argv) == 4:
    print(f"# {sys.argv[3]:s}")

# read each line of the override file and store any configuration values
# in the overrides dictionary, keyed by the configuration name.
overrides = {}
with open(override_file, "rt", encoding="utf-8") as f:
    for line in [l.strip() for l in f.readlines()]:
        c = find_config(line)
        if c and c not in overrides:
            overrides[c] = line

# now read and print the base config, checking each line
# that defines a config value and printing the override if
# it exists
with open(baseconfig_file, "rt", encoding="utf-8") as f:
    for line in [ l.strip() for l in f.readlines() ]:
        c = find_config(line)
        if c and c in overrides:
            print(overrides[c])
            del overrides[c]
        else:
            print(line)

# print out the remaining configs (new values)
# from the overrides file
for v in overrides.values():
    print (v)

sys.exit(0)
