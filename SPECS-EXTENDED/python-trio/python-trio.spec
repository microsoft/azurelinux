%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?__python3: %global __python3 /usr/bin/python3}

# what it's called on pypi
%global srcname trio
# what it's imported as
%global libname %{srcname}
# name of egg info directory
%global eggname %{srcname}
# package name fragment
%global pkgname %{srcname}

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

%bcond_with  tests

Name:           python-%{pkgname}
Version:        0.16.0
Release:        2%{?dist}
Summary:        A friendly Python library for async concurrency and I/O
License:        MIT or ASL 2.0
URL:            https://github.com/python-trio/trio
#Source0:       https://files.pythonhosted.org/packages/source/t/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source0:        https://files.pythonhosted.org/packages/source/t/%{pypi_name}/%{name}-%{version}.tar.gz
BuildArch:      noarch

%description %{common_description}

%package -n python3-%{pkgname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with tests}
BuildRequires:  python3-pytest
BuildRequires:  python3-pyOpenSSL
BuildRequires:  python3-trustme
BuildRequires:  python3-attrs
BuildRequires:  python3-sortedcontainers
BuildRequires:  python3-async-generator
BuildRequires:  python3-idna
BuildRequires:  python3-outcome
BuildRequires:  python3-sniffio
%endif
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{common_description}

%prep
%autosetup -n %{srcname}-%{version}
rm -rf %{eggname}.egg-info

%build
%py3_build

%install
%py3_install

%if %{with tests}
%check
%pytest --verbose trio/_core/tests
%endif

%files -n python3-%{pkgname}
%license LICENSE LICENSE.MIT LICENSE.APACHE2
%doc README.rst
%{python3_sitelib}/%{libname}
%{python3_sitelib}/%{eggname}-%{version}-py%{python3_version}.egg-info

%changelog
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