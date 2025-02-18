%global gitver 0

%if 0%{?gitver}
%global  commit      f0a089a12dca9e2fd9543c8e8086ac70f7058513
%global  date        .20210630git
%global  shortcommit %(c=%{commit}; echo ${c:0:8})
%else
%global  commit      %{nil}
%global  date        %{nil}
%global  shortcommit %{nil}
%endif

Name: python-dmidecode
Summary: Python module to access DMI data
Version: 3.12.3
Release: 9%{date}%{shortcommit}%{?dist}
License: GPL-2.0-only
URL: https://github.com/nima/python-dmidecode
Source0: %{url}/archive/%{version}/%{name}-%{version}.tar.gz

Patch0: python-dmidecode-rhbz2154949.patch

BuildRequires: make
BuildRequires: gcc
BuildRequires: libxml2-devel
BuildRequires: python3-devel
BuildRequires: libxml2-python3
BuildRequires: python3-setuptools
BuildRequires: python-distutils-extra

%global _description\
python-dmidecode is a python extension module that uses the\
code-base of the 'dmidecode' utility, and presents the data\
as python data structures or as XML data using libxml2.\
\


%description %_description

%package -n python3-dmidecode
Summary: Python 3 module to access DMI data
Requires: libxml2-python3

%description -n python3-dmidecode %_description


%prep
%autosetup -n %{name}-%{version} -N
%patch 0 -p1 -b .backup

%build
# -std=gnu89 is there to avoid `undefined symbol: dmixml_GetContent`
export PYTHON_BIN=%{__python3}
export CFLAGS="%{build_cflags} -std=gnu89"
export CXXFLAGS="%{build_cxxflags} -std=gnu89"
export CC=gcc
export CXX=g++
%make_build

%install
%{__python3} src/setup.py install --root %{buildroot} --prefix=%{_prefix}


%check
export PYTHONPATH=%{buildroot}%{python3_sitearch}
export PYTHON_BIN=%{__python3}
make -C unit-tests


%files -n python3-dmidecode
%license doc/LICENSE
%doc README doc/AUTHORS doc/AUTHORS.upstream
%{python3_sitearch}/dmidecodemod.cpython-%{python3_version_nodots}*.so
%pycached %{python3_sitearch}/dmidecode.py
%{python3_sitearch}/*.egg-info
%{_datadir}/%{name}/

%changelog
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.12.3-8
- Rebuilt for Python 3.13

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 10 2023 Lichen Liu <lichliu@redhat.com> - 3.12.3-6
- Use SPDX identifiers for license

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 3.12.3-4
- Rebuilt for Python 3.12

* Sat May 20 2023 Antonio Trande <sagitter@fedoraproject.org> - 3.12.3-3
- Fix BuildRequires packages for Python-3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Dec 25 2022 Antonio Trande <sagitter@fedoraproject.org> - 3.12.3-1
- Release 3.12.3
- Temporary fix for rhbz#2154949

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.2-29.20210630gitf0a089a1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 3.12.2-28.20210630gitf0a089a1
- Rebuilt for Python 3.11

* Sun Apr 24 2022 Antonio Trande <sagitter@fedoraproject.org> - 3.12.2-27.20210630gitf0a089a1
- Build commit #f0a089a1 (include covscan error fixes)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.2-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.2-25
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.12.2-24
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.2-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 26 2020 Antonio Trande <sagitter@fedoraproject.org> - 3.12.2-22
- Refresh SPEC file
- Fixed for Python-3.10 (rhbz#1898981)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 3.12.2-20
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.12.2-18
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.12.2-17
- Rebuilt for Python 3.8

* Sun Aug 11 2019 Miro Hrončok <mhroncok@redhat.com> - 3.12.2-16
- Subpackage python2-dmidecode has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.12.2-12
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 16 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.12.2-10
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.12.2-9
- Python 2 binary package renamed to python2-dmidecode
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.12.2-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.2-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Nov 07 2015 Robert Kuska <rkuska@redhat.com> - 3.12.2-2
- Rebuilt for Python3.5 rebuild

* Fri Jul 10 2015 Miro Hrončok <mhroncok@redhat.com> - 3.12.2-1
- Update to 3.12.2
- Add Python 3 subpackage (#1236000)
- Removed deprecated statements
- Moved some docs to license
- Removed pacthes
- Corrected bogus dates in %%changelog
- Build with -std=gnu89

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.13-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.13-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 20 2013 Ales Ledvinka <aledvink@redhat.com> - 3.10.13-9
- Attribute installed may appear as duplicate and cause invalid XML.

* Mon Jun 17 2013 Ales Ledvinka <aledvink@redhat.com> - 3.10.13-8
- Attribute dmispec may cause invalid XML on some hardware.
- Signal handler for SIGILL.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 19 2012 Ales Ledvinka <aledvink@redhat.com> 3.10.14-5
- Upstream relocated. Document source tag and tarball generation.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 3.10.13-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jun 15 2010 Roman Rakus <rrakus@redhat.com> - 3.10.13-1
- Update to new release

* Fri Mar 12 2010 Nima Talebi <nima@it.net.au> - 3.10.12-1
- Update to new release

* Tue Feb 16 2010 Nima Talebi <nima@it.net.au> - 3.10.11-1
- Update to new release

* Tue Jan 12 2010 Nima Talebi <nima@it.net.au> - 3.10.10-1
- Update to new release

* Thu Jan 07 2010 Nima Talebi <nima@it.net.au> - 3.10.9-1
- Update to new release


* Tue Dec 15 2009 Nima Talebi <nima@it.net.au> - 3.10.8-1
- New Upstream release.
- Big-endian and little-endian approved.
- Packaged unit-test to tarball.
- Rewritten unit-test to be able to run as non-root user, where it will not
  try to read /dev/mem.
- Added two dmidump data files to the unit-test.

* Thu Nov 26 2009 David Sommerseth <davids@redhat.com> - 3.10.7-3
- Fixed even more .spec file issues and removed explicit mentioning
  of /usr/share/python-dmidecode/pymap.xml

* Wed Nov 25 2009 David Sommerseth <davids@redhat.com> - 3.10.7-2
- Fixed some .spec file issues (proper Requires, use _datadir macro)

* Wed Sep 23 2009 Nima Talebi <nima@it.net.au> - 3.10.7-1
- Updated source0 to new 3.10.7 tar ball

* Mon Jul 13 2009 David Sommerseth <davids@redhat.com> - 3.10.6-6
- Only build the python-dmidecode module, not everything

* Mon Jul 13 2009 David Sommerseth <davids@redhat.com> - 3.10.6-5
- Added missing BuildRequres for libxml2-python

* Mon Jul 13 2009 David Sommerseth <davids@redhat.com> - 3.10.6-4
- Added missing BuildRequres for python-devel

* Mon Jul 13 2009 David Sommerseth <davids@redhat.com> - 3.10.6-3
- Added missing BuildRequres for libxml2-devel

* Mon Jul 13 2009 David Sommerseth <davids@redhat.com> - 3.10.6-2
- Updated release, to avoid build conflict

* Wed Jun 10 2009 David Sommerseth <davids@redhat.com> - 3.10.6-1
- Updated to work with the new XML based python-dmidecode

* Sat Mar  7 2009 Clark Williams <williams@redhat.com> - 2.10.3-1
- Initial build.

