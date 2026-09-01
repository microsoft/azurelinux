# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Allow build without test
%bcond_without tests

Name:           pytz
Version:        2025.2
Release:        6%{?dist}
Summary:        World Timezone Definitions for Python

License:        MIT
URL:            http://pytz.sourceforge.net/
Source:         %pypi_source
# Patch to use the system supplied zoneinfo files
Patch:          pytz-zoneinfo.patch
# https://bugzilla.redhat.com/1497572
Patch:          remove_tzinfo_test.patch

BuildArch:      noarch
BuildRequires:  tzdata

%global _description\
pytz brings the Olson tz database into Python. This library allows accurate\
and cross platform timezone calculations using Python 2.3 or higher. It\
also solves the issue of ambiguous times at the end of daylight savings,\
which you can read more about in the Python Library Reference\
(datetime.tzinfo).\
\
Almost all (over 540) of the Olson timezones are supported.

%description %_description


%package -n python3-%{name}
Summary:        %summary
BuildRequires:  python3-devel
%if %{with tests}
BuildRequires:  python3-pytest
%endif
Requires:       tzdata

%description -n python3-%{name} %_description


%prep
%autosetup -p1


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
rm -r %{buildroot}%{python3_sitelib}/pytz/zoneinfo


%if %{with tests}
%check
%pytest -v
%endif


%files -n python3-pytz
%doc README.rst
%{python3_sitelib}/pytz/
%{python3_sitelib}/pytz-%{version}.dist-info

%changelog
* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2025.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2025.2-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2025.2-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2025.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 2025.2-2
- Rebuilt for Python 3.14

* Tue Mar 25 2025 Gwyn Ciesla <gwync@protonmail.com> - 2025.2-1
- 2025.2

* Fri Jan 31 2025 Gwyn Ciesla <gwync@protonmail.com> - 2025.1-1
- 2025.1

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2024.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 11 2024 Gwyn Ciesla <gwync@protonmail.com> - 2024.2-1
- 2024.2

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2024.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2024.1-2
- Rebuilt for Python 3.13

* Fri Feb 02 2024 Gwyn Ciesla <gwync@protonmail.com> - 2024.1-1
- 2024.1

* Mon Jan 29 2024 Gwyn Ciesla <gwync@protonmail.com> - 2023.4-1
- 2023.4

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2023.3.post1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2023.3.post1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 2023.3.post1-1
- 2023.3.post1

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2023.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2023.3-2
- Rebuilt for Python 3.12

* Wed Mar 29 2023 Gwyn Ciesla <gwync@protonmail.com> - 2023.3-1
- 2023.3

* Mon Mar 27 2023 Gwyn Ciesla <gwync@protonmail.com> - 2023.2-1
- 2023.2

* Wed Mar 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 2022.7.1-3
- migrated to SPDX license

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2022.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 17 2023 Gwyn Ciesla <gwync@protonmail.com> - 2022.7.1-1
- 2022.7.1

* Mon Dec 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 2022.7-1
- 2022.7

* Thu Nov 10 2022 Miro Hrončok <mhroncok@redhat.com> - 2022.6-2
- Run tests during build

* Tue Nov 01 2022 Gwyn Ciesla <gwync@protonmail.com> - 2022.6-1
- 2022.6

* Tue Oct 18 2022 Gwyn Ciesla <gwync@protonmail.com> - 2022.5-1
- 2022.5

* Mon Oct 03 2022 Gwyn Ciesla <gwync@protonmail.com> - 2022.4-1
- 2022.4

* Fri Aug 12 2022 Gwyn Ciesla <gwync@protonmail.com> - 2022.2-1
- 2022.2

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2022.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2022.1-2
- Rebuilt for Python 3.11

* Mon Mar 21 2022 Gwyn Ciesla <gwync@protonmail.com> - 2022.1-1
- 2022.1

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2021.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Oct 04 2021 Gwyn Ciesla <gwync@protonmail.com> - 2021.3-1
- 2021.3

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2021.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 2021.1-3
- Rebuilt for Python 3.10

* Tue Mar 16 2021 Miro Hrončok <mhroncok@redhat.com> - 2021.1-2
- Always close the zone.tab file

* Mon Feb 01 2021 Gwyn Ciesla <gwync@protonmail.com> - 2021.1-1
- 2021.1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2020.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 24 2020 Gwyn Ciesla <gwync@protonmail.com> - 2020.5-1
- 2020.5

* Mon Dec 21 2020 Miro Hrončok <mhroncok@redhat.com> - 2020.4-3
- Disable Python 2 in Fedora 34+

* Wed Nov 25 2020 Miro Hrončok <mhroncok@redhat.com> - 2020.4-2
- Disable Python 2 in ELN

* Mon Nov 02 2020 Gwyn Ciesla <gwync@protonmail.com> - 2020.4-1
- 2020.4

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2020.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 2020.1-2
- Rebuilt for Python 3.9

* Tue Apr 28 2020 Gwyn Ciesla <gwync@protonmail.com> - 2020.1-1
- 2020.1

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2019.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 07 2019 Gwyn Ciesla <gwync@protonmail.com> - 2019.3-1
- 2019.3

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2019.2-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 2019.2-2
- Rebuilt for Python 3.8

* Wed Jul 31 2019 Gwyn Ciesla <gwync@protonmail.com> - 2019.2-1
- 2019.2

* Fri Jul 26 2019 Gwyn Ciesla <gwync@protonmail.com> - 2019.1-1
- 2019.1

* Tue Mar 12 2019 Miro Hrončok <mhroncok@redhat.com> - 2018.9-1
- Update to 2018.9
- Remove leapseconds from pytz.all_timezones (#1642003)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2018.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug 23 2018 Miro Hrončok <mhroncok@redhat.com> - 2018.5-1
- Update to 2018.5 (#1508227)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2017.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 14 2018 Miro Hrončok <mhroncok@redhat.com> - 2017.2-9
- Rebuilt for Python 3.7

* Wed May 23 2018 Miro Hrončok <mhroncok@redhat.com> - 2017.2-8
- Fix ambiguous shebangs

* Sat Mar 17 2018 Matěj Cepl <mcepl@redhat.com> - 2017.2-7
- Switch __python for __python2 macro.

* Sat Mar 17 2018 Matěj Cepl <mcepl@redhat.com> - 2017.2-6
- remove test_tzinfo.PicklingTest.testRoundtrip which fails with our
  system-wide timezone database (#1497572)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2017.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Sep 27 2017 Troy Dawson <tdawson@redhat.com> - 2017.2-4
- Cleanup spec file conditionals

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2017.2-3
- Python 2 binary package renamed to python2-pytz
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2017.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Petr Šabata <contyk@redhat.com> - 2017.2-1
- Update to 2017.2

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2016.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Charalampos Stratakis <cstratak@redhat.com> - 2016.10-3
- Enable tests

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 2016.10-2
- Rebuild for Python 3.6
- Disable python3 tests for now

* Tue Dec 6 2016 Orion Poplawski <orion@cora.nwra.com> - 2016.10-1
- Update to 2016.10

* Tue Nov 8 2016 Orion Poplawski <orion@cora.nwra.com> - 2016.7-1
- Update to 2016.7

* Thu Jul 21 2016 Matěj Cepl <mcepl@redhat.com> - 2016.6.1-1
- Update to 2016.6.1 (RHBZ #1356337)
- Fix Source0 URL to override a change in PyPI URLs (see
  https://bitbucket.org/pypa/pypi/issues/438/)

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2016.4-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon May 16 2016 Orion Poplawski <orion@cora.nwra.com> 2016.4-1
- Use proper PYTHONPATH with python3 test
- Use %%license
- Drop BuildRoot and %%clean

* Sat Apr 23 2016 Matěj Cepl <mcepl@redhat.com> 2016.4-1
- Update to 2016.4 (RHBZ #1265036)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2015.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 03 2015 Robert Kuska <rkuska@redhat.com> - 2015.7-2
- Rebuilt for Python3.5 rebuild

* Mon Oct 26 2015 Orion Poplawski <orion@cora.nwra.com> - 2015.7-1
- Update to 2015.7

* Sun Aug 30 2015 Orion Poplawski <orion@cora.nwra.com> - 2015.4-1
- Update to 2015.4 (bug #1161236)
- Do not ship zoneinfo with python3 package (bug #1251554)
- Run tests

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012d-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012d-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 2012d-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012d-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012d-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan  3 2013 David Malcolm <dmalcolm@redhat.com> - 2012d-3
- remove rhel logic from with_python3 conditional

* Fri Sep 14 2012 Jon Ciesla <limburgher@gmail.com> - 2012d-2
- Use system zoneinfo, BZ 857266.

* Thu Aug 23 2012 Jon Ciesla <limburgher@gmail.com> - 2012d-1
- Latest upstream, python3 support, BZ 851226.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2010h-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2010h-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2010h-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2010h-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jun 28 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 2010h-2
- Define => global

* Tue Apr 27 2010 Jon Ciesla <limb@jcomserv.net> - 2010h-1
- Update to current version, BZ 573252.

* Mon Feb 01 2010 Jon Ciesla <limb@jcomserv.net> - 2009i-7
- Corrected Source0 URL, BZ 560168.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2008i-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2008i-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2008i-4
- Rebuild for Python 2.6

* Tue Nov 18 2008 Jef Spaleta <jspaleta at fedoraproject dot org> 2008i-3
- Apply patch correctly.

* Thu Nov 13 2008 Jef Spaleta <jspaleta at fedoraproject dot org> 2008i-2
- Updated tzdata patch from Petr Machata bug 471014

* Tue Nov 11 2008 Jef Spaleta <jspaleta at fedoraproject dot org> 2008i-1
- Update to latest, now using timezone files provided by tzdata package

* Fri Jan 04 2008 Jef Spaleta <jspaleta@gmail.com> 2006p-3
- Fix for egg-info file creation

* Mon Dec 11 2006 Jef Spaleta <jspaleta@gmail.com> 2006p-2
- Bump for rebuild against python 2.5 and change BR to python-devel accordingly

* Fri Dec  8 2006 Orion Poplawski <orion@cora.nwra.com> 2006p-1
- Update to 2006p

* Thu Sep  7 2006 Orion Poplawski <orion@cora.nwra.com> 2006g-1
- Update to 2006g

* Mon Feb 13 2006 Orion Poplawski <orion@cora.nwra.com> 2005r-2
- Rebuild for gcc/glibc changes

* Tue Jan  3 2006 Orion Poplawski <orion@cora.nwra.com> 2005r-1
- Update to 2005r

* Thu Dec 22 2005 Orion Poplawski <orion@cora.nwra.com> 2005m-1
- Update to 2005m

* Fri Jul 22 2005 Orion Poplawski <orion@cora.nwra.com> 2005i-2
- Remove -O1 from install command

* Tue Jul 05 2005 Orion Poplawski <orion@cora.nwra.com> 2005i-1
- Initial Fedora Extras package
