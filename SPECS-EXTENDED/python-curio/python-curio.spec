%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?__python3: %global __python3 /usr/bin/python3}

# what it's called on pypi
%global srcname curio
# what it's imported as
%global libname curio
# name of egg info directory
%global eggname curio
# package name fragment
%global pkgname curio

%global _description \
Curio is a library of building blocks for performing concurrent I/O and common\
system programming tasks such as launching subprocesses, working with files,\
and farming work out to thread and process pools.  It uses Python coroutines\
and the explicit async/await syntax introduced in Python 3.5.  Its programming\
model is based on cooperative multitasking and existing programming\
abstractions such as threads, sockets, files, subprocesses, locks, and queues.\
You'll find it to be small, fast, and fun.  Curio has no third-party\
dependencies and does not use the standard asyncio module.  Most users will\
probably find it to be a bit too-low level--it's probably best to think of it\
as a library for building libraries.  Although you might not use it directly,\
many of its ideas have influenced other libraries with similar functionality.

%bcond_without tests

Summary:        Building blocks for performing concurrent I/O
Name:           python-%{pkgname}
Version:        1.4
Release:        3%{?dist}
License:        BSD
URL:            https://github.com/dabeaz/curio
#Source0:       https://files.pythonhosted.org/packages/source/c/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source0:        https://files.pythonhosted.org/packages/source/c/%{pypi_name}/%{name}-%{version}.tar.gz
BuildArch:      noarch

%description %{_description}

%package -n python3-%{pkgname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with tests}
BuildRequires:  python3-pytest
%endif
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname} %{_description}

%prep
%autosetup -n %{srcname}-%{version} -p 1
rm -rf %{eggname}.egg-info

%build
%py3_build

%install
%py3_install

%if %{with tests}
%check
PYTHONPATH=%{buildroot}%{python3_sitelib} py.test-%{python3_version} --verbose -m 'not internet'
%endif

%files -n python3-%{pkgname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{libname}
%{python3_sitelib}/%{eggname}-%{version}-py%{python3_version}.egg-info

%changelog
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