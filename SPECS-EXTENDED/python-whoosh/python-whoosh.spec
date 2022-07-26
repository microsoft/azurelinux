# For bootstrapping sphinxcontrib-websupport
%bcond_without docs

Name:           python-whoosh
Version:        2.7.4
Release:        21%{?dist}
Summary:        Fast, pure-Python full text indexing, search, and spell checking library

License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/mchaput/whoosh
Source0:        https://github.com/mchaput/whoosh/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch

%if %{with_check}
BuildRequires:  python3-pip
%endif

%if %{with docs}
BuildRequires:  python%{python3_pkgversion}-sphinx
%endif

BuildRequires: python%{python3_pkgversion}-devel
BuildRequires: python%{python3_pkgversion}-setuptools
BuildRequires: python%{python3_pkgversion}-pytest

%description
Whoosh is a fast, featureful full-text indexing and searching library
implemented in pure Python. Programmers can use it to easily add search
functionality to their applications and websites. Every part of how Whoosh
works can be extended or replaced to meet your needs exactly.

%package -n python%{python3_pkgversion}-whoosh
Summary:    Fast, Python3 full text indexing, search, and spell checking library
%{?python_provide:%python_provide python%{python3_pkgversion}-whoosh}

%description -n python%{python3_pkgversion}-whoosh
Whoosh is a fast, featureful full-text indexing and searching library
implemented in pure Python. Programmers can use it to easily add search
functionality to their applications and websites. Every part of how Whoosh
works can be extended or replaced to meet your needs exactly.

%prep
%setup -q -n whoosh-%{version}
# pytest 4
sed -i 's/\[pytest\]/\[tool:pytest\]/' setup.cfg

%build
%py3_build

%if %{with docs}
sphinx-build docs/source docs/html
rm -f docs/html/.buildinfo
rm -rf docs/html/.doctrees
%endif

%install
%py3_install

%check
%{__python3} -m pip install wheel
%{__python3} setup.py test

%files -n python%{python3_pkgversion}-whoosh
%license LICENSE.txt
%doc README.txt
%if %{with docs}
%doc docs/html/
%endif
%{python3_sitelib}/whoosh/
%{python3_sitelib}/*.egg-info/

%changelog
* Fri Jul 22 2022 Muhammad Falak <mwani@microsoft.com> - 2.7.4-21
- Install `wheel` package in %check section to enable build
- Switch to github tarball

* Thu Apr 21 2022 Muhammad Falak <mwani@microsoft.com> - 2.7.4-20
- Add an explicit BR on `pip` to enable ptest
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.7.4-19
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.7.4-17
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 2.7.4-16
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 20 2019 Miro Hrončok <mhroncok@redhat.com> - 2.7.4-14
- Subpackage python2-whoosh has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 2.7.4-11
- Rebuilt for Python 3.7

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 2.7.4-10
- Bootstrap for Python 3.7

* Wed Feb 28 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.7.4-9
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Charalampos Stratakis <cstratak@redhat.com> - 2.7.4-5
- Enable tests

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 2.7.4-4
- Rebuild for Python 3.6
- Disable python3 tests for now

* Wed Oct 12 2016 Orion Poplawski <orion@cora.nwra.com> - 2.7.4-3
- Ship python2-whoosh
- Build python3 package for EPEL7
- Modernize spec

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.4-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sun May 01 2016 Robert Kuska <rkuska@gmail.com> - 2.7.4-1
- Update to version 2.7.4

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 12 2015 Robert Kuska <rkuska@redhat.com> 2.7.0-1
- Update to version 2.7.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jul 30 2014 Robert Kuska <rkuska@redhat.com> - 2.7.5-4
- Change spec for el6 and epel7

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 16 2014 Robert Kuska <rkuska@redhat.com> - 2.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Mar 03 2014 Robert Kuska <rkuska@redhat.com> - 2.5.7-1
- Rebase to 2.5.7

* Mon Jan 27 2014 Robert Kuska <rkuska@redhat.com> - 2.5.6-1
- Rebase to 2.5.6

* Tue Nov 19 2013 Robert Kuska <rkuska@redhat.com> - 2.5.5-1
- Rebase to 2.5.5

* Mon Sep 09 2013 Robert Kuska <rkuska@redhat.com> - 2.5.3-1
- Rebase to 2.5.3

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 08 2013 Robert Kuska <rkuska@redhat.com> - 2.5.1-1
- Update source
- Add python3 subpackage (rhbz#979235)

* Mon Apr 08 2013 Robert Kuska <rkuska@redhat.com> - 2.4.1-2
- Review fixes

* Fri Apr 05 2013 Robert Kuska <rkuska@redhat.com> - 2.4.1-1
- Initial package

