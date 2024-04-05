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
import pathlib
import zipfile

from pyproject_requirements_txt import convert_requirements_txt
from pyproject_wheel import parse_config_settings_args


# Some valid Python version specifiers are not supported.
# Allow only the forms we know we can handle.
VERSION_RE = re.compile(r'[a-zA-Z0-9.-]+(\.\*)?')


class EndPass(Exception):
    """End current pass of generating requirements"""


# nb: we don't use functools.partial to be able to use pytest's capsys
# see https://github.com/pytest-dev/pytest/issues/8900
def print_err(*args, **kwargs):
    kwargs.setdefault('file', sys.stderr)
    print(*args, **kwargs)


try:
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

    def add(self, requirement_str, *, package_name=None, source=None):
        """Output a Python-style requirement string as RPM dep"""
        print_err(f'Handling {requirement_str} from {source}')

        try:
            requirement = Requirement(requirement_str)
        except InvalidRequirement:
            hint = guess_reason_for_invalid_requirement(requirement_str)
            message = f'Requirement {requirement_str!r} from {source} is invalid.'
            if hint:
                message += f' Hint: {hint}'
            raise ValueError(message)

        if requirement.url:
            print_err(
                f'WARNING: Simplifying {requirement_str!r} to {requirement.name!r}.'
            )

        name = canonicalize_name(requirement.name)
        if (requirement.marker is not None and
                not self.evaluate_all_environments(requirement)):
            print_err(f'Ignoring alien requirement:', requirement_str)
            self.ignored_alien_requirements.append(requirement_str)
            return

        # Handle self-referencing requirements
        if package_name and canonicalize_name(package_name) == name:
            # Self-referential extras need to be handled specially
            if requirement.extras:
                if not (requirement.extras <= self.extras):  # only handle it if needed
                    # let all further requirements know we want those extras
                    self.add_extras(*requirement.extras)
                    # re-add all of the alien requirements ignored in the past
                    # they might no longer be alien now
                    self.readd_ignored_alien_requirements(package_name=package_name)
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


def get_backend(requirements):
    try:
        f = open('pyproject.toml', 'rb')
    except FileNotFoundError:
        pyproject_data = {}
    else:
        with f:
            pyproject_data = toml_load(f)

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
        # PEP 517 doesn't mandate depending on wheel when the default backend is used.
        # Historically, it used to be assumed as necessary, but later it turned out to be wrong.
        # See the removal in pip and build:
        #   https://github.com/pypa/pip/pull/12449
        #   https://github.com/pypa/build/pull/716
        # However, the requirement *will* be generated by setuptools anyway
        # as part of get_requires_for_build_wheel().
        # So we might as well keep it to skip one redundant step.
        requirements.add('wheel', source='default build backend')

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
        new_reqs = get_requires(config_settings=requirements.config_settings)
        requirements.extend(new_reqs, source='get_requires_for_build_wheel')
        requirements.check(source='get_requires_for_build_wheel')


def parse_metadata_file(metadata_file):
    return email.parser.Parser().parse(metadata_file, headersonly=True)


def requires_from_parsed_metadata_file(message):
    return {k: message.get_all(k, ()) for k in ('Requires', 'Requires-Dist')}


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
            'Use the provisional -w flag to build the wheel and parse the metadata from it, '
            'or use the -R flag not to generate runtime dependencies.'
        )
    dir_basename = prepare_metadata('.', config_settings=requirements.config_settings)
    with open(dir_basename + '/METADATA') as metadata_file:
        name, requires = package_name_and_requires_from_metadata_file(metadata_file)
        for key, req in requires.items():
            requirements.extend(req,
                                package_name=name,
                                source=f'hook generated metadata: {key} ({name})')


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
                    for key, req in requires.items():
                        requirements.extend(req,
                                            package_name=name,
                                            source=f'built wheel metadata: {key} ({name})')
                break
        else:
            raise RuntimeError('Could not find *.dist-info/METADATA in built wheel.')


def generate_run_requirements(backend, requirements, *, build_wheel, wheeldir):
    if build_wheel:
        generate_run_requirements_wheel(backend, requirements, wheeldir)
    else:
        generate_run_requirements_hook(backend, requirements)


def generate_tox_requirements(toxenv, requirements):
    toxenv = ','.join(toxenv)
    requirements.add('tox-current-env >= 0.0.6', source='tox itself')
    requirements.check(source='tox itself')
    with tempfile.NamedTemporaryFile('r') as deps, \
        tempfile.NamedTemporaryFile('r') as extras, \
            tempfile.NamedTemporaryFile('r') as provision:
        r = subprocess.run(
            [sys.executable, '-m', 'tox',
             '--print-deps-to', deps.name,
             '--print-extras-to', extras.name,
             '--no-provision', provision.name,
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

        deplines = deps.read().splitlines()
        packages = convert_requirements_txt(deplines)
        requirements.add_extras(*extras.read().splitlines())
        requirements.extend(packages,
                            source=f'tox --print-deps-only: {toxenv}')


def python3dist(name, op=None, version=None, python3_pkgversion="3"):
    prefix = f"python{python3_pkgversion}dist"

    if op is None:
        if version is not None:
            raise AssertionError('op and version go together')
        return f'{prefix}({name})'
    else:
        return f'{prefix}({name}) {op} {version}'


def generate_requires(
    *, include_runtime=False, build_wheel=False, wheeldir=None, toxenv=None, extras=None,
    get_installed_version=importlib.metadata.version,  # for dep injection
    generate_extras=False, python3_pkgversion="3", requirement_files=None, use_build_system=True,
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

    try:
        if (include_runtime or toxenv) and not use_build_system:
            raise ValueError('-N option cannot be used in combination with -r, -e, -t, -x options')
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
        if toxenv:
            include_runtime = True
            generate_tox_requirements(toxenv, requirements)
        if include_runtime:
            generate_run_requirements(backend, requirements, build_wheel=build_wheel, wheeldir=wheeldir)
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
        '-p', '--python3_pkgversion', metavar='PYTHON3_PKGVERSION',
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
              '(useful for build backends without the prepare_metadata_for_build_wheel hook)'),
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
            generate_extras=args.generate_extras,
            python3_pkgversion=args.python3_pkgversion,
            requirement_files=args.requirement_files,
            use_build_system=args.use_build_system,
            output=args.output,
            config_settings=parse_config_settings_args(args.config_settings),
        )
    except Exception:
        # Log the traceback explicitly (it's useful debug info)
        traceback.print_exc()
        exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])
