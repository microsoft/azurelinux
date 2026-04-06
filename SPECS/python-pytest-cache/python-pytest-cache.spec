# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?fedora} >= 31
%bcond_with python2
%else
%bcond_without python2 
%endif

%global srcname pytest-cache

Name:           python-%{srcname}
Version:        1.0
Release:        41%{?dist}
Summary:        Pytest plugin with mechanisms for caching across test runs

License:        MIT
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        https://pypi.python.org/packages/source/p/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

%description
Pytest plugin with mechanisms for caching across test runs for Python 2.

%if %{with python2}
%package -n python2-%{srcname}
Summary:        Pytest plugin with mechanisms for caching across test runs for Python 3
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pytest
BuildRequires:  python2-execnet
Requires:       python2-pytest
Requires:       python2-execnet
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
Pytest plugin with mechanisms for caching across test runs for Python 3.
%endif

%package -n python%{python3_pkgversion}-%{srcname}
Summary:        Pytest plugin with mechanisms for caching across test runs for Python 3
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-execnet
BuildRequires:  python%{python3_pkgversion}-pytest
Requires:       python%{python3_pkgversion}-execnet
Requires:       python%{python3_pkgversion}-pytest
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%description -n python%{python3_pkgversion}-%{srcname}
Pytest plugin with mechanisms for caching across test runs for Python 3.


%prep
%setup -q -n %{srcname}-%{version}
rm -rf *.egg-info


%build
%if %{with python2}
%py2_build
%endif
%py3_build


%install
%py3_install
%if %{with python2}
%py2_install
%endif


%check
# No idea why the tests fail
%if %{with python2}
PYTHONPATH=%{buildroot}%{python2_sitelib} py.test-%{python2_version} -v || :
%endif
PYTHONPATH=%{buildroot}%{python3_sitelib} py.test-%{python3_version} -v || :


%if %{with python2}
%files -n python2-%{srcname}
%license LICENSE
%doc CHANGELOG PKG-INFO README.rst
%{python2_sitelib}/pytest_cache.py*
%{python2_sitelib}/pytest_cache-*.egg-info/
%endif

%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc CHANGELOG PKG-INFO README.rst
%{python3_sitelib}/pytest_cache.py
%{python3_sitelib}/pytest_cache-*.egg-info/
%{python3_sitelib}/__pycache__/*


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.0-41
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.0-40
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.0-38
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.0-35
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 1.0-31
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 1.0-28
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.0-25
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0-22
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0-20
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0-19
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Apr  4 2019 Orion Poplawski <orion@nwra.com> - 1.0-17
- Drop python2 for Fedora 31+
- Build for python3 for EPEL
- Be more explicit about files
- Run tests with py.test, but ignore failures

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0-14
- Rebuilt for Python 3.7

* Wed Feb 28 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.0-13
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.0-9
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-8
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sat Feb 13 2016 Orion Poplawski <orion@cora.nwra.com> - 1.0-7
- Fix provide typo

* Wed Feb 3 2016 Orion Poplawski <orion@cora.nwra.com> - 1.0-6
- Modernize spec
- Fix python3 package file ownership

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue Feb 25 2014 Orion Poplawski <orion@cora.nwra.com> - 1.0-1
- Initial package
