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

* Tue Apr 26 2022 Mandeep Plaha <mandeepplaha@microsoft.com> - 1.4-4
- Updated source URL.
- License verified.

* Tue Jan 12 2021 Steve Laughman <steve.laughman@microsoft.com> - 1.4-3
- Correction to files declaration

* Tue Dec 08 2020 Steve Laughman <steve.laughman@microsoft.com> - 1.4-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT)

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
