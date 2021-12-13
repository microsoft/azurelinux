Vendor:         Microsoft Corporation
Distribution:   Mariner
%global pypi_name fasteners

%if 0%{?rhel} >= 8
%bcond_with pytests
%else
%bcond_without pytests
%endif

Name:           python-%{pypi_name}
Version:        0.14.1
Release:        22%{?dist}
Summary:        A python package that provides useful locks

License:        ASL 2.0
URL:            https://github.com/harlowja/fasteners
Source0:        https://codeload.github.com/harlowja/fasteners/tar.gz/%{version}#/%{pypi_name}-%{version}.tar.gz
Patch0:         fasteners-monotonic.patch
BuildArch:      noarch

%description
A python package that provides useful locks.


%package -n python3-%{pypi_name}
Summary:        A python package that provides useful locks
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-six
BuildRequires:  python3-devel
# tests
%if %{with pytests}
BuildRequires:  python3-testtools
BuildRequires:  python3-nose
Requires:       python3-six
%endif

%description -n python3-%{pypi_name}
A python package that provides useful locks.


%prep
%autosetup -p1 -n %{pypi_name}-%{version}


%build
%py3_build


%install
%py3_install

%if %{with pytests}
%check
nosetests-%{python3_version}
%endif

%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-*.egg-info/


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.14.1-22
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 15 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.14.1-21
- Fix conditionals.

* Mon Jan 13 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.14.1-19
- Disable tests on EL-8

* Mon Sep 02 2019 Miro Hrončok <mhroncok@redhat.com> - 0.14.1-18
- Subpackage python2-fasteners has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.14.1-17
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.14.1-13
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.14.1-12
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 17 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.14.1-10
- Fix monotonic req on py3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.14.1-7
- Rebuild for Python 3.6

* Mon Aug 29 2016 Matthias Runge <mrunge@redhat.com> - 0.14.1-6
- Use time.monotonic if available (Python3 > 3.2)
  patch thanks to Ville Skyttä (rhbz#1294335)
- modernize spec

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.1-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Mar 16 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 0.14.1-4
- Spec cleanups

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 18 2015 Matthias Runge <mrunge@redhat.com> - 0.14.1-2
- update to 0.14.1 (rhbz#1281772)
- fix python_provide

* Mon Nov 16 2015 Matthias Runge <mrunge@redhat.com> - 0.13.0-3
- Fix build

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Aug 28 2015 Matthias Runge <mrunge@redhat.com> - 0.13.0-1
- update to 0.13.0 (rhbz#1256153)

* Mon Jun 22 2015 Matthias Runge <mrunge@redhat.com> - 0.12.0-1
- update to 0.12.0 (rhbz#1234253)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 Matthias Runge <mrunge@redhat.com> - 0.9.0-2
- switch to github sourcecode, license included
- add tests, fix conditionals for python3

* Thu Jun 11 2015 Matthias Runge <mrunge@redhat.com> - 0.9.0-1
- Initial package. (rhbz#1230548)
