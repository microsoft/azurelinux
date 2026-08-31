# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           pyodbc
Version:        5.1.0
Release:        6%{?dist}
Summary:        Python DB API 2.0 Module for ODBC
License:        MIT-0
URL:            https://github.com/mkleehammer/pyodbc
Source0:        https://github.com/mkleehammer/pyodbc/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Fix build with Python 3.13
# https://github.com/mkleehammer/pyodbc/pull/1361
# https://bugzilla.redhat.com/show_bug.cgi?id=2246290
Patch:          0001-Adjust-for-_PyLong_AsByteArray-signature-change-in-P.patch
BuildRequires:  gcc-c++
BuildRequires:  unixODBC-devel
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Recommends: (postgresql-odbc if postgresql-server)
Recommends: (mariadb-connector-odbc if mariadb-server)

%global _description\
A Python DB API 2 and 3 module for ODBC. This project provides an up-to-date,\
convenient interface to ODBC using native data types like datetime and\
decimal.

%description %_description

%package -n python3-%{name}
Summary:        Python DB API 2.0 Module for ODBC
%{?python_provide:%python_provide python3-%{name}}
Recommends: (mariadb-connector-odbc if mariadb-server)
Recommends: (postgresql-odbc if postgresql-server)

%description -n python3-%{name}
A Python DB API 2 and 3 module for ODBC. This project provides an up-to-date,
convenient interface to ODBC using native data types like datetime and
decimal.

%prep
%autosetup -n %{name}-%{version} -p1

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install

%files -n python3-%{name}
%license LICENSE.txt
%doc README.md notes.txt
%{python3_sitearch}/%{name}%{python3_ext_suffix}
%{python3_sitearch}/%{name}-%{version}.dist-info/
%{python3_sitearch}/%{name}.pyi

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 5.1.0-5
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Adam Williamson <awilliam@redhat.com> - 5.1.0-2
- Backport PR #1361 to fix build with Python 3.13
- Rebuilt for Python 3.13

* Tue Feb 6 2024 Ondrej Sloup <osloup@redhat.com> - 5.1.0-1
- Rebase to the newest version (Related: rhbz#2262845)
- Update license tag to the SPDX format (MIT-0)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Oct 15 2023 Ondrej Sloup <osloup@redhat.com> - 5.0.1-1
- Rebase to the newest version (Related: rhbz#2244039)

* Thu Sep 28 2023 Ondrej Sloup <osloup@redhat.com> - 5.0.0~b4-1
- Rebase to the newest version, test the beta (Related: rhbz#2235401)
- Remove the hotfix (move of pyodbc.py) as it is fixed in upstream

* Mon Aug 28 2023 Ondřej Sloup <osloup@redhat.com> - 5.0.0~b1-2
- Move /usr/pyodbc.pyi to /usr/lib64/python3.X/site-packages/pyodbc.pyi as originally intended

* Mon Aug 28 2023 Ondřej Sloup <osloup@redhat.com> - 5.0.0~b1-1
- Rebase to the newest version, test the beta (rhbz#2235122)
- This release drops Python 2 and adds Python 3.12 support

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.39-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 4.0.39-3
- Rebuilt for Python 3.12

* Mon Apr 17 2023 Ondřej Sloup <osloup@redhat.com> - 4.0.39-1
- Rebase to the newest version
- Remove the PyUnicode_AsUTF8String Patch file, as it is already merged in upstream
- Change packaged files to match new setup.py requirements

* Wed Jan 25 2023 Miro Hrončok <mhroncok@redhat.com> - 4.0.30-10
- Fix version in the Python package metadata
- This makes the package provide python3dist(pyodbc) = 4.0.30 instead of python3dist(pyodbc) = 4.0.0-unsupported
- This makes the package buildable with python-packaging 22+

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.30-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.30-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 28 2022 Ondrej Sloup <osloup@redhat.com> - 4.0.30-7
- Use autosetup
- Use name macro
- Fix pyodbc fails to build with Python 3.11: error: PyUnicode_EncodeUTF8 (#2049428)

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 4.0.30-6
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.30-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.30-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.0.30-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Oct 2 2020 Filip Janus <fjanus@redhat.com> - 4.0.30-1
- Upstream released 4.0.30
- Add Recommendation to install database connector

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 4.0.27-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 23 2019 Filip Janus <fjanus@redhat.com> - 4.0.27-1
- Upstream released 4.0.27

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.0.10-19
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Miro Hrončok <mhroncok@redhat.com> - 3.0.10-16
- Subpackage python2-pyodbc has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.0.10-14
- Rebuilt for Python 3.7

* Wed Feb 14 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.0.10-13
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.0.10-11
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.0.10-10
- Python 2 binary package renamed to python2-pyodbc
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.0.10-6
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.10-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 12 2015 Orion Poplawski <orion@cora.wnra.com> - 3.0.10-1
- Update to 3.0.10

* Tue May 12 2015 Orion Poplawski <orion@cora.wnra.com> - 3.0.7-4
- Cleanup and update spec

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.0.7-3
- Rebuilt for GCC 5 C++11 ABI change

* Tue Feb 17 2015 Honza Horak <hhorak@redhat.com> - 3.0.7-2
- Start compiling for python3
  Thanks Ganapathi Kamath

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.7-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug 13 2012 Honza Horak <hhorak@redhat.com> - 3.0.6-1
- Upstream released 3.0.6
 
* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 22 2009 Ray Van Dolson <rayvd@fedoraproject.org> - 2.1.5-2
- EVR bump

* Wed Apr 22 2009 Ray Van Dolson <rayvd@fedoraproject.org> - 2.1.5-1
- Upstream released 2.1.5

* Mon Feb 23 2009 Ray Van Dolson <rayvd@fedoraproject.org> - 2.1.4-5
- Removing versioned BuildRequires

* Mon Feb 23 2009 Ray Van Dolson <rayvd@fedoraproject.org> - 2.1.4-4
- Changes for plague

* Sun Feb 22 2009 Ray Van Dolson <rayvd@fedoraproject.org> - 2.1.4-3
- Removed extraneous Requires

* Sun Feb 22 2009 Ray Van Dolson <rayvd@fedoraproject.org> - 2.1.4-2
- Added README.rst file from git repo

* Wed Jan 07 2009 Ray Van Dolson <rayvd@fedoraproject.org> - 2.1.4-1
- Upstream released 2.1.4

* Wed Dec 03 2008 Ray Van Dolson <rayvd@fedoraproject.org> - 2.1.1-1
- New upstream version and homepage

* Mon Jun 02 2008 Ray Van Dolson <rayvd@fedoraproject.org> - 2.0.58-3
- Removed silly python BuildRequires

* Mon Jun 02 2008 Ray Van Dolson <rayvd@fedoraproject.org> - 2.0.58-2
- Added python and python-devel to BuildRequires

* Fri May 30 2008 Ray Van Dolson <rayvd@fedoraproject.org> - 2.0.58-1
- Initial package
