# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname anyio

%global common_description %{expand:
AnyIO is an asynchronous networking and concurrency library that works on top
of either asyncio or trio.  It implements trio-like structured concurrency (SC)
on top of asyncio, and works in harmony with the native SC of trio itself.}

Name:           python-%{srcname}
Version:        4.12.1
Release: 2%{?dist}
Summary:        Compatibility layer for multiple asynchronous event loop implementations
License:        MIT
URL:            https://github.com/agronholm/anyio
Source:         %{pypi_source %{srcname}}

BuildArch:      noarch

BuildRequires:  tomcli

%description %{common_description}


%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
# Sphinx-generated HTML documentation is not suitable for packaging; see
# https://bugzilla.redhat.com/show_bug.cgi?id=2006555 for discussion.
# We could perhaps generate PDF documentation as a substitute, but instead we
# simply drop the -doc subpackage.
Obsoletes:      python-%{srcname}-doc < 3.7.1-7


%description -n python3-%{srcname} %{common_description}


%pyproject_extras_subpkg -n python3-%{srcname} trio


%prep
%autosetup -n %{srcname}-%{version} -p1

# - Disable coverage test requirement
#   https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters
# - Drop test dependency on python3dist(truststore), not packaged
# - Drop test dependency on python3dist(uvloop), packaged but outdated and
#   FTBFS, https://bugzilla.redhat.com/show_bug.cgi?id=2307494,
#   https://bugzilla.redhat.com/show_bug.cgi?id=2341233
# = Drop test dependency on blockbuster; see
#   https://github.com/cbornet/blockbuster/issues/46 for why we would prefer
#   not to package it
tomcli set pyproject.toml lists delitem \
    dependency-groups.test '(blockbuster|coverage|truststore|uvloop)\b.*'


%generate_buildrequires
%pyproject_buildrequires -x trio -g test


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l %{srcname}


%check
# https://github.com/agronholm/anyio/pull/1020#issuecomment-3477923712
k="${k-}${k+ and }not (TestCapacityLimiter and test_bad_init_value[trio])"

%pytest -Wdefault -m "not network" -k "${k-}" -rsx -v


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst


%changelog
* Tue Jan 06 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 4.12.1-1
- Update to 4.12.1 (close RHBZ#2427391)

* Fri Dec 26 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 4.12.0-1
- Update to 4.12.0 (close RHBZ#2419146)

* Thu Nov 13 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 4.11.0-1
- Update to 4.11.0 (close RHBZ#2352829)

* Thu Nov 13 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 4.10.0-1
- Update to 4.10.0

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 4.8.0-7
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 4.8.0-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 4.8.0-4
- Rebuilt for Python 3.14

* Mon Apr 07 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 4.8.0-3
- Patch for Python 3.14.0a6 test failures (fixes RHBZ#2357902)

* Tue Mar 04 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 4.8.0-2
- Patch for Python 3.14 test failures (fixes RHBZ#2349445)

* Mon Feb 10 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 4.8.0-1
- Stop generating HTML documentation; Obsolete the -doc subpackage
- Update to 4.8.0 (close RHBZ#2236330)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 3.7.1-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Aug 7 2023 Lumír Balhar <lbalhar@redhat.com> - 3.7.1-1
- Update to 3.7.1 (rhbz#2085426)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jul 01 2023 Miro Hrončok <mhroncok@redhat.com> - 3.7.0-1
- Update to 3.7.0

* Sat Jul 01 2023 Python Maint <python-maint@redhat.com> - 3.5.0-6
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 3.5.0-3
- Rebuilt for Python 3.11

* Tue Mar 29 2022 Miro Hrončok <mhroncok@redhat.com> - 3.5.0-2
- Fix for pytest7
- Fixes: rhbz#2069194

* Fri Mar 04 2022 Carl George <carl@george.computer> - 3.5.0-1
- Latest upstream rhbz#2007952
- Enable test suite
- Only run test on Fedora
- Only build docs on Fedora

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Oct 08 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 3.3.1-2
- Add metapackage for “trio” extra

* Wed Sep 08 2021 Fabian Affolter <mail@fabian-affolter.ch> - 3.3.1-1
- Update to latest upstream release 3.3.1 (closes rhbz#1975540)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 22 2021 Carl George <carl@george.computer> - 3.2.0-1
- Latest upstream
- Fixes: rhbz#1926501
- Fixes: rhbz#1900506

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.0.2-2
- Rebuilt for Python 3.10

* Thu Jan 28 2021 Dan Čermák <dan.cermak@cgc-instruments.com> - 2.0.2-1
- New upstream release 2.0.2

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 02 2020 Carl George <carl@george.computer> - 1.3.1-1
- Latest upstream

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.2.3-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 Carl George <carl@george.computer> - 1.2.3-1
- Latest upstream rhbz#1786957

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 16 2019 Carl George <carl@george.computer> - 1.0.0-1
- Initial package
