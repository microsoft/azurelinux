import glob
import io
import os
import sys
import importlib.metadata
import argparse
import traceback
import json
import subprocess
import re
import tempfile
import email.parser
import functools
import pathlib
import zipfile

from pyproject_requirements_txt import convert_requirements_txt
from pyproject_wheel import parse_config_settings_args


# Some valid Python version specifiers are not supported.
# Allow only the forms we know we can handle.
VERSION_RE = re.compile(r'[a-zA-Z0-9.-]+(\.\*)?')

# To avoid breakage on Fedora 40-42,
# we don't assert tox configuration there.
# This can be removed when Fedora 42 goes EOL.
# Note that %tox still uses --assert-config
# because %tox without config is dangerous (false sense of tests).
# Running %pyproject_buildrequires -t/-e without tox config is wrong, but not dangerous.
FEDORA = int(os.getenv('FEDORA') or 0)
TOX_ASSERT_CONFIG_OPTS = () if 40 <= FEDORA < 43 else ('--assert-config',)


class EndPass(Exception):
    """End current pass of generating requirements"""


# nb: we don't use functools.partial to be able to use pytest's capsys
# see https://github.com/pytest-dev/pytest/issues/8900
def print_err(*args, **kwargs):
    kwargs.setdefault('file', sys.stderr)
    print(*args, **kwargs)


try:
    from packaging.markers import Marker
    from packaging.requirements import Requirement, InvalidRequirement
    from packaging.utils import canonicalize_name
except ImportError as e:
    print_err('Import error:', e)
    # already echoed by the %pyproject_buildrequires macro
    sys.exit(0)

# uses packaging, needs to be imported after packaging is verified to be present
from pyproject_convert import convert


def guess_reason_for_invalid_requirement(requirement_str):
    if ':' in requirement_str:
        message = (
            'It might be an URL. '
            '%pyproject_buildrequires cannot handle all URL-based requirements. '
            'Add PackageName@ (see PEP 508) to the URL to at least require any version of PackageName.'
        )
        if '@' in requirement_str:
            message += ' (but note that URLs might not work well with other features)'
        return message
    if '/' in requirement_str:
        return (
            'It might be a local path. '
            '%pyproject_buildrequires cannot handle local paths as requirements. '
            'Use an URL with PackageName@ (see PEP 508) to at least require any version of PackageName.'
        )
    # No more ideas
    return None


class Requirements:
    """Requirement gatherer. The macro will eventually print out output_lines."""
    def __init__(self, get_installed_version, extras=None,
                 generate_extras=False, python3_pkgversion='3', config_settings=None):
        self.get_installed_version = get_installed_version
        self.output_lines = []
        self.extras = set()

        if extras:
            for extra in extras:
                self.add_extras(*extra.split(','))

        self.missing_requirements = False
        self.ignored_alien_requirements = []

        self.generate_extras = generate_extras
        self.python3_pkgversion = python3_pkgversion
        self.config_settings = config_settings

        self.package_name = None

    def add_extras(self, *extras):
        self.extras |= set(e.strip() for e in extras)

    @property
    def marker_envs(self):
        if self.extras:
            return [{'extra': e} for e in sorted(self.extras)]
        return [{'extra': ''}]

    def evaluate_all_environments(self, requirement):
        for marker_env in self.marker_envs:
            if requirement.marker.evaluate(environment=marker_env):
                return True
        return False

    def set_package_name(self, name):
        canonical_name = canonicalize_name(name)
        if self.package_name is None:
            self.package_name = canonical_name
        else:
            # This really shouldn't happen, but it's better to be safe than sorry
            if canonical_name != self.package_name:
                raise ValueError(f'Package name mismatch: {canonical_name} != {self.package_name}')

    def add(self, requirement, *, source=None, extra=None):
        """Output a Python-style requirement string as RPM dep"""

        requirement_str = str(requirement)
        print_err(f'Handling {requirement_str} from {source}')

        # requirements read initially from the metadata are strings
        # further on we work with them as Requirement instances
        if not isinstance(requirement, Requirement):
            try:
                requirement = Requirement(requirement)
            except InvalidRequirement:
                hint = guess_reason_for_invalid_requirement(requirement)
                message = f'Requirement {requirement!r} from {source} is invalid.'
                if hint:
                    message += f' Hint: {hint}'
                raise ValueError(message)

        if requirement.url:
            print_err(
                f'WARNING: Simplifying {requirement_str!r} to {requirement.name!r}.'
            )

        name = canonicalize_name(requirement.name)

        if extra is not None:
            extra_str = f'extra == "{extra}"'
            if requirement.marker is not None:
                extra_str = f'({requirement.marker}) and {extra_str}'
            requirement.marker = Marker(extra_str)

        if (requirement.marker is not None and
                not self.evaluate_all_environments(requirement)):
            print_err(f'Ignoring alien requirement:', requirement_str)
            self.ignored_alien_requirements.append(requirement)
            return

        # Handle self-referencing requirements
        if self.package_name and self.package_name == name:
            # Self-referential extras need to be handled specially
            if requirement.extras:
                if not (requirement.extras <= self.extras):  # only handle it if needed
                    # let all further requirements know we want those extras
                    self.add_extras(*requirement.extras)
                    # re-add all of the alien requirements ignored in the past
                    # they might no longer be alien now
                    self.readd_ignored_alien_requirements()
            else:
                print_err(f'Ignoring self-referential requirement without extras:', requirement_str)
            return

        # We need to always accept pre-releases as satisfying the requirement
        # Otherwise e.g. installed cffi version 1.15.0rc2 won't even satisfy the requirement for "cffi"
        # https://bugzilla.redhat.com/show_bug.cgi?id=2014639#c3
        requirement.specifier.prereleases = True

        try:
            # TODO: check if requirements with extras are satisfied
            installed = self.get_installed_version(requirement.name)
        except importlib.metadata.PackageNotFoundError:
            print_err(f'Requirement not satisfied: {requirement_str}')
            installed = None
        if installed and installed in requirement.specifier:
            print_err(f'Requirement satisfied: {requirement_str}')
            print_err(f'   (installed: {requirement.name} {installed})')
            if requirement.extras:
                print_err(f'   (extras are currently not checked)')
        else:
            self.missing_requirements = True

        if self.generate_extras:
            extra_names = [f'{name}[{extra.lower()}]' for extra in sorted(requirement.extras)]
        else:
            extra_names = []

        for name in [name] + extra_names:
            together = []
            for specifier in sorted(
                requirement.specifier,
                key=lambda s: (s.operator, s.version),
            ):
                if not VERSION_RE.fullmatch(str(specifier.version)):
                    raise ValueError(
                        f'Unknown character in version: {specifier.version}. '
                        + '(This might be a bug in pyproject-rpm-macros.)',
                    )
                together.append(convert(python3dist(name, python3_pkgversion=self.python3_pkgversion),
                                        specifier.operator, specifier.version))
            if len(together) == 0:
                dep = python3dist(name, python3_pkgversion=self.python3_pkgversion)
                self.output_lines.append(dep)
            elif len(together) == 1:
                self.output_lines.append(together[0])
            else:
                self.output_lines.append(f"({' with '.join(together)})")

    def check(self, *, source=None):
        """End current pass if any unsatisfied dependencies were output"""
        if self.missing_requirements:
            print_err(f'Exiting dependency generation pass: {source}')
            raise EndPass(source)

    def extend(self, requirement_strs, **kwargs):
        """add() several requirements"""
        for req_str in requirement_strs:
            self.add(req_str, **kwargs)

    def readd_ignored_alien_requirements(self, **kwargs):
        """add() previously ignored alien requirements again."""
        requirements, self.ignored_alien_requirements = self.ignored_alien_requirements, []
        kwargs.setdefault('source', 'Previously ignored alien requirements')
        self.extend(requirements, **kwargs)


def toml_load(opened_binary_file):
    try:
        # tomllib is in the standard library since 3.11.0b1
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib
        except ImportError as e:
            print_err('Import error:', e)
            # already echoed by the %pyproject_buildrequires macro
            sys.exit(0)
    return tomllib.load(opened_binary_file)


@functools.cache
def load_pyproject():
    try:
        f = open('pyproject.toml', 'rb')
    except FileNotFoundError:
        pyproject_data = {}
    else:
        with f:
            pyproject_data = toml_load(f)
    return pyproject_data


def get_backend(requirements):
    pyproject_data = load_pyproject()

    buildsystem_data = pyproject_data.get('build-system', {})
    requirements.extend(
        buildsystem_data.get('requires', ()),
        source='build-system.requires',
    )

    backend_name = buildsystem_data.get('build-backend')
    if not backend_name:
        # https://www.python.org/dev/peps/pep-0517/:
        # If the pyproject.toml file is absent, or the build-backend key is
        # missing, the source tree is not using this specification, and tools
        # should revert to the legacy behaviour of running setup.py
        # (either directly, or by implicitly invoking the [following] backend).
        # If setup.py is also not present program will mimick pip's behavior
        # and end with an error.
        if not os.path.exists('setup.py'):
            raise FileNotFoundError('File "setup.py" not found for legacy project.')
        backend_name = 'setuptools.build_meta:__legacy__'

        # Note: For projects without pyproject.toml, this was already echoed
        # by the %pyproject_buildrequires macro, but this also handles cases
        # with pyproject.toml without a specified build backend.
        # If the default requirements change, also change them in the macro!
        requirements.add('setuptools >= 40.8', source='default build backend')

    requirements.check(source='build backend')

    backend_path = buildsystem_data.get('backend-path')
    if backend_path:
        # PEP 517 example shows the path as a list, but some projects don't follow that
        if isinstance(backend_path, str):
            backend_path = [backend_path]
        sys.path = backend_path + sys.path

    module_name, _, object_name = backend_name.partition(":")
    backend_module = importlib.import_module(module_name)

    if object_name:
        return getattr(backend_module, object_name)

    return backend_module


def generate_build_requirements(backend, requirements):
    get_requires = getattr(backend, 'get_requires_for_build_wheel', None)
    if get_requires:
        new_reqs = get_requires(requirements.config_settings)
        requirements.extend(new_reqs, source='get_requires_for_build_wheel')
        requirements.check(source='get_requires_for_build_wheel')


def parse_metadata_file(metadata_file):
    return email.parser.Parser().parse(metadata_file, headersonly=True)


def requires_from_parsed_metadata_file(message):
    return {k: message.get_all(k, ()) for k in ('Requires-Dist',)}


def package_name_from_parsed_metadata_file(message):
    return message.get('name')


def package_name_and_requires_from_metadata_file(metadata_file):
    message = parse_metadata_file(metadata_file)
    package_name = package_name_from_parsed_metadata_file(message)
    requires = requires_from_parsed_metadata_file(message)
    return package_name, requires


def generate_run_requirements_hook(backend, requirements):
    hook_name = 'prepare_metadata_for_build_wheel'
    prepare_metadata = getattr(backend, hook_name, None)
    if not prepare_metadata:
        raise ValueError(
            'The build backend cannot provide build metadata '
            '(incl. runtime requirements) before build. '
            'If the dependencies are specified in the pyproject.toml [project] '
            'table, you can use the -p flag to read them. '
            'Alternatively, use the -R flag not to generate runtime dependencies.'
        )
    dir_basename = prepare_metadata('.', requirements.config_settings)
    with open(dir_basename + '/METADATA') as metadata_file:
        name, requires = package_name_and_requires_from_metadata_file(metadata_file)
        requirements.set_package_name(name)
        for key, req in requires.items():
            requirements.extend(req,
                                source=f'hook generated metadata: {key} ({requirements.package_name})')


def find_built_wheel(wheeldir):
    wheels = glob.glob(os.path.join(wheeldir, '*.whl'))
    if not wheels:
        return None
    if len(wheels) > 1:
        raise RuntimeError('Found multiple wheels in %{_pyproject_wheeldir}, '
                           'this is not supported with %pyproject_buildrequires -w.')
    return wheels[0]


def generate_run_requirements_wheel(backend, requirements, wheeldir):
    # Reuse the wheel from the previous round of %pyproject_buildrequires (if it exists)
    wheel = find_built_wheel(wheeldir)
    if not wheel:
        # pip is already echoed from the macro
        # but we need to explicitly restart if has not yet been installed
        # see https://bugzilla.redhat.com/2169855
        requirements.add('pip >= 19', source='%pyproject_buildrequires -w')
        requirements.check(source='%pyproject_buildrequires -w')
        import pyproject_wheel
        returncode = pyproject_wheel.build_wheel(
            wheeldir=wheeldir,
            stdout=sys.stderr,
            config_settings=requirements.config_settings,
        )
        if returncode != 0:
            raise RuntimeError('Failed to build the wheel for %pyproject_buildrequires -w.')
        wheel = find_built_wheel(wheeldir)
    if not wheel:
        raise RuntimeError('Cannot locate the built wheel for %pyproject_buildrequires -w.')

    print_err(f'Reading metadata from {wheel}')
    with zipfile.ZipFile(wheel) as wheelfile:
        for name in wheelfile.namelist():
            if name.count('/') == 1 and name.endswith('.dist-info/METADATA'):
                with io.TextIOWrapper(wheelfile.open(name), encoding='utf-8') as metadata_file:
                    name, requires = package_name_and_requires_from_metadata_file(metadata_file)
                    requirements.set_package_name(name)
                    for key, req in requires.items():
                        requirements.extend(req,
                                            source=f'built wheel metadata: {key} ({name})')
                break
        else:
            raise RuntimeError('Could not find *.dist-info/METADATA in built wheel.')


def generate_run_requirements_pyproject(requirements):
    pyproject_data = load_pyproject()

    if not (project_table := pyproject_data.get('project', {})):
        raise ValueError('Could not find the [project] table in pyproject.toml.')

    dynamic_fields = project_table.get('dynamic', [])
    if 'dependencies' in dynamic_fields or 'optional-dependencies' in dynamic_fields:
        raise ValueError('Could not read the dependencies or optional-dependencies '
            'from the [project] table in pyproject.toml, as the field is dynamic.')

    dependencies = project_table.get('dependencies', [])
    name = project_table.get('name')
    requirements.set_package_name(name)
    requirements.extend(dependencies,
                        source=f'pyproject.toml generated metadata: [dependencies] ({name})')

    optional_dependencies = project_table.get('optional-dependencies', {})
    for extra, dependencies in optional_dependencies.items():
        requirements.extend(dependencies,
                            source=f'pyproject.toml generated metadata: [optional-dependencies] {extra} ({name})',
                            extra=extra)


def generate_run_requirements(backend, requirements, *, build_wheel, read_pyproject_dependencies, wheeldir):
    if read_pyproject_dependencies:
        generate_run_requirements_pyproject(requirements)
    elif build_wheel:
        generate_run_requirements_wheel(backend, requirements, wheeldir)
    else:
        generate_run_requirements_hook(backend, requirements)


def generate_tox_requirements(toxenv, requirements):
    toxenv = ','.join(toxenv)
    requirements.add('tox-current-env >= 0.0.16', source='tox itself')
    requirements.check(source='tox itself')
    with tempfile.NamedTemporaryFile('r') as deps, \
        tempfile.NamedTemporaryFile('r') as extras, \
            tempfile.NamedTemporaryFile('r') as provision:
        r = subprocess.run(
            [sys.executable, '-m', 'tox',
             '--print-deps-to', deps.name,
             '--print-extras-to', extras.name,
             '--no-provision', provision.name,
             *TOX_ASSERT_CONFIG_OPTS,
             '-q', '-r', '-e', toxenv],
            check=False,
            encoding='utf-8',
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if r.stdout:
            print_err(r.stdout, end='')

        provision_content = provision.read()
        if provision_content and r.returncode != 0:
            provision_requires = json.loads(provision_content)
            if provision_requires.get('minversion') is not None:
                requirements.add(f'tox >= {provision_requires["minversion"]}',
                                 source='tox provision (minversion)')
            if 'requires' in provision_requires:
                requirements.extend(provision_requires["requires"],
                                    source='tox provision (requires)')
            requirements.check(source='tox provision')  # this terminates the script
            raise RuntimeError(
                'Dependencies requested by tox provisioning appear installed, '
                'but tox disagreed.')
        else:
            r.check_returncode()

        tox_extras = {e for e in extras.read().splitlines() if e}
        if not (tox_extras <= requirements.extras):
            requirements.add_extras(*tox_extras)
            requirements.readd_ignored_alien_requirements(source=f'tox added extras: {toxenv}')

        deplines = deps.read().splitlines()
        packages = convert_requirements_txt(deplines)
        requirements.extend(packages,
                            source=f'tox --print-deps-only: {toxenv}')


def tox_dependency_groups(toxenv):
    # We call this command separately instead of folding it into the previous one
    # becasue --print-dependency-groups-to only works with tox 4.22+ and tox-current-env 0.0.14+.
    # We handle failure gracefully: upstreams using dependency_groups should require tox >= 4.22.
    toxenv = ','.join(toxenv)
    with tempfile.NamedTemporaryFile('r') as groups:
        r = subprocess.run(
            [sys.executable, '-m', 'tox',
             '--print-dependency-groups-to', groups.name,
             '-q', '-e', toxenv],
            check=False,
            encoding='utf-8',
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if r.returncode == 0:
            if r.stdout:
                print_err(r.stdout, end='')
            if output := groups.read().strip():
                return output.splitlines()
    return []


def generate_dependency_groups(requested_groups, requirements):
    """Adapted from https://peps.python.org/pep-0735/#reference-implementation (public domain)"""
    from collections import defaultdict

    def _normalize_name(name: str) -> str:
        return re.sub(r"[-_.]+", "-", name).lower()

    def _normalize_group_names(dependency_groups: dict) -> dict:
        original_names = defaultdict(list)
        normalized_groups = {}

        for group_name, value in dependency_groups.items():
            normed_group_name = _normalize_name(group_name)
            original_names[normed_group_name].append(group_name)
            normalized_groups[normed_group_name] = value

        errors = []
        for normed_name, names in original_names.items():
            if len(names) > 1:
                errors.append(f"{normed_name} ({', '.join(names)})")
        if errors:
            raise ValueError(f"Duplicate dependency group names: {', '.join(errors)}")

        return normalized_groups

    def _resolve_dependency_group(
        dependency_groups: dict, group: str, past_groups: tuple[str, ...] = ()
    ) -> list[str]:
        if group in past_groups:
            raise ValueError(f"Cyclic dependency group include: {group} -> {past_groups}")

        if group not in dependency_groups:
            raise LookupError(f"Dependency group '{group}' not found")

        raw_group = dependency_groups[group]
        if not isinstance(raw_group, list):
            raise ValueError(f"Dependency group '{group}' is not a list")

        realized_group = []
        for item in raw_group:
            if isinstance(item, str):
                realized_group.append(item)
            elif isinstance(item, dict):
                if tuple(item.keys()) != ("include-group",):
                    raise ValueError(f"Invalid dependency group item: {item}")

                include_group = _normalize_name(next(iter(item.values())))
                realized_group.extend(
                    _resolve_dependency_group(
                        dependency_groups, include_group, past_groups + (group,)
                    )
                )
            else:
                raise ValueError(f"Invalid dependency group item: {item}")

        return realized_group

    def resolve(dependency_groups: dict, group: str) -> list[str]:
        if not isinstance(dependency_groups, dict):
            raise TypeError("Dependency Groups table is not a dict")
        return _resolve_dependency_group(dependency_groups, _normalize_name(group))

    pyproject_data = load_pyproject()
    dependency_groups_raw = pyproject_data.get("dependency-groups", {})
    dependency_groups = _normalize_group_names(dependency_groups_raw)

    for group_names in requested_groups:
        for group_name in group_names.split(","):
            requirements.extend(
                resolve(dependency_groups, group_name),
                source=f"Dependency group {group_name}",
            )


def python3dist(name, op=None, version=None, python3_pkgversion="3"):
    prefix = f"python{python3_pkgversion}dist"

    if op is None:
        if version is not None:
            raise AssertionError('op and version go together')
        return f'{prefix}({name})'
    else:
        return f'{prefix}({name}) {op} {version}'


def generate_requires(
    *, include_runtime=False, build_wheel=False, wheeldir=None, toxenv=None, extras=None, dependency_groups=None,
    get_installed_version=importlib.metadata.version,  # for dep injection
    generate_extras=False, python3_pkgversion="3", requirement_files=None, use_build_system=True,
    read_pyproject_dependencies=False,
    output, config_settings=None,
):
    """Generate the BuildRequires for the project in the current directory

    The generated BuildRequires are written to the provided output.

    This is the main Python entry point.
    """
    requirements = Requirements(
        get_installed_version, extras=extras or [],
        generate_extras=generate_extras,
        python3_pkgversion=python3_pkgversion,
        config_settings=config_settings,
    )

    dependency_groups = dependency_groups or []
    try:
        if (include_runtime or toxenv or read_pyproject_dependencies) and not use_build_system:
            raise ValueError('-N option cannot be used in combination with -r, -e, -t, -x, -p options')
        if requirement_files:
            for req_file in requirement_files:
                requirements.extend(
                    convert_requirements_txt(req_file, pathlib.Path(req_file.name)),
                    source=f'requirements file {req_file.name}'
                )
            requirements.check(source='all requirements files')
        if use_build_system:
            backend = get_backend(requirements)
            generate_build_requirements(backend, requirements)
        if include_runtime or toxenv:
            generate_run_requirements(backend, requirements, build_wheel=build_wheel,
                read_pyproject_dependencies=read_pyproject_dependencies, wheeldir=wheeldir)
        if toxenv:
            generate_tox_requirements(toxenv, requirements)
            dependency_groups.extend(tox_dependency_groups(toxenv))
        if dependency_groups:
            generate_dependency_groups(dependency_groups, requirements)
    except EndPass:
        return
    finally:
        output.write_text(os.linesep.join(requirements.output_lines) + os.linesep)


def main(argv):
    parser = argparse.ArgumentParser(
        description='Generate BuildRequires for a Python project.',
        prog='%pyproject_buildrequires',
        add_help=False,
    )
    parser.add_argument(
        '--help', action='help',
        default=argparse.SUPPRESS,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        '-r', '--runtime', action='store_true', default=True,
        help=argparse.SUPPRESS,  # Generate run-time requirements (backwards-compatibility only)
    )
    parser.add_argument(
        '--generate-extras', action='store_true',
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        '--python3_pkgversion', metavar='PYTHON3_PKGVERSION',
        default="3", help=argparse.SUPPRESS,
    )
    parser.add_argument(
        '--output', type=pathlib.Path, required=True, help=argparse.SUPPRESS,
    )
    parser.add_argument(
        '--wheeldir', metavar='PATH', default=None,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        '-x', '--extras', metavar='EXTRAS', action='append',
        help='comma separated list of "extras" for runtime requirements '
             '(e.g. -x testing,feature-x) (implies --runtime, can be repeated)',
    )
    parser.add_argument(
        '-g', '--dependency-groups', metavar='GROUPS', action='append',
        help='comma separated list of dependency groups (PEP 735) for requirements '
             '(e.g. -g tests,docs) (can be repeated)',
    )
    parser.add_argument(
        '-t', '--tox', action='store_true',
        help=('generate test tequirements from tox environment '
              '(implies --runtime)'),
    )
    parser.add_argument(
        '-e', '--toxenv', metavar='TOXENVS', action='append',
        help=('specify tox environments (comma separated and/or repeated)'
              '(implies --tox)'),
    )
    parser.add_argument(
        '-w', '--wheel', action='store_true', default=False,
        help=('Generate run-time requirements by building the wheel '
              '(useful for build backends without the prepare_metadata_for_build_wheel hook, deprecated)'),
    )
    parser.add_argument(
        '-p', '--read-pyproject-dependencies', action='store_true', default=False,
        help=('Generate dependencies from [project] table of pyproject.toml '
              'instead of calling prepare_metadata_for_build_wheel hook)'),
    )
    parser.add_argument(
        '-R', '--no-runtime', action='store_false', dest='runtime',
        help="Don't generate run-time requirements (implied by -N)",
    )
    parser.add_argument(
        '-N', '--no-use-build-system', dest='use_build_system',
        action='store_false', help='Use -N to indicate that project does not use any build system',
    )
    parser.add_argument(
        'requirement_files', nargs='*', type=argparse.FileType('r'),
        metavar='REQUIREMENTS.TXT',
        help=('Add buildrequires from file'),
    )
    parser.add_argument(
        '-C',
        dest='config_settings',
        action='append',
        help='Configuration settings to pass to the PEP 517 backend',
    )

    args = parser.parse_args(argv)

    if not args.use_build_system:
        args.runtime = False

    if args.wheel:
        if not args.wheeldir:
            raise ValueError('--wheeldir must be set when -w.')

    if args.toxenv:
        args.tox = True

    if args.tox:
        args.runtime = True
        if not args.toxenv:
            _default = f'py{sys.version_info.major}{sys.version_info.minor}'
            args.toxenv = [os.getenv('RPM_TOXENV', _default)]

    if args.extras:
        args.runtime = True

    try:
        generate_requires(
            include_runtime=args.runtime,
            build_wheel=args.wheel,
            wheeldir=args.wheeldir,
            toxenv=args.toxenv,
            extras=args.extras,
            dependency_groups=args.dependency_groups,
            generate_extras=args.generate_extras,
            python3_pkgversion=args.python3_pkgversion,
            requirement_files=args.requirement_files,
            use_build_system=args.use_build_system,
            read_pyproject_dependencies=args.read_pyproject_dependencies,
            output=args.output,
            config_settings=parse_config_settings_args(args.config_settings),
        )
    except Exception:
        # Log the traceback explicitly (it's useful debug info)
        traceback.print_exc()
        exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])
