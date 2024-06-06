#!/usr/bin/python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from os.path import dirname

import argparse
import shlex
import subprocess

# Can't rely on Python's 'pyrpm.spec' module - it's not as good with parsing the spec as 'rpmspec' and may leave unexpanded macros.
RPMSPEC_COMMAND_COMMON = "rpmspec --parse -D 'forgemeta %{{nil}}' -D 'py3_dist X' -D 'with_check 0' -D 'dist .azl3' -D '__python3 python3' -D '_sourcedir {source_dir}' -D 'fillup_prereq fillup'"

class Entry:
    def __init__(self, name, version, release: str):
        self.name = name
        self.version = version
        self.release = release

    def get_processed_entry(self) -> str:
        return self.version+"-"+self.release

def formatted_rpmspec_command(spec_path: str) -> str:
    source_dir = dirname(spec_path)
    return f"{RPMSPEC_COMMAND_COMMON.format(source_dir=source_dir)}"

def read_spec_name(spec_path: str) -> str:
    return read_spec_tag(spec_path, "NAME")

def read_spec_version(spec_path: str) -> str:
    return read_spec_tag(spec_path, "VERSION")

def read_spec_release(spec_path: str):
    return read_spec_tag(spec_path, "RELEASE")

def read_spec_tag(spec_path, tag: str) -> str:
    command = formatted_rpmspec_command(spec_path)
    raw_output = subprocess.check_output(shlex.split(f"{command} --srpm --qf '%{{{tag}}}' -q {spec_path}"),
                                         stderr=subprocess.DEVNULL)
    return str(raw_output, encoding="utf-8", errors="strict")

def get_arch(manifest: str) -> str:
    if "x86_64" in manifest:
        arch = "x86_64"
    elif "aarch64" in manifest:
        arch = "aarch64"
    else:
        raise ValueError("failed to find architecture of manifest file")
    return arch

def update_manifest(manifest: str, entry: Entry):
    updated_manifest = []
    arch = get_arch(manifest)

    with open(manifest,"r") as manifest_file:
        for line in manifest_file:
            if line.startswith(entry.name):
                sublines = line.split('-')
                replace_line = sublines[-2]+"-"+sublines[-1] #{version}-{release}.{arch}.rpm
                line = line.replace(replace_line, entry.get_processed_entry()+"."+arch+".rpm\n")
            updated_manifest.append(line)

    with open(manifest, "w") as manifest_file:
        manifest_file.writelines((str(i) for i in updated_manifest))

    return

def process_spec(spec_path: str) -> Entry:
    print(f"Processing: {spec_path}")

    name = read_spec_name(spec_path)
    version = read_spec_version(spec_path)
    release = read_spec_release(spec_path)

    return Entry(name, version, release)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='''Tool for updating the 'toolchain_manifest*.json' with values from the input spec files.
                    Usage: python3 update_toolchain_manifest.py <path_to_toolchain_manifest.txt> <path_to_spec> ...''')
    parser.add_argument('manifest_file',
                        type=argparse.FileType(),
                        metavar='manifest_file',
                        help='path to the "toolchain_manifest.json" file')
    parser.add_argument('specs',
                        metavar='spec_path',
                        type=argparse.FileType('r'),
                        nargs='+',
                        help='path to spec file(s)')
    args = parser.parse_args()

    for spec in args.specs:
        entry = process_spec(spec.name)
        update_manifest(args.manifest_file.name, entry)
