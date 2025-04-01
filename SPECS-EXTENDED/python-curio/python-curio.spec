# Upstream doesn't plan to make any more releases.  Unless they change their
# mind, we'll need to stick with git snapshots going forward.
# https://github.com/dabeaz/curio/commit/45ada857189de0e6b3b81f50e93496fc710889ca
%global commit      148454621f9bd8dd843f591e87715415431f6979
%global shortcommit %{lua:print(macros.commit:sub(1,7))}

Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           python-curio
Version:        1.6^1.%{shortcommit}
Release:        1%{?dist}
Summary:        Building blocks for performing concurrent I/O
License:        BSD-3-Clause
URL:            https://github.com/dabeaz/curio
Source:         %{url}/archive/%{commit}/curio-%{shortcommit}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch

%global common_description %{expand:
Curio is a coroutine-based library for concurrent Python systems programming
using async/await. It provides standard programming abstractions such as tasks,
sockets, files, locks, and queues as well as some advanced features such as
support for structured concurrency. It works on Unix and Windows and has zero
dependencies. You will find it to be familiar, small, fast, and fun.}


%description %{common_description}


%package -n python3-curio
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist pytest}

BuildRequires:  python3-pip
BuildRequires:  python3dist(wheel)

%description -n python3-curio %{common_description}

%prep
%autosetup -n curio-%{commit}


%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files curio

%check
%pytest --verbose -m 'not internet'

%files -n python3-curio -f %{pyproject_files}
%doc README.rst

%changelog
* Mon Mar 19 2025 Sumit Jena <v-sumitjena@microsoft.com> - 1.6^1.1484546-1
- Update to version 1.6^1.1484546
- License verified

* Thu Apr 28 2022 Muhammad Falak <mwani@microsoft.com> - 1.4-5
- Drop BR on pytest & pip install latest deps
- Use py.test instead of py.test-3 to enable ptest

* Wed Jun 05 2024 Carl George <carlwgeorge@fedoraproject.org> - 1.6^1.1484546-1
- Update to latest upstream snapshot
- Resolves Python 3.13 build error rhbz#2246053
- Switch to SPDX license notation

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jul 25 2023 Carl George <carl@george.computer> - 1.6-5
- Add patch for Python 3.12 compatibility, resolves rhbz#2174408

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.6-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Oct 25 2022 Carl George <carl@george.computer> - 1.6-1
- Update to 1.6, resolves rhbz#2137578

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.5-6
- Rebuilt for Python 3.11

* Thu Jan 27 2022 Carl George <carl@george.computer> - 1.5-5
- Convert to pyproject macros

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.5-2
- Rebuilt for Python 3.10

* Fri Mar 19 2021 Charalampos Stratakis <cstratak@redhat.com> - 1.5-1
- Update to 1.5 (rhbz#1821534)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Oct 05 2020 Yatin Karel <ykarel@redhat.com> - 1.4-1
- Update to 1.4

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1-2
- Rebuilt for Python 3.9

* Wed Mar 18 2020 Carl George <carl@george.computer> - 1.1-1
- Latest upstream
- Add patch0 to skip tests that require internet

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Sep 12 2018 Carl George <carl@george.computer> - 0.9-1
- Initial package

## END: Generated by rpmautospec
