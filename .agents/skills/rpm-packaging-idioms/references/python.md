# Python packaging idioms

Source: [Fedora Python Packaging Guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/)
(cite this URL; § names below are its section headings). Local provider:
[pyproject-rpm-macros README](../../../../specs/p/pyproject-rpm-macros/README.md) and
[macros.pyproject](../../../../specs/p/pyproject-rpm-macros/macros.pyproject).

## Canonical shape (pure-Python library)

```spec
Name:           python-foo
Version:        1.2.3
Release:        %autorelease
Summary:        ...
License:        MIT
URL:            https://github.com/org/foo
Source:         %{url}/archive/v%{version}/foo-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel

%global _description %{expand:
...}
%description %_description

%package -n python3-foo
Summary:        %{summary}
%description -n python3-foo %_description

%prep
%autosetup -p1 -n foo-%{version}

%generate_buildrequires
%pyproject_buildrequires -t        # or -x test / -g test; plain if no test deps

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l foo       # importable module name(s), never '*'

%check
%pytest                            # or %tox; at minimum %pyproject_check_import

%files -n python3-foo -f %{pyproject_files}
%doc README.md
%{_bindir}/foo                     # executables/docs are listed explicitly

%changelog
%autochangelog
```

Find live examples: `grep -l '%pyproject_wheel' specs/*/python-*/*.spec | head`.

## Anti-patterns

| Seen in spec | Fix | Level (§) |
| --- | --- | --- |
| No `BuildRequires: python3-devel` | Add it explicitly | MUST (Dependencies) |
| Manual BRs for pip/setuptools/wheel/build backend; no `%generate_buildrequires` | `%pyproject_buildrequires` | SHOULD (Automatically generated dependencies) |
| `%py3_build` / `%py3_install` / `setup.py build/install` | `%pyproject_wheel` / `%pyproject_install` (legacy macros are deprecated; fail if no `setup.py`) | MUST for new packages (intro: legacy guidelines) |
| `pip install` / `pip3 wheel` called directly | pyproject macros (offline, no-deps, RECORD handling) | MUST NOT fetch from network (main page `#_build_time_network_access`); legacy-guideline MUST NOT for new packages |
| Hardcoded `/usr/lib/python3.X/site-packages` | `%{python3_sitelib}` / `%{python3_sitearch}`, or `%files -f %{pyproject_files}` | MUST (Mandatory macros) |
| `%{python3_sitelib}/*`, `%pyproject_save_files '*'`/`+auto` | List the importable module(s) | SHOULD NOT (Explicit lists) |
| Owning `%{python3_sitelib}/__pycache__` | Don't | MUST NOT (Explicit lists) |
| Missing `*.dist-info` in payload | Keep metadata (pyproject_save_files handles it) | MUST (Dist-info metadata) |
| Pure Python without `BuildArch: noarch` | Add it | warning: archful output, empty debuginfo (Example spec file) |
| Library named `foo` / binary not `python3-foo` | SRPM `python-foo`, binary `python3-foo` (apps may keep app name) | MUST (Library naming) |
| `Requires: python3`, manual `Requires:` for deps in metadata | Remove; generator emits them (fix metadata via patch if wrong) | SHOULD NOT; runtime generator MUST be used (Dependencies, Automatically generated dependencies) |
| Manual `Provides: python-foo` / `python3dist(foo)` | `%py_provides` only if needed; generated otherwise | SHOULD NOT add manually (Provides) |
| No `%check`, or tests disabled wholesale | Run upstream tests (`%pytest`/`%tox`); if impossible, `%pyproject_check_import` | SHOULD run tests; import smoke test MUST; MUST NOT disable whole suite to fix a build (Tests) |
| Linters (flake8/black/mypy/pylint/coverage) in `%check` | Drop them and their BRs | SHOULD NOT (Linters) |
| Shebang `#!/usr/bin/env python3` installed | `%{python3}` (pyproject macros fix this) | MUST (Shebangs) |
| Cython-generated `.c` shipped in sources used as-is | Delete in `%prep`, regenerate | MUST (Using Cython) |
| Git-forge tarball + setuptools_scm/hatch-vcs | Set `SETUPTOOLS_SCM_PRETEND_VERSION=%{version}` in `%generate_buildrequires` and `%build`, or use the sdist (`%{pypi_source}`). GitHub archives are allowed (preferred if the sdist lacks tests). | correctness (Source files from PyPI) |

## Overlay / change hazards

- Changing `%pyproject_buildrequires` flags (`-x`, `-t`, `-e`, `-g`, `-R`) changes which deps are generated;
  removing `-t`/`-x test` while keeping `%pytest` breaks `%check`.
- Patching dependency bounds: use a patch to `pyproject.toml`/`setup.cfg` (or the provisional
  `%pyproject_patch_dependency`, see README). Never add manual `Requires:` to "fix" generated ones.
- `%pyproject_save_files` names must match what upstream installs; a renamed/added top-level module silently
  drops files or fails the build.
- Adding `%py_provides`/`Provides:` for names the generator already emits creates duplicates.
