# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define __cmake_in_source_build 1

Name:           libcomps
Version:        0.1.23
Release:        1%{?dist}
Summary:        Comps XML file manipulation library

License:        GPL-2.0-or-later
URL:            https://github.com/rpm-software-management/libcomps
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake >= 3.10
BuildRequires:  gcc
BuildRequires:  libxml2-devel
BuildRequires:  check-devel
BuildRequires:  expat-devel
BuildRequires:  zlib-devel

%description
Libcomps is library for structure-like manipulation with content of
comps XML files. Supports read/write XML file, structure(s) modification.

%package devel
Summary:        Development files for libcomps library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for libcomps library.

%package doc
Summary:        Documentation files for libcomps library
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch
BuildRequires:  doxygen

%description doc
Documentation files for libcomps library.

%package -n python-%{name}-doc
Summary:        Documentation files for python bindings libcomps library
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch
BuildRequires:  python3-sphinx


%description -n python-%{name}-doc
Documentation files for python bindings libcomps library.

%package -n python3-%{name}
Summary:        Python 3 bindings for libcomps library
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  make
%{?python_provide:%python_provide python3-%{name}}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      platform-python-%{name} < %{version}-%{release}

%description -n python3-%{name}
Python3 bindings for libcomps library.

%prep
%autosetup -p1 -n %{name}-%{version}

mkdir build-py3
mkdir build-doc

%build
pushd build-py3
  %cmake ../libcomps/
  %cmake_build
popd

pushd build-doc
  %cmake ../libcomps/
  %cmake_build -t docs
  %cmake_build -t pydocs
popd

%install
pushd build-py3
  %cmake_install
popd

%check
pushd build-py3
  %cmake_build -t test
  %cmake_build -t pytest
popd

%if %{undefined ldconfig_scriptlets}
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%else
%ldconfig_scriptlets
%endif

%files
%license COPYING
%doc README.md
%{_libdir}/%{name}.so.*

%files devel
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/

%files doc
%doc build-doc/docs/libcomps-doc/html

%files -n python-%{name}-doc
%doc build-doc/src/python/docs/html

%files -n python3-%{name}
%{python3_sitearch}/%{name}/
%{python3_sitearch}/%{name}-%{version}-py%{python3_version}.egg-info

%changelog
* Thu Sep 11 2025 Marek Blaha <mblaha@redhat.com> - 0.1.23-1
- Update to 0.1.23

* Mon Aug 18 2025 Petr Pisar <ppisar@redhat.com> - 0.1.22-1
- 0.1.22 bump

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.1.21-8
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.21-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.1.21-6
- Rebuilt for Python 3.14

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Dec 11 2024 Miro Hrončok <mhroncok@redhat.com> - 0.1.21-4
- Python: Return self from iter(iterator) to prevent a segfault
- Fixes: rhbz#2331665

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.1.21-2
- Rebuilt for Python 3.13

* Sat Apr 20 2024 Sérgio Basto <sergio@serjux.com> - 0.1.21-1
- Update libcomps to 0.1.21 (#2269210)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Florian Weimer <fweimer@redhat.com> - 0.1.20-3
- Backport upstream patch to fix C compatibility issue

* Wed Dec 13 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 0.1.20-2
- Fix build with libxml2-2.12.0

* Thu Oct 05 2023 Jan Kolarik <jkolarik@redhat.com> - 0.1.20-1
- Update to 0.1.20
- Fixes of xml parsing
- Fix non-optimized builds by removing inline keyword
- Use Py_hash_t instead of long

* Wed Oct 04 2023 Mattia Verga <mattia.verga@proton.me> - 0.1.19-5
- Backport additional patch to fix segfault in fromxml_str

* Tue Sep 05 2023 Mattia Verga <mattia.verga@proton.me> - 0.1.19-4
- Backport patch to fix segfault in fromxml_str

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 0.1.19-2
- Rebuilt for Python 3.12

* Tue Feb 28 2023 Sérgio Basto <sergio@serjux.com> - 0.1.19-1
- Update libcomps to 0.1.19
- Migrated to SPDX license

* Tue Feb 28 2023 Miro Hrončok <mhroncok@redhat.com> - 0.1.18-6
- BuildRequire python3-setuptools explicitly, don't assume they are pulled transitively

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.1.18-3
- Rebuilt for Python 3.11

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Sep 23 2021 Pavla Kratochvilova <pkratoch@redhat.com> - 0.1.18-1
- Update to 0.1.18
- Fix several covscan warnings

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 15 2021 Pavla Kratochvilova <pkratoch@redhat.com> - 0.1.17-1
- Update to 0.1.17
- Fix a crash when clearing COMPS_ObjRTree (RhBug:1888343)
- Don't print empty requires
- Fix memory leaks and resource leaks
- Remove Python 2 support

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 0.1.15-7
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Aug 07 2020 Nicola Sella <nsella@redhat.com> - 0.1.15-5
- spec: Fix building with new cmake macros

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.15-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 0.1.15-2
- Rebuilt for Python 3.9

* Wed Apr 01 2020 Ales Matej <amatej@redhat.com> - 0.1.15-1
- Update to 0.1.15
- Do not skip type=mandatory in xml output (RhBug:1771224)

* Fri Jan 31 2020 Ales Matej <amatej@redhat.com> - 0.1.14-4
- Fix global header variable defined without extern for gcc-10

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Dec 14 2019 Jeff Law <law@redhat.com> - 0.1.14-2
- Fix inline vs static inline issue for gcc-10

* Fri Nov 29 2019 Ales Matej <amatej@redhat.com> - 0.1.14-1
- Update to 0.1.14

* Fri Nov 29 2019 Ales Matej <amatej@redhat.com> - 0.1.12-1
- Update to 0.1.12

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.1.11-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 0.1.11-4
- Rebuilt for Python 3.8

* Wed Jul 31 2019 Miro Hrončok <mhroncok@redhat.com> - 0.1.11-3
- Fix Python method descriptors for Python 3.8 (#1734777)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 11 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 0.1.11-1
- Update to 0.1.11

* Wed Feb 13 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 0.1.10-1
- Update to 0.1.10

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 27 2018 Marek Blaha <mblaha@redhat.com> - 0.1.8-15
- Disable Python 2 bindings for Fedora >= 30

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 0.1.8-13
- Rebuilt for Python 3.7

* Tue Feb 20 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.1.8-12
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Igor Gnatenko <ignatenko@redhat.com> - 0.1.8-10
- Switch to %%ldconfig_scriptlets

* Tue Nov 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.1.8-9
- Use better Obsoletes for platform-python

* Fri Nov 03 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.1.8-8
- Remove platform-python subpackage

* Fri Sep 01 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.1.8-7
- Disable platform python on old releases

* Thu Aug 10 2017 Lumír Balhar <lbalhar@redhat.com> - 0.1.8-6
- Add Platform Python subpackage (https://fedoraproject.org/wiki/Changes/Platform_Python_Stack)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 0.1.8-2
- Rebuild for Python 3.6

* Thu Sep 22 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.1.8-1
- Update to 0.1.8

* Tue Aug 09 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.1.7-6
- Add %%{?system_python_abi}

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.7-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Apr 12 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.1.7-4
- Adopt to new packaging guidelines
- Use %%license macro
- Fix file ownerships

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 0.1.7-2
- Rebuilt for Python3.5 rebuild

* Thu Jul 02 2015 Jindrich Luza <jluza@redhat.com> 0.1.7
- added langpacks to union process
- comps DOCTYPE read-write-read fix
- support biarchonly attribute
- fixed rhbz#1073885 rhbz#1073890 rhbz#1073907 rhbz#1073979
- fix rhbz#1073079
- comps_*_match() now support fnmatching
- added libpycomps.MATCH_IGNORECASE as matching flag
- added group.packages_match
- added comps.groups_match, comps.categories_match, comps.entironments_match
- PyCOMPS_Package hash
- cmake-2.6, python-2.6, RHEL-6 compatible
- '_arch' attribute change to 'arch'
- empty 'arch' attribute will be ommited from output from now

* Wed Jan 29 2014 Jindrich Luza <jluza@redhat.com> 0.1.6
- version bumped
- added libcomps.MDict.keys()
-         libcomps.MDict.values()
-         libcomps.MDict.items()
-         libcomps.MDict.clear()
-         libcomps.MDict.update()
-         libcomps.MDict.copy()
- COMPS_List replaced with COMPS_HSList
- added missing basearchonly to DocGroupPackage
- python3/CMakeLists.txt fixed
- added explicit attributes support for xml options
- added arch_filter test for python
- insert method in libcomps.Sequence
- Unioning is now accomplished with replace x append policy
- Weaker package equality check (comparing only name now)
- Fixed leeks in unioning
- modified test_merge_comps test_libcomps
- dictionaries are now storing keys in alphabetical order
- comps parser redesigned
- change python/tests directory composition
- added elem attributes check in parser
- xml output '_arch' attribute support
- parser and xml output defaults options for specify defaults values
- comps object validation in python
- added validity checker before append/set object to list (python only)
- .validate() method
- added libcomps.Dict.keys
-         libcomps.Dict.values
-         libcomps.Dict.items
-         libcomps.Dict.clear
-         libcomps.Dict.update
-         libcomps.Dict.copy
- added xml output options (comps.xml_str([options = {}]), comps.xml_f(options = {}))

* Wed Oct 23 2013 Jindrich Luza <jluza@redhat.com> 0.1.4-4
- group.uservisible is true by default now.
- fixed comps_mobjradix parent node problem
- implemented bindings for blacklist, whiteout and langpacks
- COMPS_Logger redesigned

* Tue Oct 08 2013 Jindrich Luza <jluza@redhat.com> 0.1.5
- version bump
- PyCOMPS_Sequence.__getitem__["objectid"] implemented for libcomps.GroupList, libcomps.CategoryList, libcomps.EnvList
- added missing files
- missing display_order fix for libcomps.Environment

* Tue Oct 01 2013 Jindrich Luza <jluza@redhat.com> 0.1.4
- added missing files
- architectural redesign finished
- fixed #1003986 by Gustavo Luiz Duarte guidelines (but not tested on ppc)
- fixed bug #1000449
- fixed bug #1000442
- added GroupId.default test
- some minor unreported bugs discovered during testing fixed
- finished default attribute support in groupid object
- Comps.get_last_parse_errors and Comps.get_last_parse_log has been renamed
-   as Comps.get_last_errors and Comps.get_last_log
- version bumped. Python bindings is now easier.
- added missing files

* Tue Aug 20 2013 Jindrich Luza <jluza@redhat.com> 0.1.3
- finished default attribute support in groupid object
- Comps.get_last_parse_errors and Comps.get_last_parse_log has been renamed
-   as Comps.get_last_errors and Comps.get_last_log
- finished default attribute support in groupid object
- Comps.get_last_parse_errors and Comps.get_last_parse_log has been renamed
-   as Comps.get_last_errors and Comps.get_last_log

* Thu Jul 18 2013 Jindrich Luza <jluza@redhat.com> 0.1.2
- automatic changelog system
- fixed issue #14
- libcomps.Dict is now behave more like python dict. Implemented iter(libcomps.Dict)
- libcomps.iteritems() and libcomps.itervalues()
- remaked error reporting system.
-     libcomps.Comps.fromxml_f and libcomps.Comps.fromxml_str now return
-     -1, 0 or 1. 0 means parse procedure completed without any problem,
-     1 means there's some errors or warnings but not fatal. -1 indicates
-     fatal error problem (some results maybe given, but probably incomplete
-     and invalid)
- errors catched during parsing can be obtained by calling
-     libcomps.Comps.get_last_parse_errors
- all log is given by
-     libcomps.Comps.get_last_parse_log
- prop system complete
- fixed issue 1
- fixed issue 3
- added <packagereq requires=...> support
- new prop system in progress....
- separated doc package
- some minor fixes in CMakeFiles
- improved integrated tests

* Tue Jun 25 2013 Jindrich Luza <jluza@redhat.com> 0.1.1-1
- Automatic commit of package [libcomps] release [0.1.1-1].

