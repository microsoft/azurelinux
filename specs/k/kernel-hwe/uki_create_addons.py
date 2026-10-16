#!/usr/bin/env python3
#
# This script inspects a given json proving a list of addons, and
# creates an addon for each key/value pair matching the given uki, distro and
# arch provided in input.
#
# Usage: python uki_create_addons.py input_json out_dir uki distro arch [sbat]
#
# This tool requires the systemd-ukify and systemd-boot packages.
#
# Addon file
#-----------
# Each addon terminates with .addon
# Each addon contains only two types of lines:
# Lines beginning with '#' are description and thus ignored
# All other lines are command line to be added.
# The name of the end resulting addon is taken from the json hierarchy.
# For example, and addon in json['virt']['rhel']['x86_64']['hello.addon'] will
# result in an UKI addon file generated in out_dir called
# hello-virt.rhel.x86_64.addon.efi
#
# The common key, present in any sub-dict in the provided json (except the leaf dict)
# is used as place for default addons when the same addon is not defined deep
# in the hierarchy. For example, if we define test.addon (text: 'test1\n') in
# json['common']['test.addon'] = ['test1\n'] and another test.addon (text: test2) in
# json['virt']['common']['test.addon'] = ['test2'], any other uki except virt
# will have a test.addon.efi with text "test1", and virt will have a
# test.addon.efi with "test2"

import os
import sys
import json
import collections
import subprocess


UKIFY_PATH = '/usr/lib/systemd/ukify'

def usage(err):
    print(f'Usage: {os.path.basename(__file__)} input_json output_dir uki distro arch [sbat]')
    print(f'Error:{err}')
    sys.exit(1)

def check_clean_arguments(input_json, out_dir):
    # Remove end '/'
    if out_dir[-1:] == '/':
        out_dir = out_dir[:-1]
    if not os.path.isfile(input_json):
        usage(f'input_json {input_json} is not a file, or does not exist!')
    if not os.path.isdir(out_dir):
        usage(f'out_dir_dir {out_dir} is not a dir, or does not exist!')
    return out_dir

UKICmdlineAddon = collections.namedtuple('UKICmdlineAddon', ['name', 'cmdline'])
uki_addons_list = []
uki_addons = {}

def parse_lines(lines):
    cmdline = ''
    for l in lines:
        l = l.lstrip()
        if not l:
            continue
        if l[0] == '#':
            continue
        cmdline += l.rstrip() + ' '
    if cmdline == '':
        return ''
    return cmdline

def parse_all_addons(in_obj):
    for el in in_obj.keys():
        # addon found: copy it in our global dict uki_addons
        if el.endswith('.addon'):
            uki_addons[el] = in_obj[el]

def recursively_find_addons(in_obj, folder_list):
    # end of recursion, leaf directory. Search all addons here
    if len(folder_list) == 0:
        parse_all_addons(in_obj)
        return

    # first, check for common folder
    if 'common' in in_obj:
        parse_all_addons(in_obj['common'])

    # second, check if there is a match with the searched folder
    if folder_list[0] in in_obj:
        folder_next = in_obj[folder_list[0]]
        folder_list = folder_list[1:]
        recursively_find_addons(folder_next, folder_list)

def parse_in_json(in_json, uki_name, distro, arch):
    with open(in_json, 'r') as f:
        in_obj = json.load(f)
    recursively_find_addons(in_obj, [uki_name, distro, arch])

    for addon_name, cmdline in uki_addons.items():
        addon_name = addon_name.replace(".addon","")
        addon_full_name = f'{addon_name}-{uki_name}.{distro}.{arch}.addon.efi'
        cmdline = parse_lines(cmdline).rstrip()
        if cmdline:
            uki_addons_list.append(UKICmdlineAddon(addon_full_name, cmdline))

def create_addons(out_dir, sbat):
    for uki_addon in uki_addons_list:
        out_path = os.path.join(out_dir, uki_addon.name)
        cmd = [
            f'{UKIFY_PATH}', 'build',
            '--cmdline', uki_addon.cmdline,
            '--output', out_path]
        if sbat:
            cmd.extend(['--sbat', sbat.rstrip()])

        subprocess.check_call(cmd, text=True)

if __name__ == "__main__":
    argc = len(sys.argv) - 1
    if argc < 5 or argc > 6:
        usage('too few or too many parameters!')

    input_json = sys.argv[1]
    out_dir = sys.argv[2]
    uki_name = sys.argv[3]
    distro = sys.argv[4]
    arch = sys.argv[5]

    custom_sbat = None
    if argc == 6:
        custom_sbat = sys.argv[6]

    out_dir = check_clean_arguments(input_json, out_dir)
    parse_in_json(input_json, uki_name, distro, arch)
    create_addons(out_dir, custom_sbat)


