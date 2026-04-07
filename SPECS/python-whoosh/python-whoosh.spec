# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# For bootstrapping sphinxcontrib-websupport
%bcond_without docs

%global mod_name Whoosh

Name:           python-whoosh
Version:        2.7.4
Release:        41%{?dist}
Summary:        Fast, pure-Python full text indexing, search, and spell checking library 

# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD 
URL:            http://pythonhosted.org/Whoosh/
Source0:        https://pypi.python.org/packages/source/W/%{mod_name}/%{mod_name}-%{version}.tar.gz
Patch1:         whoosh-fix-sphinx.patch

BuildArch:      noarch

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
%setup -q -n %{mod_name}-%{version}
%patch -p1 -P1
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
# Do not run test over test_automata.py, it fails due to Python 3.13
# Whoosh project is dead, no fixes expected
rm tests/test_automata.py
%pytest

%files -n python%{python3_pkgversion}-whoosh
%license LICENSE.txt
%doc README.txt
%if %{with docs}
%doc docs/html/
%endif
%{python3_sitelib}/whoosh/
%{python3_sitelib}/*.egg-info/

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.7.4-41
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.7.4-40
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.7.4-38
- Rebuilt for Python 3.14

* Thu Jan 23 2025 Alexander Bokovoy <abokovoy@redhat.com> - 2.7.4-37
- fix sphinx references
- Resolves: rhbz#2341238

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Oct 23 2024 Alexander Bokovoy <abokovoy@redhat.com> - 2.7.4-35
- Switch from 'setup.py test' to '%pytest'
- Resolves: rhbz#2319736

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 2.7.4-34
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.7.4-32
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 2.7.4-28
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.7.4-25
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 2.7.4-22
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 2.7.4-19
- Rebuilt for Python 3.9

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

