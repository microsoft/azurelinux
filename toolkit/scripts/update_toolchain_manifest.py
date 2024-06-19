#!/usr/bin/python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import argparse
import os
import shlex
import subprocess

# Can't rely on Python's 'pyrpm.spec' module - it's not as good with parsing the spec as 'rpmspec' and may leave unexpanded macros.
RPMSPEC_COMMAND_COMMON = "rpmspec --parse -D 'forgemeta %{{nil}}' -D 'py3_dist X' -D 'with_check 0' -D 'dist .azl3' -D '__python3 python3' -D '_sourcedir {source_dir}' -D 'fillup_prereq fillup'"
manifest_files = ["pkggen_core_x86_64.txt", "toolchain_x86_64.txt", "pkggen_core_aarch64.txt",  "toolchain_aarch64.txt"]

class Entry:
    def __init__(self, name, version, release: str):
        self.name = name
        self.version = version
        self.release = release

    def get_processed_entry(self) -> str:
        return self.version+"-"+self.release

def formatted_rpmspec_command(spec_path: str) -> str:
    source_dir = os.path.dirname(spec_path)
    return f"{RPMSPEC_COMMAND_COMMON.format(source_dir=source_dir)}"

def read_spec_name(spec_path: str) -> str:
    return read_spec_tag(spec_path, "NAME")

def read_spec_version(spec_path: str) -> str:
    return read_spec_tag(spec_path, "VERSION")

def read_spec_release(spec_path: str):
    return read_spec_tag(spec_path, "RELEASE")

def read_spec_tag(spec_path, tag: str) -> str:
    command = formatted_rpmspec_command(spec_path)
    raw_output = subprocess.check_output(f"{command} --srpm --qf '%{{{tag}}}' -q {spec_path}", shell=True,
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

def dir_type(path: str) -> str:
    if(os.path.isdir(path)):
        return path
    else:
        raise NotADirectoryError(path, "is not a valid directory")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='''Tool for updating the toolchain and pkggen manifest files with values from the input spec files.
                    Sample usage: python3 scripts/update_toolchain_manifest.py --manifest_dir resources/manifests/package/ --specs ../SPECS/sqlite/sqlite.spec''')
    parser.add_argument('--manifest_dir',
                        type=dir_type,
                        required=True,
                        metavar='',
                        help='path to folder containing toolchain_.txt and pkggen_core_.txt files')
    parser.add_argument('--specs',
                        metavar='',
                        type=argparse.FileType('r'),
                        required=True,
                        nargs='+',
                        help='path to spec file(s)')
    args = parser.parse_args()
    manifest_dir = args.manifest_dir

    if not manifest_dir.endswith("/"):
        manifest_dir = manifest_dir+'/'

    for spec in args.specs:
        entry = process_spec(spec.name)
        for manifest in manifest_files:
            update_manifest(manifest_dir+manifest, entry)
