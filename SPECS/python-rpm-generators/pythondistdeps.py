#!/usr/bin/python3 -s
# -*- coding: utf-8 -*-
#
# Copyright 2010 Per Ã˜yvind Karlsen <proyvind@moondrake.org>
# Copyright 2015 Neal Gompa <ngompa13@gmail.com>
# Copyright 2020 SUSE LLC
#
# This program is free software. It may be redistributed and/or modified under
# the terms of the LGPL version 2.1 (or later).
#
# RPM python dependency generator, using .egg-info/.egg-link/.dist-info data
#

from __future__ import print_function
import argparse
from os.path import dirname, sep
import re
from sys import argv, stdin, stderr, version_info
from sysconfig import get_path
from warnings import warn

from packaging.requirements import Requirement as Requirement_
from packaging.version import parse
import packaging.markers

# Monkey patching packaging.markers to handle extras names in a
# case-insensitive manner:
#   pip considers dnspython[DNSSEC] and dnspython[dnssec] to be equal, but
#   packaging markers treat extras in a case-sensitive manner. To solve this
#   issue, we introduce a comparison operator that compares case-insensitively
#   if both sides of the comparison are strings. And then we inject this
#   operator into packaging.markers to be used when comparing names of extras.
# Fedora BZ: https://bugzilla.redhat.com/show_bug.cgi?id=1936875
# Upstream issue: https://discuss.python.org/t/what-extras-names-are-treated-as-equal-and-why/7614
# - After it's established upstream what is the canonical form of an extras
#   name, we plan to open an issue with packaging to hopefully solve this
#   there without having to resort to monkeypatching.
def str_lower_eq(a, b):
    if isinstance(a, str) and isinstance(b, str):
        return a.lower() == b.lower()
    else:
        return a == b
packaging.markers._operators["=="] = str_lower_eq

try:
    from importlib.metadata import PathDistribution
except ImportError:
    from importlib_metadata import PathDistribution

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path


def normalize_name(name):
    """https://www.python.org/dev/peps/pep-0503/#normalized-names"""
    return re.sub(r'[-_.]+', '-', name).lower()


def legacy_normalize_name(name):
    """Like pkg_resources Distribution.key property"""
    return re.sub(r'[-_]+', '-', name).lower()


class Requirement(Requirement_):
    def __init__(self, requirement_string):
        super(Requirement, self).__init__(requirement_string)
        self.normalized_name = normalize_name(self.name)
        self.legacy_normalized_name = legacy_normalize_name(self.name)


class Distribution(PathDistribution):
    def __init__(self, path):
        super(Distribution, self).__init__(Path(path))

        # Check that the initialization went well and metadata are not missing or corrupted
        # name is the most important attribute, if it doesn't exist, import failed
        if not self.name or not isinstance(self.name, str):
            print("*** PYTHON_METADATA_FAILED_TO_PARSE_ERROR___SEE_STDERR ***")
            print('Error: Python metadata at `{}` are missing or corrupted.'.format(path), file=stderr)
            exit(65)  # os.EX_DATAERR

        self.normalized_name = normalize_name(self.name)
        self.legacy_normalized_name = legacy_normalize_name(self.name)
        self.requirements = [Requirement(r) for r in self.requires or []]
        self.extras = [
            v.lower() for k, v in self.metadata.items() if k == 'Provides-Extra']
        self.py_version = self._parse_py_version(path)

    # `name` is defined as a property exactly like this in Python 3.10 in the
    # PathDistribution class. Due to that we can't redefine `name` as a normal
    # attribute. So we copied the Python 3.10 definition here into the code so
    # that it works also on previous Python/importlib_metadata versions.
    @property
    def name(self):
        """Return the 'Name' metadata for the distribution package or None."""
        return self.metadata.get('Name')

    def _parse_py_version(self, path):
        # Try to parse the Python version from the path the metadata
        # resides at (e.g. /usr/lib/pythonX.Y/site-packages/...)
        res = re.search(r"/python(?P<pyver>\d+\.\d+)/", path)
        if res:
            return res.group('pyver')
        # If that hasn't worked, attempt to parse it from the metadata
        # directory name
        res = re.search(r"-py(?P<pyver>\d+.\d+)[.-]egg-info$", path)
        if res:
            return res.group('pyver')
        return None

    def requirements_for_extra(self, extra):
        extra_deps = []
        # we are only interested in dependencies with extra == 'our_extra' marker
        for req in self.requirements:
            # no marker at all, nothing to evaluate
            if not req.marker:
                continue
            # does the marker include extra == 'our_extra'?
            # we can only evaluate the marker as a whole,
            # so we evaluate it twice (using 2 different marker_envs)
            # and see if it only evaluates to True with our extra
            if (req.marker.evaluate(get_marker_env(self, extra)) and
                    not req.marker.evaluate(get_marker_env(self, None))):
                extra_deps.append(req)
        return extra_deps

    def __repr__(self):
        return '{} from {}'.format(self.name, self._path)


class RpmVersion():
    def __init__(self, version_id):
        version = parse(version_id)
        if isinstance(version._version, str):
            self.version = version._version
        else:
            self.epoch = version._version.epoch
            self.version = list(version._version.release)
            self.pre = version._version.pre
            self.dev = version._version.dev
            self.post = version._version.post
            # version.local is ignored as it is not expected to appear
            # in public releases
            # https://www.python.org/dev/peps/pep-0440/#local-version-identifiers

    def is_legacy(self):
        return isinstance(self.version, str)

    def increment(self):
        self.version[-1] += 1
        self.pre = None
        self.dev = None
        self.post = None
        return self

    def is_zero(self):
        return self.__str__() == '0'

    def __str__(self):
        if self.is_legacy():
            return self.version
        if self.epoch:
            rpm_epoch = str(self.epoch) + ':'
        else:
            rpm_epoch = ''
        while len(self.version) > 1 and self.version[-1] == 0:
            self.version.pop()
        rpm_version = '.'.join(str(x) for x in self.version)
        if self.pre:
            rpm_suffix = '~{}'.format(''.join(str(x) for x in self.pre))
        elif self.dev:
            rpm_suffix = '~~{}'.format(''.join(str(x) for x in self.dev))
        elif self.post:
            rpm_suffix = '^post{}'.format(self.post[1])
        else:
            rpm_suffix = ''
        return '{}{}{}'.format(rpm_epoch, rpm_version, rpm_suffix)


def convert_compatible(name, operator, version_id):
    if version_id.endswith('.*'):
        print("*** INVALID_REQUIREMENT_ERROR___SEE_STDERR ***")
        print('Invalid requirement: {} {} {}'.format(name, operator, version_id), file=stderr)
        exit(65)  # os.EX_DATAERR
    version = RpmVersion(version_id)
    if version.is_legacy():
        # LegacyVersions are not supported in this context
        print("*** INVALID_REQUIREMENT_ERROR___SEE_STDERR ***")
        print('Invalid requirement: {} {} {}'.format(name, operator, version_id), file=stderr)
        exit(65)  # os.EX_DATAERR
    if len(version.version) == 1:
        print("*** INVALID_REQUIREMENT_ERROR___SEE_STDERR ***")
        print('Invalid requirement: {} {} {}'.format(name, operator, version_id), file=stderr)
        exit(65)  # os.EX_DATAERR
    upper_version = RpmVersion(version_id)
    upper_version.version.pop()
    upper_version.increment()
    return '({} >= {} with {} < {})'.format(
        name, version, name, upper_version)


def convert_equal(name, operator, version_id):
    if version_id.endswith('.*'):
        version_id = version_id[:-2] + '.0'
        return convert_compatible(name, '~=', version_id)
    version = RpmVersion(version_id)
    return '{} = {}'.format(name, version)


def convert_arbitrary_equal(name, operator, version_id):
    if version_id.endswith('.*'):
        print("*** INVALID_REQUIREMENT_ERROR___SEE_STDERR ***")
        print('Invalid requirement: {} {} {}'.format(name, operator, version_id), file=stderr)
        exit(65)  # os.EX_DATAERR
    version = RpmVersion(version_id)
    return '{} = {}'.format(name, version)


def convert_not_equal(name, operator, version_id):
    if version_id.endswith('.*'):
        version_id = version_id[:-2]
        version = RpmVersion(version_id)
        if version.is_legacy():
            # LegacyVersions are not supported in this context
            print("*** INVALID_REQUIREMENT_ERROR___SEE_STDERR ***")
            print('Invalid requirement: {} {} {}'.format(name, operator, version_id), file=stderr)
            exit(65)  # os.EX_DATAERR
        version_gt = RpmVersion(version_id).increment()
        version_gt_operator = '>='
        # Prevent dev and pre-releases from satisfying a < requirement
        version = '{}~~'.format(version)
    else:
        version = RpmVersion(version_id)
        version_gt = version
        version_gt_operator = '>'
    return '({} < {} or {} {} {})'.format(
        name, version, name, version_gt_operator, version_gt)


def convert_ordered(name, operator, version_id):
    if version_id.endswith('.*'):
        # PEP 440 does not define semantics for prefix matching
        # with ordered comparisons
        # see: https://github.com/pypa/packaging/issues/320
        # and: https://github.com/pypa/packaging/issues/321
        # This style of specifier is officially "unsupported",
        # even though it is processed.  Support may be removed
        # in version 21.0.
        version_id = version_id[:-2]
        version = RpmVersion(version_id)
        if operator == '>':
            # distutils will allow a prefix match with '>'
            operator = '>='
        if operator == '<=':
            # distutils will not allow a prefix match with '<='
            operator = '<'
    else:
        version = RpmVersion(version_id)
    # For backwards compatibility, fallback to previous behavior with LegacyVersions
    if not version.is_legacy():
        # Prevent dev and pre-releases from satisfying a < requirement
        if operator == '<' and not version.pre and not version.dev and not version.post:
            version = '{}~~'.format(version)
        # Prevent post-releases from satisfying a > requirement
        if operator == '>' and not version.pre and not version.dev and not version.post:
            version = '{}.0'.format(version)
    return '{} {} {}'.format(name, operator, version)


OPERATORS = {'~=': convert_compatible,
             '==': convert_equal,
             '===': convert_arbitrary_equal,
             '!=': convert_not_equal,
             '<=': convert_ordered,
             '<': convert_ordered,
             '>=': convert_ordered,
             '>': convert_ordered}


def convert(name, operator, version_id):
    try:
        return OPERATORS[operator](name, operator, version_id)
    except Exception as exc:
        raise RuntimeError("Cannot process Python package version `{}` for name `{}`".
                           format(version_id, name)) from exc


def get_marker_env(dist, extra):
    # packaging uses a default environment using
    # platform.python_version to evaluate if a dependency is relevant
    # based on environment markers [1],
    # e.g. requirement `argparse;python_version<"2.7"`
    #
    # Since we're running this script on one Python version while
    # possibly evaluating packages for different versions, we
    # set up an environment with the version we want to evaluate.
    #
    # [1] https://www.python.org/dev/peps/pep-0508/#environment-markers
    return {"python_full_version": dist.py_version,
            "python_version": dist.py_version,
            "extra": extra}


def main():
    """To allow this script to be importable (and its classes/functions
       reused), actions are defined in the main function and are performed only
       when run as a main script."""
    parser = argparse.ArgumentParser(prog=argv[0])
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-P', '--provides', action='store_true', help='Print Provides')
    group.add_argument('-R', '--requires', action='store_true', help='Print Requires')
    group.add_argument('-r', '--recommends', action='store_true', help='Print Recommends')
    group.add_argument('-C', '--conflicts', action='store_true', help='Print Conflicts')
    group.add_argument('-E', '--extras', action='store_true', help='[Unused] Generate spec file snippets for extras subpackages')
    group_majorver = parser.add_mutually_exclusive_group()
    group_majorver.add_argument('-M', '--majorver-provides', action='store_true', help='Print extra Provides with Python major version only')
    group_majorver.add_argument('--majorver-provides-versions', action='append',
                                help='Print extra Provides with Python major version only for listed '
                                     'Python VERSIONS (appended or comma separated without spaces, e.g. 2.7,3.9)')
    parser.add_argument('-m', '--majorver-only', action='store_true', help='Print Provides/Requires with Python major version only')
    parser.add_argument('-n', '--normalized-names-format', action='store',
                        default="legacy-dots", choices=["pep503", "legacy-dots"],
                        help='Format of normalized names according to pep503 or legacy format that allows dots [default]')
    parser.add_argument('--normalized-names-provide-both', action='store_true',
                        help='Provide both `pep503` and `legacy-dots` format of normalized names (useful for a transition period)')
    parser.add_argument('-L', '--legacy-provides', action='store_true', help='Print extra legacy pythonegg Provides')
    parser.add_argument('-l', '--legacy', action='store_true', help='Print legacy pythonegg Provides/Requires instead')
    parser.add_argument('--console-scripts-nodep-setuptools-since', action='store',
                        help='An optional Python version (X.Y), at least 3.8. '
                             'For that version and any newer version, '
                             'a dependency on "setuptools" WILL NOT be generated for packages with console_scripts/gui_scripts entry points. '
                             'By setting this flag, you guarantee that setuptools >= 47.2.0 is used '
                             'during the build of packages for this and any newer Python version.')
    parser.add_argument('--require-extras-subpackages', action='store_true',
                        help="If there is a dependency on a package with extras functionality, require the extras subpackage")
    parser.add_argument('--package-name', action='store', help="Name of the RPM package that's being inspected. Required for extras requires/provides to work.")
    parser.add_argument('--namespace', action='store', help="Namespace for the printed Requires, Provides, Recommends and Conflicts")
    parser.add_argument('--fail-if-zero', action='store_true', help='Fail the script if the automatically generated Provides version was 0, which usually indicates a packaging error.')
    parser.add_argument('files', nargs=argparse.REMAINDER, help="Files from the RPM package that are to be inspected, can also be supplied on stdin")
    args = parser.parse_args()

    if args.fail_if_zero and not args.provides:
        raise parser.error('--fail-if-zero only works with --provides')

    py_abi = args.requires
    py_deps = {}

    if args.majorver_provides_versions:
        # Go through the arguments (can be specified multiple times),
        # and parse individual versions (can be comma-separated)
        args.majorver_provides_versions = [v for vstring in args.majorver_provides_versions
                                             for v in vstring.split(",")]

    # If normalized_names_require_pep503 is True we require the pep503
    # normalized name, if it is False we provide the legacy normalized name
    normalized_names_require_pep503 = args.normalized_names_format == "pep503"

    # If normalized_names_provide_pep503/legacy is True we provide the
    #   pep503/legacy normalized name, if it is False we don't
    normalized_names_provide_pep503 = \
        args.normalized_names_format == "pep503" or args.normalized_names_provide_both
    normalized_names_provide_legacy = \
        args.normalized_names_format == "legacy-dots" or args.normalized_names_provide_both

    # At least one type of normalization must be provided
    assert normalized_names_provide_pep503 or normalized_names_provide_legacy

    if args.console_scripts_nodep_setuptools_since:
        nodep_setuptools_pyversion = parse(args.console_scripts_nodep_setuptools_since)
        if nodep_setuptools_pyversion < parse("3.8"):
            print("Only version 3.8+ is supported in --console-scripts-nodep-setuptools-since", file=stderr)
            print("*** PYTHON_EXTRAS_ARGUMENT_ERROR___SEE_STDERR ***")
            exit(65)  # os.EX_DATAERR
    else:
        nodep_setuptools_pyversion = None

    # Is this script being run for an extras subpackage?
    extras_subpackage = None
    if args.package_name and '+' in args.package_name:
        # The extras names are encoded in the package names after the + sign.
        # We take the part after the rightmost +, ignoring when empty,
        # this allows packages like nicotine+ or c++ to work fine.
        # While packages with names like +spam or foo+bar would break,
        # names started with the plus sign are not very common
        # and pluses in the middle can be easily replaced with dashes.
        # Python extras names don't contain pluses according to PEP 508.
        package_name_parts = args.package_name.rpartition('+')
        extras_subpackage = package_name_parts[2].lower() or None

    namespace = (args.namespace + "({})") if args.namespace else "{}"

    for f in (args.files or stdin.readlines()):
        f = f.strip()
        lower = f.lower()
        name = 'python(abi)'
        # add dependency based on path, versioned if within versioned python directory
        if py_abi and (lower.endswith('.py') or lower.endswith('.pyc') or lower.endswith('.pyo')):
            if name not in py_deps:
                py_deps[name] = []
            running_python_version = '{}.{}'.format(*version_info[:2])
            purelib = get_path('purelib').split(running_python_version)[0]
            platlib = get_path('platlib').split(running_python_version)[0]
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
            dist = Distribution(f)
            if not dist.py_version:
                warn("Version for {!r} has not been found".format(dist), RuntimeWarning)
                continue

            # If processing an extras subpackage:
            #   Check that the extras name is declared in the metadata, or
            #   that there are some dependencies associated with the extras
            #   name in the requires.txt (this is an outdated way to declare
            #   extras packages).
            # - If there is an extras package declared only in requires.txt
            #   without any dependencies, this check will fail. In that case
            #   make sure to use updated metadata and declare the extras
            #   package there.
            if extras_subpackage and extras_subpackage not in dist.extras and not dist.requirements_for_extra(extras_subpackage):
                print("*** PYTHON_EXTRAS_NOT_FOUND_ERROR___SEE_STDERR ***")
                print(f"\nError: The package name contains an extras name `{extras_subpackage}` that was not found in the metadata.\n"
                      "Check if the extras were removed from the project. If so, consider removing the subpackage and obsoleting it from another.\n", file=stderr)
                exit(65)  # os.EX_DATAERR

            if args.majorver_provides or args.majorver_provides_versions or \
                    args.majorver_only or args.legacy_provides or args.legacy:
                # Get the Python major version
                pyver_major = dist.py_version.split('.')[0]
            if args.provides:
                extras_suffix = f"[{extras_subpackage}]" if extras_subpackage else ""
                # If egg/dist metadata says package name is python, we provide python(abi)
                if dist.normalized_name == 'python':
                    name = namespace.format('python(abi)')
                    if name not in py_deps:
                        py_deps[name] = []
                    py_deps[name].append(('==', dist.py_version))
                if not args.legacy or not args.majorver_only:
                    if normalized_names_provide_legacy:
                        name = namespace.format('python{}dist({}{})').format(dist.py_version, dist.legacy_normalized_name, extras_suffix)
                        if name not in py_deps:
                            py_deps[name] = []
                    if normalized_names_provide_pep503:
                        name_ = namespace.format('python{}dist({}{})').format(dist.py_version, dist.normalized_name, extras_suffix)
                        if name_ not in py_deps:
                            py_deps[name_] = []
                if args.majorver_provides or args.majorver_only or \
                        (args.majorver_provides_versions and dist.py_version in args.majorver_provides_versions):
                    if normalized_names_provide_legacy:
                        pymajor_name = namespace.format('python{}dist({}{})').format(pyver_major, dist.legacy_normalized_name, extras_suffix)
                        if pymajor_name not in py_deps:
                            py_deps[pymajor_name] = []
                    if normalized_names_provide_pep503:
                        pymajor_name_ = namespace.format('python{}dist({}{})').format(pyver_major, dist.normalized_name, extras_suffix)
                        if pymajor_name_ not in py_deps:
                            py_deps[pymajor_name_] = []
                if args.legacy or args.legacy_provides:
                    legacy_name = namespace.format('pythonegg({})({})').format(pyver_major, dist.legacy_normalized_name)
                    if legacy_name not in py_deps:
                        py_deps[legacy_name] = []
                if dist.version:
                    version = dist.version
                    spec = ('==', version)
                    if args.fail_if_zero:
                        if RpmVersion(version).is_zero():
                            print('*** PYTHON_PROVIDED_VERSION_NORMALIZES_TO_ZERO___SEE_STDERR ***')
                            print(f'\nError: The version in the Python package metadata {version} normalizes to zero.\n'
                                  'It\'s likely a packaging error caused by missing version information\n'
                                  '(e.g. when using a version control system snapshot as a source).\n'
                                  'Try providing the version information manually when building the Python package,\n'
                                  'for example by setting the SETUPTOOLS_SCM_PRETEND_VERSION environment variable if the package uses setuptools_scm.\n'
                                  'If you are confident that the version of the Python package is intentionally zero,\n'
                                  'you may %define the _python_dist_allow_version_zero macro in the spec file to disable this check.\n', file=stderr)
                            exit(65)  # os.EX_DATAERR

                    if normalized_names_provide_legacy:
                        if spec not in py_deps[name]:
                            py_deps[name].append(spec)
                            if args.majorver_provides or \
                                    (args.majorver_provides_versions and dist.py_version in args.majorver_provides_versions):
                                py_deps[pymajor_name].append(spec)
                    if normalized_names_provide_pep503:
                        if spec not in py_deps[name_]:
                            py_deps[name_].append(spec)
                            if args.majorver_provides or \
                                    (args.majorver_provides_versions and dist.py_version in args.majorver_provides_versions):
                                py_deps[pymajor_name_].append(spec)
                    if args.legacy or args.legacy_provides:
                        if spec not in py_deps[legacy_name]:
                            py_deps[legacy_name].append(spec)
            if args.requires or (args.recommends and dist.extras):
                name = namespace.format('python(abi)')
                # If egg/dist metadata says package name is python, we don't add dependency on python(abi)
                if dist.normalized_name == 'python':
                    py_abi = False
                    if name in py_deps:
                        py_deps.pop(name)
                elif py_abi and dist.py_version:
                    if name not in py_deps:
                        py_deps[name] = []
                    spec = ('==', dist.py_version)
                    if spec not in py_deps[name]:
                        py_deps[name].append(spec)

                if extras_subpackage:
                    deps = [d for d in dist.requirements_for_extra(extras_subpackage)]
                else:
                    deps = dist.requirements

                # console_scripts/gui_scripts entry points needed pkg_resources from setuptools
                # on new Python/setuptools versions, this is no longer required
                if nodep_setuptools_pyversion is None or parse(dist.py_version) < nodep_setuptools_pyversion:
                    if (dist.entry_points and
                        (lower.endswith('.egg') or
                         lower.endswith('.egg-info'))):
                        groups = {ep.group for ep in dist.entry_points}
                        if {"console_scripts", "gui_scripts"} & groups:
                            # stick them first so any more specific requirement
                            # overrides it
                            deps.insert(0, Requirement('setuptools'))
                # add requires/recommends based on egg/dist metadata
                for dep in deps:
                    # Even if we're requiring `foo[bar]`, also require `foo`
                    # to be safe, and to make it discoverable through
                    # `repoquery --whatrequires`
                    extras_suffixes = [""]
                    if args.require_extras_subpackages and dep.extras:
                        # A dependency can have more than one extras,
                        # i.e. foo[bar,baz], so let's go through all of them
                        extras_suffixes += [f"[{e.lower()}]" for e in dep.extras]

                    for extras_suffix in extras_suffixes:
                        if normalized_names_require_pep503:
                            dep_normalized_name = dep.normalized_name
                        else:
                            dep_normalized_name = dep.legacy_normalized_name

                        if args.legacy:
                            name = namespace.format('pythonegg({})({})').format(pyver_major, dep.legacy_normalized_name)
                        else:
                            if args.majorver_only:
                                name = namespace.format('python{}dist({}{})').format(pyver_major, dep_normalized_name, extras_suffix)
                            else:
                                name = namespace.format('python{}dist({}{})').format(dist.py_version, dep_normalized_name, extras_suffix)

                        if dep.marker and not args.recommends and not extras_subpackage:
                            if not dep.marker.evaluate(get_marker_env(dist, '')):
                                continue

                        if name not in py_deps:
                            py_deps[name] = []
                        for spec in dep.specifier:
                            if (spec.operator, spec.version) not in py_deps[name]:
                                py_deps[name].append((spec.operator, spec.version))

            # Unused, for automatic sub-package generation based on 'extras' from egg/dist metadata
            # TODO: implement in rpm later, or...?
            if args.extras:
                print(dist.extras)
                for extra in dist.extras:
                    print('%%package\textras-{}'.format(extra))
                    print('Summary:\t{} extra for {} python package'.format(extra, dist.legacy_normalized_name))
                    print('Group:\t\tDevelopment/Python')
                    for dep in dist.requirements_for_extra(extra):
                        for spec in dep.specifier:
                            if spec.operator == '!=':
                                print('Conflicts:\t{} {} {}'.format(dep.legacy_normalized_name, '==', spec.version))
                            else:
                                print('Requires:\t{} {} {}'.format(dep.legacy_normalized_name, spec.operator, spec.version))
                    print('%%description\t{}'.format(extra))
                    print('{} extra for {} python package'.format(extra, dist.legacy_normalized_name))
                    print('%%files\t\textras-{}\n'.format(extra))
            if args.conflicts:
                # Should we really add conflicts for extras?
                # Creating a meta package per extra with recommends on, which has
                # the requires/conflicts in stead might be a better solution...
                for dep in dist.requirements:
                    for spec in dep.specifier:
                        if spec.operator == '!=':
                            if dep.legacy_normalized_name not in py_deps:
                                py_deps[dep.legacy_normalized_name] = []
                            spec = ('==', spec.version)
                            if spec not in py_deps[dep.legacy_normalized_name]:
                                py_deps[dep.legacy_normalized_name].append(spec)

    for name in sorted(py_deps):
        if py_deps[name]:
            # Print out versioned provides, requires, recommends, conflicts
            spec_list = []
            for spec in py_deps[name]:
                spec_list.append(convert(name, spec[0], spec[1]))
            if len(spec_list) == 1:
                print(spec_list[0])
            else:
                # Sort spec_list so that the results can be tested easily
                print('({})'.format(' with '.join(sorted(spec_list))))
        else:
            # Print out unversioned provides, requires, recommends, conflicts
            print(name)


if __name__ == "__main__":
    """To allow this script to be importable (and its classes/functions
       reused), actions are performed only when run as a main script."""
    try:
        main()
    except Exception as exc:
        print("*** PYTHONDISTDEPS_GENERATORS_FAILED ***", flush=True)
        raise RuntimeError("Error: pythondistdeps.py generator encountered an unhandled exception and was terminated.") from exc
