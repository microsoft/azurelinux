Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global common_description %{expand:
The Trio project's goal is to produce a production-quality, permissively
licensed, async/await-native I/O library for Python.  Like all async libraries,
its main purpose is to help you write programs that do multiple things at the
same time with parallelized I/O.  A web spider that wants to fetch lots of
pages in parallel, a web server that needs to juggle lots of downloads and
websocket connections at the same time, a process supervisor monitoring
multiple subprocesses... that sort of thing.  Compared to other libraries, Trio
attempts to distinguish itself with an obsessive focus on usability and
correctness.  Concurrency is complicated; we try to make it easy to get things
right.}
 
 
Name:           python-trio
Version:        0.23.1
Release:        1%{?dist}
Summary:        A friendly Python library for async concurrency and I/O
License:        Apache-2.0 OR MIT
URL:            https://github.com/python-trio/trio
Source:         %pypi_source trio
 
# Python 3.13 support
# Manually rebased from https://github.com/python-trio/trio/pull/2959
Patch:          python3.13-PR-2959.patch
# Manually rebased from https://github.com/python-trio/trio/pull/3005
Patch:          python3.13-PR-3005.patch
 
BuildArch:      noarch
 
 
%description %{common_description}
 
 
%package -n python3-trio
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  python3-sniffio
 
%description -n python3-trio %{common_description}

%prep
%autosetup -p 1 -n trio-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel
 
%install
%pyproject_install
%pyproject_save_files trio
 
%check
# https://github.com/python-trio/trio/issues/2863
# https://github.com/python-trio/trio/pull/2870
# https://docs.pytest.org/en/stable/explanation/goodpractices.html#tests-as-part-of-application-code
%pytest --pyargs trio -p trio._tests.pytest_plugin --verbose --skip-optional-imports
 
%files -n python3-trio -f %{pyproject_files}
%doc README.rst

%changelog
* Mon Apr 21 2025 Akarsh Chaudhary <v-akarshc@microsoft.com> - 0.23.1-1
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified

* Tue Apr 26 2022 Mandeep Plaha <mandeepplaha@microsoft.com> - 0.16.0-3
- Updated source URL.
- License verified.
* Tue Dec 08 2020 Steve Laughman <steve.laughman@microsoft.com> - 0.16.0-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
- Disable tests by default
* Sun Sep 06 2020 Carl George <carl@george.computer> - 0.16.0-1
- Latest upstream
* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
* Thu Jun 04 2020 Carl George <carl@george.computer> - 0.15.1-1
- Latest upstream rhbz#1828266
* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.13.0-3
- Rebuilt for Python 3.9
* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
* Thu Jan 02 2020 Carl George <carl@george.computer> - 0.13.0-1
- Latest upstream rhbz#1742425
* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.11.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)
* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.11.0-3
- Rebuilt for Python 3.8
* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild
* Thu Feb 28 2019 Carl George <carl@george.computer> - 0.11.0-1
- Latest upstream
* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
* Thu Sep 20 2018 Carl George <carl@george.computer> - 0.7.0-1
- Initial package