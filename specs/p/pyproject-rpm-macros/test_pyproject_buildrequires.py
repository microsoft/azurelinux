from pathlib import Path
import importlib.metadata

import packaging.version
import pytest
import setuptools
import yaml

from pyproject_buildrequires import generate_requires, load_pyproject

SETUPTOOLS_VERSION = packaging.version.parse(setuptools.__version__)
SETUPTOOLS_60 = SETUPTOOLS_VERSION >= packaging.version.parse('60')

try:
    import tox
except ImportError:
    TOX_4_22 = False
else:
    TOX_VERSION = packaging.version.parse(tox.__version__)
    TOX_4_22 = TOX_VERSION >= packaging.version.parse('4.22')

testcases = {}
with Path(__file__).parent.joinpath('pyproject_buildrequires_testcases.yaml').open() as f:
    testcases = yaml.safe_load(f)


@pytest.fixture(autouse=True)
def clear_pyproject_data():
    """
    Clear pyproject data before each test.
    In reality we build one RPM package at a time, so we can keep the once-loaded
    pyproject.toml contents.
    When testing, the cached data would leak the once-loaded data to all the
    following test cases.
    """
    load_pyproject.cache_clear()


@pytest.mark.parametrize('case_name', testcases)
def test_data(case_name, capfd, tmp_path, monkeypatch):
    case = testcases[case_name]

    cwd = tmp_path.joinpath('cwd')
    cwd.mkdir()
    monkeypatch.chdir(cwd)
    wheeldir = cwd.joinpath('wheeldir')
    wheeldir.mkdir()
    output = tmp_path.joinpath('output.txt')

    if case.get('xfail'):
        pytest.xfail(case.get('xfail'))

    if case.get('skipif') and eval(case.get('skipif')):
        pytest.skip(case.get('skipif'))

    for filename in case:
        file_types = ('.toml', '.py', '.in', '.ini', '.txt', '.cfg')
        if filename.endswith(file_types):
            cwd.joinpath(filename).write_text(case[filename])

    for name, value in case.get('environ', {}).items():
        monkeypatch.setenv(name, value)

    def get_installed_version(dist_name):
        try:
            return str(case['installed'][dist_name])
        except (KeyError, TypeError):
            raise importlib.metadata.PackageNotFoundError(
                f'info not found for {dist_name}'
            )
    requirement_files = case.get('requirement_files', [])
    requirement_files = [open(f) for f in requirement_files]
    use_build_system = case.get('use_build_system', True)
    read_pyproject_dependencies = case.get('read_pyproject_dependencies', False)
    try:
        generate_requires(
            get_installed_version=get_installed_version,
            include_runtime=case.get('include_runtime', use_build_system),
            build_wheel=case.get('build_wheel', False),
            wheeldir=str(wheeldir),
            extras=case.get('extras', []),
            dependency_groups=case.get('dependency_groups', []),
            toxenv=case.get('toxenv', None),
            generate_extras=case.get('generate_extras', False),
            requirement_files=requirement_files,
            use_build_system=use_build_system,
            read_pyproject_dependencies=read_pyproject_dependencies,
            output=output,
            config_settings=case.get('config_settings'),
        )
    except SystemExit as e:
        assert e.code == case['result']
    except Exception as e:
        if 'except' not in case:
            raise
        assert type(e).__name__ == case['except']
    else:
        assert 0 == case['result']

        # this prevents us from accidentally writing "empty" tests
        # if we ever need to do that, we can remove the check or change it:
        assert 'expected' in case or 'stderr_contains' in case

        out, err = capfd.readouterr()
        dependencies = sorted(output.read_text().splitlines())

        if 'expected' in case:
            expected = case['expected']
            if isinstance(expected, list):
                # at least one of them needs to match
                assert dependencies in [sorted(e.splitlines()) for e in expected]
            else:
                assert dependencies == sorted(expected.splitlines())

        # stderr_contains may be a string or list of strings
        stderr_contains = case.get('stderr_contains')
        if stderr_contains is not None:
            if isinstance(stderr_contains, str):
                stderr_contains = [stderr_contains]
            for expected_substring in stderr_contains:
                assert expected_substring.format(**locals()) in err
    finally:
        for req in requirement_files:
            req.close()
