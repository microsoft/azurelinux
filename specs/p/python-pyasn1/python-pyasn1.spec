# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global module pyasn1
%global modules_version 0.4.1

Name:           python-pyasn1
Version:        0.6.2
Release: 2%{?dist}
Summary:        ASN.1 tools for Python
License:        BSD-2-Clause
Source0:        https://github.com/pyasn1/pyasn1/archive/v%{version}.tar.gz
Source1:        https://github.com/pyasn1/pyasn1-modules/archive/v%{modules_version}.tar.gz
URL:            https://github.com/pyasn1/pyasn1
BuildArch:      noarch

%description
This is an implementation of ASN.1 types and codecs in the Python programming
language.

%package -n python3-pyasn1
Summary:    ASN.1 tools for Python 3
BuildRequires:  python3-devel
BuildRequires:  python3-pytest

%description -n python3-pyasn1
This is an implementation of ASN.1 types and codecs in the Python 3 programming
language.

%package -n python3-pyasn1-modules
Summary:    Modules for pyasn1
Requires:   python3-pyasn1 >= 0.4.7, python3-pyasn1 < 0.7.0

%description -n python3-pyasn1-modules
ASN.1 types modules for python3-pyasn1.

%package doc
Summary:        Documentation for pyasn1
BuildRequires:  make
BuildRequires:  python3-sphinx

%description doc
%{summary}.


%prep
%setup -n %{module}-%{version} -q -b1


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel

pushd ../pyasn1-modules-%{modules_version}
%pyproject_wheel
popd

pushd docs
PYTHONPATH=%{buildroot}%{python3_sitelib} make SPHINXBUILD=sphinx-build-3 html
popd


%install
%pyproject_install


%check
%pytest


%files -n python3-pyasn1
%doc README.md
%license LICENSE.rst
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-%{version}.dist-info/

%files -n python3-pyasn1-modules
%{python3_sitelib}/%{module}_modules/
%{python3_sitelib}/%{module}_modules-%{modules_version}.dist-info/

%files doc
%license LICENSE.rst
%doc docs/build/html/*

%changelog
* Thu Feb 05 2026 Simon Pichugin <spichugi@redhat.com> - 0.6.2-1
- Update to 0.6.2
- Fixed continuation octet limits in OID/RELATIVE-OID decoder (CVE-2026-23490)

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.6.1-7
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.6.1-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.6.1-4
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Oct 18 2024 Rob Crittenden <rcritten@redhat.com> - 0.6.1-2
- Convert to the pyproject macros (#2319694)

* Fri Sep 20 2024 Simon Pichugin <spichugi@redhat.com> - 0.6.1-1
- Update to 0.6.1
- Update modules to 0.4.1

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.6.0-2
- Rebuilt for Python 3.13

* Fri Apr 26 2024 Simon Pichugin <spichugi@redhat.com> - 0.6.0-1
- Update to 0.6.0
- Update modules to 0.4.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 27 2023 Simon Pichugin <spichugi@redhat.com> - 0.5.1-1
- Update to 0.5.1
- Update modules to 0.3.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 27 2023 Stephen Gallagher <sgallagh@redhat.com> - 0.4.8-15
- Rebuild for Python 3.12

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 0.4.8-14
- Rebuilt for Python 3.12

* Thu Feb 23 2023 Rob Crittenden <rcritten@redhat.com> - 0.4.8-13
- migrated to SPDX license
- correct bad date in changelog

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.4.8-10
- Rebuilt for Python 3.11

* Mon Mar  1 2021 Rob Crittenden <rcritten@redhat.com> - 0.4.8-9
- Set URL to https://github.com/etingof/pyasn1 in the spec file (#2059715)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-7
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 07 2021 Rob Crittenden <rcritten@redhat.com> - 0.4.8-6
- Follow upstream requirements.txt for modules -> pyasn1 (#1979875)

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 0.4.8-5
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 0.4.8-2
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Rob Crittenden <rcritten@redhat.com> - 0.4.8-1
- Update to 0.4.8 (#1747820)
- Update modules to 0.2.8

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 23 2019 Rob Crittenden <rcritten@redhat.com> - 0.4.6-3
- Remove python2 subpackages (#1764573)

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4.6-2
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 30 2019 Rob Crittenden <rcritten@redhat.com> - 0.4.6-1
- Update to 0.4.6 (#1742424)
- Update modules to 0.2.6

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4.4-6
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 16 2018 Rob Crittenden <rcritten@redhat.com> - 0.4.4-3
- Restore python2 subpackages

* Mon Oct 15 2018 Rob Crittenden <rcritten@redhat.com> - 0.4.4-2
- Add back accidentally removed buildrequires

* Mon Oct 15 2018 Rob Crittenden <rcritten@redhat.com> - 0.4.4-1
- Update to 0.4.4 (#1582010)
- Update modules to 0.2.2
- Drop python 2 subpackages

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.3.7-5
- Use Python 3 Sphinx if with Python 3
- Cleanup

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 0.3.7-4
- Rebuilt for Python 3.7

* Wed Feb 14 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.3.7-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 16 2017 Christian Heimes <cheimes@redhat.com> - 0.3.7-1
- Update to upstream release 0.3.7 (#1492446)
- Update modules to 0.1.5

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 0.3.4-2
- Cleanup spec file conditionals

* Fri Sep 15 2017 Rob Crittenden <rcritten@redhat.com> - 0.3.4-1
- Update to upstream release 0.3.4 (#1485669)
- Update modules to 0.1.2
- Patch to fixed crash at SequenceOf native decoder

* Wed Aug 16 2017 Rob Crittenden <rcritten@redhat.com> - 0.3.2-1
- Update to upstream release 0.3.2 (#1475594)
- Update modules to 0.0.11

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 27 2017 Rob Crittenden <rcritten@redhat.com> - 0.2.3-1
- Update to upstream release 0.2.3 (#1426979)
- Adapt to the way upstream changed the way tests are executed
- Pass PYTHONPATH when building the documentation

* Mon Feb  6 2017 Rob Crittenden <rcritten@redhat.com> - 0.2.1-1
- Update to upstream release 0.2.1 (#1419310)
- Added doc subpackage and moved documentation there

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.1.9-8.1
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.9-7.1
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Rob Crittenden <rcritten@redhat.com> - 0.1.9-5.1
- Add in missing colon after Provides

* Mon Jan 11 2016 Rob Crittenden <rcritten@redhat.com> - 0.1.9-5
- If python_provide wasn't defined then the python2 subpackages
  didn't provide python-pyasn1-*

* Tue Jan  5 2016 Martin Kosek <mkosek@redhat.com> - 0.1.9-4
- Fix python2 provides for pyasn1 modules (#1295693)

* Mon Jan  4 2016 Rob Crittenden <rcritten@redhat.com> - 0.1.9-3
- Explicitly provide python2 subpackages, use python_provide macro

* Wed Nov 04 2015 Robert Kuska <rkuska@redhat.com> - 0.1.9-2
- Rebuilt for Python3.5 rebuild

* Mon Oct 19 2015 Rob Crittenden <rcritten@redhat.com> - 0.1.9-1
- Update to new upstream release 0.1.9, modules 0.0.8.

* Sat Aug 15 2015 Rob Crittenden <rcritten@redhat.com> - 0.1.8-2
- Move LICENSE to the license tag instead of doc.

* Wed Jul 15 2015 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.1.8-1
- Update to new upstream release 0.1.8, modules 0.0.6.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Rob Crittenden <rcritten@redhat.com> - 0.1.7-1
- update to upstream release 0.1.7
- update modules to 0.0.5

* Sat Feb 16 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 0.1.6-1
- update to upstream release 0.1.6
- update modules to 0.0.4
- update description
- add python3-pyasn1 subpackage
- add versioned Requires for the module subpackages
- add %%check section

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 02 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.1.2-1
- New upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.12a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Rob Crittenden <rcritten@redhat.com> - 0.0.12a-1
- Update to upstream version 0.0.12a

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.0.9a-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Nov 16 2009 Rob Crittenden <rcritten@redhat.com> - 0.0.9a-1
- Update to upstream version 0.0.9a
- Include patch that adds parsing for the Any type

* Wed Sep  2 2009 Rob Crittenden <rcritten@redhat.com> - 0.0.8a-5
- Include doc/notes.html in the package

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.8a-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.8a-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.0.8a-2
- Rebuild for Python 2.6

* Tue Sep  9 2008 Paul P. Komkoff Jr <i@stingr.net> - 0.0.8a-1
- Update to upstream version 0.0.8a

* Wed Jan 16 2008 Rob Crittenden <rcritten@redhat.com> - 0.0.7a-4
- Use setuptools to install the package
- simplify the files included in the rpm so it includes the .egg-info

* Mon Jan 14 2008 Rob Crittenden <rcritten@redhat.com> - 0.0.7a-3
- Rename to python-pyasn1
- Spec file cleanups

* Mon Nov 19 2007 Karl MacMillan <kmacmill@redhat.com> - 0.0.7a-2
- Update rpm to be more fedora friendly

* Thu Nov 8 2007 Simo Sorce <ssorce@redhat.com> 0.0.7a-1
- New release

* Mon May 28 2007 Andreas Hasenack <andreas@mandriva.com> 0.0.6a-1mdv2008.0
+ Revision: 31989
- fixed (build)requires
- Import pyasn1

