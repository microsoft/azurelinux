## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# Copyright (C) Fedora Project Authors
# SPDX-License-Identifier: MIT
# License text: https://spdx.org/licenses/MIT

%bcond tests 1
# Optional integration tests (no effect if tests are disabled)
%bcond numpy_tests 1
%bcond pandas_tests 1
%bcond inline_snapshot_tests 1

Name:           python-pydantic-core
Version:        2.41.5
Release:        %autorelease
Summary:        Core validation logic for pydantic written in rust

License:        MIT
URL:            https://github.com/pydantic/pydantic-core
Source:         %{url}/archive/v%{version}/pydantic-core-%{version}.tar.gz

BuildRequires:  python3-devel
BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  tomcli

%global _description %{expand:
The pydantic-core project provides the core validation logic for pydantic
written in Rust.}

%description %_description


%package -n python3-pydantic-core
Summary:        %{summary}
# (MIT OR Apache-2.0) AND Unicode-DFS-2016
# Apache-2.0 OR BSL-1.0
# Apache-2.0 OR MIT
# BSD-2-Clause OR Apache-2.0 OR MIT
# MIT
# MIT OR Apache-2.0
# Unicode-3.0
# Unlicense OR MIT
License:        %{shrink:
                (MIT OR Apache-2.0)
                AND MIT
                AND Unicode-3.0
                AND Unicode-DFS-2016
                AND (Apache-2.0 OR BSL-1.0)
                AND (BSD-2-Clause OR Apache-2.0 OR MIT)
                AND (Unlicense OR MIT)
                }

%description -n python3-pydantic-core %_description


%prep
%autosetup -p1 -n pydantic-core-%{version}

# Remove unused Cargo config that contains buildflags for Darwin
rm -v .cargo/config.toml

# Upstream tests with certain dependencies on x86_64 only (and only on certain
# Python interpreter versions) due to the limited availability of precompiled
# wheels on PyPI. We have no such limitations, except that python-pandas is not
# available on i686.
tomcli-set pyproject.toml lists replace 'dependency-groups.testing' \
    'pandas; *' 'pandas; platform_machine != "i686"'
tomcli-set pyproject.toml lists replace 'dependency-groups.testing' \
    'pytest-examples; *' 'pytest-examples'
tomcli-set pyproject.toml lists replace 'dependency-groups.testing' \
    'numpy; *' 'numpy'

# Use a regex to remove entries from the testing dependency group.
remove_from_testing() {
  tomcli-set pyproject.toml lists delitem --type regex \
      'dependency-groups.testing' "${1}"
}
# Remove coverage analysis, etc. from testing dependency group.
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters
remove_from_testing 'coverage\b.*'
# The pytest-examples plugin is possibly useful, but not packaged.
# The pytest-pretty plugin is purely cosmetic.
# The pytest-run-parallel plugin is possibly useful, but not packaged.
# The pytest-speed plugin is for benchmarking, which we do not need.
# The pytest-timeout plugin is not needed for downstream tests.
remove_from_testing 'pytest-(examples|pretty|run-parallel|speed|timeout)\b.*'
# We rely on the system timezone database, not on PyPI tzdata.
remove_from_testing 'tzdata\b.*'
# Handle conditional test dependencies.
%if %{without numpy_tests}
remove_from_testing 'numpy\b.*'
%endif
%if %{without pandas_tests}
remove_from_testing 'pandas\b.*'
%endif
%if %{without inline_snapshot_tests}
remove_from_testing 'inline-snapshot\b.*'
%endif

# Delete pytest addopts. We don't care about benchmarking.
tomcli-set pyproject.toml del 'tool.pytest.ini_options.addopts'
# Remove pytest timeout config. pytest-timeout is not needed for downstream tests.
tomcli-set pyproject.toml del 'tool.pytest.ini_options.timeout'
# Work around patched-out pytest-run-parallel plugin dependency (avoid
# "pytest.PytestUnknownMarkWarning: Unknown pytest.mark.thread_unsafe" error)
tomcli-set pyproject.toml list 'tool.pytest.ini_options.markers' \
    'thread_unsafe: mark as incompatible with patched-out pytest-run-parallel'

%cargo_prep

# Remove Windows-only dependencies
tomcli-set Cargo.toml lists delitem 'dependencies.pyo3.features' 'generate-import-lib'


%generate_buildrequires
%pyproject_buildrequires %{?with_tests:-g testing}
%cargo_generate_buildrequires


%build
%cargo_license_summary
%{cargo_license} > LICENSES.dependencies

%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l pydantic_core


%check
%pyproject_check_import
%if %{with tests}
ignore="${ignore-} --ignore=tests/benchmarks"
%if %{without inline_snapshot_tests}
ignore="${ignore-} --ignore=tests/validators/test_allow_partial.py"
%endif

# Due to patching out the pytest-timeout dependency:
warningsfilter="${warningsfilter-} -W ignore::pytest.PytestUnknownMarkWarning"

%pytest ${warningsfilter-} ${ignore-} -k "${k-}" -rs
%endif


%files -n python3-pydantic-core -f %{pyproject_files}
%doc README.md


%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 2.41.5-3
- Latest state for python-pydantic-core

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2.41.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Nov 06 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.41.5-1
- Update to 2.41.5

* Tue Oct 14 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.41.4-1
- Update to 2.41.4

* Tue Oct 14 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.41.3-1
- Update to 2.41.3, for Pydantic 2.12.1

* Wed Oct 08 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.41.1-1
- Update to 2.41.1

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.37.2-3
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.37.2-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Sun Jul 27 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.37.2-1
- Update to 2.37.2

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.35.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jun 21 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.35.1-1
- Update to 2.35.1 (fix RHBZ#2325425)

* Mon Jun 16 2025 Python Maint <python-maint@redhat.com> - 2.33.2-3
- Rebuilt for Python 3.14

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.33.2-2
- Bootstrap for Python 3.14

* Mon May 05 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.33.2-1
- Update to 2.33.2

* Sat Apr 12 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.33.1-1
- Update to 2.33.1
- Remove conditionals, workarounds, etc. for Fedora 42 and older

* Fri Apr 11 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.27.2-5
- Rebuilt with idna 1.x; no longer allow older idna versions

* Fri Apr 11 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.27.2-4
- Expect maturin to handle license files

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.27.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Dec 26 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.27.2-2
- Omit snapshot tests on EPEL10

* Wed Dec 18 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.27.2-1
- Update to 2.27.2

* Sat Nov 23 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.27.1-1
- Update to 2.27.1

* Thu Sep 26 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.23.4-2
- Fix automatic provides on Python extension due to SONAME

* Wed Sep 18 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.23.4-1
- Update to 2.23.4

* Tue Sep 10 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.23.3-1
- Update to 2.23.3

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jul 06 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.20.1-1
- Update to 2.20.1

* Tue Jun 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.20.0-1
- Update to 2.20.0

* Sat Jun 15 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.18.4-3
- Rebuilt with rust-jiter 0.4.2

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.18.4-2
- Rebuilt for Python 3.13

* Wed Jun 05 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.18.4-1
- Update to 2.18.4

* Wed May 29 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.18.3-1
- Update to 2.18.3

* Fri May 24 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.18.2-2
- Rebuild with Rust 1.78 to fix incomplete debuginfo and backtraces

* Wed Apr 24 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.18.2-1
- Update to 2.18.2

* Sat Apr 13 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.18.1-1
- Update to 2.18.1

* Sat Feb 24 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.16.3-1
- Update to 2.16.3.

* Mon Feb 05 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.16.2-1
- Update to 2.16.2.

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Dec 23 2023 Maxwell G <maxwell@gtmx.me> - 2.14.6-1
- Update to 2.14.6.

* Sat Nov 25 2023 Maxwell G <maxwell@gtmx.me> - 2.14.5-1
- Update to 2.14.5.

* Fri Sep 29 2023 Maxwell G <maxwell@gtmx.me> - 2.10.1-1
- Update to 2.10.1.

* Mon Jun 05 2023 Maxwell G <maxwell@gtmx.me> - 2.6.3-1
- Initial package. Closes rhbz#2238117.

## END: Generated by rpmautospec
