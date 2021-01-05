#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright 2010 Per Øyvind Karlsen <proyvind@moondrake.org>
# Copyright 2015 Neal Gompa <ngompa13@gmail.com>
#
# This program is free software. It may be redistributed and/or modified under
# the terms of the LGPL version 2.1 (or later).
#
# RPM python dependency generator, using .egg-info/.egg-link/.dist-info data
#

from __future__ import print_function
from getopt import getopt
from os.path import basename, dirname, isdir, sep
from sys import argv, stdin, version
from distutils.sysconfig import get_python_lib
from warnings import warn


opts, args = getopt(
    argv[1:], 'hPRrCEMmLl:',
    ['help', 'provides', 'requires', 'recommends', 'conflicts', 'extras', 'majorver-provides', 'majorver-only', 'legacy-provides' , 'legacy'])

Provides = False
Requires = False
Recommends = False
Conflicts = False
Extras = False
Provides_PyMajorVer_Variant = False
PyMajorVer_Deps = False
legacy_Provides = False
legacy = False

def normalize_name(name):
    """https://www.python.org/dev/peps/pep-0503/#normalized-names"""
    import re
    return re.sub(r'[-_.]+', '-', name).lower()

for o, a in opts:
    if o in ('-h', '--help'):
        print('-h, --help\tPrint help')
        print('-P, --provides\tPrint Provides')
        print('-R, --requires\tPrint Requires')
        print('-r, --recommends\tPrint Recommends')
        print('-C, --conflicts\tPrint Conflicts')
        print('-E, --extras\tPrint Extras ')
        print('-M, --majorver-provides\tPrint extra Provides with Python major version only')
        print('-m, --majorver-only\tPrint Provides/Requires with Python major version only')
        print('-L, --legacy-provides\tPrint extra legacy pythonegg Provides')
        print('-l, --legacy\tPrint legacy pythonegg Provides/Requires instead')
        exit(1)
    elif o in ('-P', '--provides'):
        Provides = True
    elif o in ('-R', '--requires'):
        Requires = True
    elif o in ('-r', '--recommends'):
        Recommends = True
    elif o in ('-C', '--conflicts'):
        Conflicts = True
    elif o in ('-E', '--extras'):
        Extras = True
    elif o in ('-M', '--majorver-provides'):
        Provides_PyMajorVer_Variant = True
    elif o in ('-m', '--majorver-only'):
        PyMajorVer_Deps = True
    elif o in ('-L', '--legacy-provides'):
        legacy_Provides = True
    elif o in ('-l', '--legacy'):
        legacy = True

if Requires:
    py_abi = True
else:
    py_abi = False
py_deps = {}
if args:
    files = args
else:
    files = stdin.readlines()

for f in files:
    f = f.strip()
    lower = f.lower()
    name = 'python(abi)'
    # add dependency based on path, versioned if within versioned python directory
    if py_abi and (lower.endswith('.py') or lower.endswith('.pyc') or lower.endswith('.pyo')):
        if name not in py_deps:
            py_deps[name] = []
        purelib = get_python_lib(standard_lib=0, plat_specific=0).split(version[:3])[0]
        platlib = get_python_lib(standard_lib=0, plat_specific=1).split(version[:3])[0]
        for lib in (purelib, platlib):
            if lib in f:
                spec = ('==', f.split(lib)[1].split(sep)[0])
                if spec not in py_deps[name]:
                    py_deps[name].append(spec)

    # XXX: hack to workaround RPM internal dependency generator not passing directories
    lower_dir = dirname(lower)
    if lower_dir.endswith('.egg') or \
            lower_dir.endswith('.egg-info') or \
            lower_dir.endswith('.dist-info'):
        lower = lower_dir
        f = dirname(f)
    # Determine provide, requires, conflicts & recommends based on egg/dist metadata
    if lower.endswith('.egg') or \
            lower.endswith('.egg-info') or \
            lower.endswith('.dist-info'):
        # This import is very slow, so only do it if needed
        from pkg_resources import Distribution, FileMetadata, PathMetadata, Requirement, parse_version
        dist_name = basename(f)
        if isdir(f):
            path_item = dirname(f)
            metadata = PathMetadata(path_item, f)
        else:
            path_item = f
            metadata = FileMetadata(f)
        dist = Distribution.from_location(path_item, dist_name, metadata)
        # Check if py_version is defined in the metadata file/directory name
        if not dist.py_version:
            # Try to parse the Python version from the path the metadata
            # resides at (e.g. /usr/lib/pythonX.Y/site-packages/...)
            import re
            res = re.search(r"/python(?P<pyver>\d+\.\d+)/", path_item)
            if res:
                dist.py_version = res.group('pyver')
            else:
                warn("Version for {!r} has not been found".format(dist), RuntimeWarning)
                continue

        # XXX: https://github.com/pypa/setuptools/pull/1275
        import platform
        platform.python_version = lambda: dist.py_version

        # This is the PEP 503 normalized name.
        # It does also convert dots to dashes, unlike dist.key.
        # In the current code, we only add additional provides with this.
        # Later, we can start requiring them.
        # See https://bugzilla.redhat.com/show_bug.cgi?id=1791530
        normalized_name = normalize_name(dist.project_name)

        if Provides_PyMajorVer_Variant or PyMajorVer_Deps or legacy_Provides or legacy:
            # Get the Python major version
            pyver_major = dist.py_version.split('.')[0]
        if Provides:
            # If egg/dist metadata says package name is python, we provide python(abi)
            if dist.key == 'python':
                name = 'python(abi)'
                if name not in py_deps:
                    py_deps[name] = []
                py_deps[name].append(('==', dist.py_version))
            if not legacy or not PyMajorVer_Deps:
                name = 'python{}dist({})'.format(dist.py_version, dist.key)
                if name not in py_deps:
                    py_deps[name] = []
                name_ = 'python{}dist({})'.format(dist.py_version, normalized_name)
                if name_ not in py_deps:
                    py_deps[name_] = []
            if Provides_PyMajorVer_Variant or PyMajorVer_Deps:
                pymajor_name = 'python{}dist({})'.format(pyver_major, dist.key)
                if pymajor_name not in py_deps:
                    py_deps[pymajor_name] = []
                pymajor_name_ = 'python{}dist({})'.format(pyver_major, normalized_name)
                if pymajor_name_ not in py_deps:
                    py_deps[pymajor_name_] = []
            if legacy or legacy_Provides:
                legacy_name = 'pythonegg({})({})'.format(pyver_major, dist.key)
                if legacy_name not in py_deps:
                    py_deps[legacy_name] = []
            if dist.version:
                version = dist.version
                while version.endswith('.0'):
                    version = version[:-2]
                spec = ('==', version)
                if spec not in py_deps[name]:
                    if not legacy:
                        py_deps[name].append(spec)
                        if name != name_:
                            py_deps[name_].append(spec)
                    if Provides_PyMajorVer_Variant:
                        py_deps[pymajor_name].append(spec)
                        if pymajor_name != pymajor_name_:
                            py_deps[pymajor_name_].append(spec)
                    if legacy or legacy_Provides:
                        py_deps[legacy_name].append(spec)
        if Requires or (Recommends and dist.extras):
            name = 'python(abi)'
            # If egg/dist metadata says package name is python, we don't add dependency on python(abi)
            if dist.key == 'python':
                py_abi = False
                if name in py_deps:
                    py_deps.pop(name)
            elif py_abi and dist.py_version:
                if name not in py_deps:
                    py_deps[name] = []
                spec = ('==', dist.py_version)
                if spec not in py_deps[name]:
                    py_deps[name].append(spec)
            deps = dist.requires()
            if Recommends:
                depsextras = dist.requires(extras=dist.extras)
                if not Requires:
                    for dep in reversed(depsextras):
                        if dep in deps:
                            depsextras.remove(dep)
                deps = depsextras
            # console_scripts/gui_scripts entry points need pkg_resources from setuptools
            if ((dist.get_entry_map('console_scripts') or
                     dist.get_entry_map('gui_scripts')) and
                    (lower.endswith('.egg') or
                     lower.endswith('.egg-info'))):
                # stick them first so any more specific requirement overrides it
                deps.insert(0, Requirement.parse('setuptools'))
            # add requires/recommends based on egg/dist metadata
            for dep in deps:
                if legacy:
                    name = 'pythonegg({})({})'.format(pyver_major, dep.key)
                else:
                    if PyMajorVer_Deps:
                        name = 'python{}dist({})'.format(pyver_major, dep.key)
                    else:
                        name = 'python{}dist({})'.format(dist.py_version, dep.key)
                for spec in dep.specs:
                    while spec[1].endswith('.0'):
                        spec = (spec[0], spec[1][:-2])
                    if name not in py_deps:
                        py_deps[name] = []
                    if spec not in py_deps[name]:
                        py_deps[name].append(spec)
                if not dep.specs:
                    py_deps[name] = []
        # Unused, for automatic sub-package generation based on 'extras' from egg/dist metadata
        # TODO: implement in rpm later, or...?
        if Extras:
            deps = dist.requires()
            extras = dist.extras
            print(extras)
            for extra in extras:
                print('%%package\textras-{}'.format(extra))
                print('Summary:\t{} extra for {} python package'.format(extra, dist.key))
                print('Group:\t\tDevelopment/Python')
                depsextras = dist.requires(extras=[extra])
                for dep in reversed(depsextras):
                    if dep in deps:
                        depsextras.remove(dep)
                deps = depsextras
                for dep in deps:
                    for spec in dep.specs:
                        if spec[0] == '!=':
                            print('Conflicts:\t{} {} {}'.format(dep.key, '==', spec[1]))
                        else:
                            print('Requires:\t{} {} {}'.format(dep.key, spec[0], spec[1]))
                print('%%description\t{}'.format(extra))
                print('{} extra for {} python package'.format(extra, dist.key))
                print('%%files\t\textras-{}\n'.format(extra))
        if Conflicts:
            # Should we really add conflicts for extras?
            # Creating a meta package per extra with recommends on, which has
            # the requires/conflicts in stead might be a better solution...
            for dep in dist.requires(extras=dist.extras):
                name = dep.key
                for spec in dep.specs:
                    if spec[0] == '!=':
                        if name not in py_deps:
                            py_deps[name] = []
                        spec = ('==', spec[1])
                        if spec not in py_deps[name]:
                            py_deps[name].append(spec)
names = list(py_deps.keys())
names.sort()
for name in names:
    if py_deps[name]:
        # Print out versioned provides, requires, recommends, conflicts
        spec_list = []
        for spec in py_deps[name]:
            if spec[0] == '!=':
                spec_list.append('({n} < {v} or {n} >= {v}.0)'.format(n=name, v=spec[1]))
            elif spec[0] == '~=':
                # Parse the current version
                next_ver = parse_version(spec[1]).base_version.split('.')
                # Drop the micro version
                next_ver = next_ver[0:-1]
                # Increment the minor version
                next_ver[-1] = str(int(next_ver[-1]) + 1)
                next_ver = '.'.join(next_ver)
                spec_list.append('({n} >= {v} with {n} < {vnext})'.format(n=name, v=spec[1], vnext=next_ver))
            elif spec[0] == '==' and spec[1].endswith('.*'):
                # Parse the current version
                next_ver = parse_version(spec[1]).base_version.split('.')
                # Drop the micro version from both the version in spec and next_ver
                next_ver = next_ver[0:-1]
                spec = (spec[0], '.'.join(next_ver))
                # Increment the minor version
                next_ver[-1] = str(int(next_ver[-1]) + 1)
                next_ver = '.'.join(next_ver)
                spec_list.append('({n} >= {v} with {n} < {vnext})'.format(n=name, v=spec[1], vnext=next_ver))
            else:
                spec_list.append('{} {} {}'.format(name, spec[0], spec[1]))
        if len(spec_list) == 1:
            print(spec_list[0])
        else:
            print('({})'.format(' with '.join(spec_list)))
    else:
        # Print out unversioned provides, requires, recommends, conflicts
        print(name)
