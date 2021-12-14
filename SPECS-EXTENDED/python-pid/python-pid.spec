Vendor:         Microsoft Corporation
Distribution:   Mariner
%global srcname pid

%global common_description %{expand:
pid provides a PidFile class that manages PID files. PidFile features:
  - stale detection
  - locking using fcntl
  - chmod (default is 0o644)
  - chown
  - custom exceptions

PidFile can also be used as a context manager or a decorator.}

%if %{defined el6}
%bcond_without  python2
# nose is too old
%bcond_with     python2_tests
%endif

%if %{defined el7}
%bcond_without  python2
%bcond_without  python2_tests
%endif




%bcond_without  python3
%bcond_without  python3_tests

Name:           python-%{srcname}
Version:        2.2.3
Release:        7%{?dist}
Summary:        PID file management library

License:        ASL 2.0
URL:            https://github.com/trbs/pid
Source0:        %pypi_source

# https://github.com/trbs/pid/pull/23
Patch0:         use-standard-library-mock-when-available.patch

BuildArch:      noarch

%description %{common_description}

%if %{with python2}
%package -n python2-%{srcname}
Summary:        %{summary}

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%if %{with python2_tests}
BuildRequires:  python2-nose >= 1.0
BuildRequires:  python2-mock
%endif

%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname} %{common_description}
%endif

%if %{with python3}
%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%if %{with python3_tests}
BuildRequires:  python%{python3_pkgversion}-nose >= 1.0
%endif

%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%description -n python%{python3_pkgversion}-%{srcname} %{common_description}
%endif

%prep
# This needs to have a blank line after because of a bug in the EL6 macros
%autosetup -p1 -n %{srcname}-%{version}

rm -rf %{srcname}.egg-info

%build
%if %{with python2}
%py2_build
%endif
%if %{with python3}
%py3_build
%endif

%install
%if %{with python2}
%py2_install
%endif
%if %{with python3}
%py3_install
%endif

%check
%if %{with python2_tests}
PYTHONPATH=%{buildroot}%{python2_sitelib} nosetests-%{python2_version} --verbose
%endif
%if %{with python3_tests}
PYTHONPATH=%{buildroot}%{python3_sitelib} nosetests-%{python3_version} --verbose
%endif

%if %{with python2}
%files -n python2-%{srcname}
%license LICENSE
%doc AUTHORS CHANGELOG README.rst
%{python2_sitelib}/%{srcname}
%{python2_sitelib}/%{srcname}-%{version}-py%{python2_version}.egg-info
%endif

%if %{with python3}
%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc AUTHORS CHANGELOG README.rst
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info
%endif

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.2.3-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.2.3-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 2.2.3-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 08 2019 Troy Dawson <tdawson@redhat.com> - 2.2.3-2
- Rebuilt to change main python from 3.4 to 3.6

* Tue Mar 05 2019 Carl George <carl@george.computer> - 2.2.3-1
- Latest upstream
- Build python3 subpackage on el6
- Run tests correctly

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 2.1.1-8
- Rebuilt for Python 3.7

* Thu Mar 22 2018 David Shea <dshea@redhat.com> - 2.1.1-7
- Remove the python2 package

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 27 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.1.1-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 2.1.1-2
- Rebuild for Python 3.6

* Tue Nov 29 2016 David Shea <dshea@redhat.com> - 2.1.1-1
- Update to 2.1.1, which adds an optional allow_samepid parameter

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 03 2015 Robert Kuska <rkuska@redhat.com> - 2.0.1-3
- Rebuilt for Python3.5 rebuild

* Wed Aug 05 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.1-2
- Update to modern python packaging guidelines

* Tue Aug  4 2015 David Shea <dshea@redhat.com> - 2.0.1-1
- Initial package
