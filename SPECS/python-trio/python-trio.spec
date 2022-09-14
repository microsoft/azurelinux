%global pypi_name trio

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

Summary:        A friendly Python library for async concurrency and I/O
Name:           python-%{pypi_name}
Version:        0.21.0
Release:        1%{?dist}
License:        MIT or ASL 2.0
URL:            https://github.com/python-trio/trio
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%description %{common_description}

%package -n python3-%{pypi_name}
Summary:        %{summary}

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
%endif
Requires:       python3-async-generator
Requires:       python3-attrs
Requires:       python3-cffi
Requires:       python3-idna
Requires:       python3-outcome
Requires:       python3-sniffio
Requires:       python3-sortedcontainers

%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name} %{common_description}

%prep
%autosetup -n %{pypi_name}-%{version}
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%check
%{python3} -m pip install -r test-requirements.txt
%pytest -v trio/_core/tests
%pytest -v trio/tests

%files -n python3-%{pypi_name}
%license LICENSE LICENSE.MIT LICENSE.APACHE2
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info

%changelog
* Wed Sep 14 2022 Sumedh Sharma <sumsharma@microsoft.com> - 0.21.0-1
- Move from SPECS-EXTENDED to SPECS
- Bump version to 0.21.0
- Enabling test section
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
