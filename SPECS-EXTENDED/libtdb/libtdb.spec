Vendor:         Microsoft Corporation
Distribution:   Mariner

%global with_python3 1

Name: libtdb
Version: 1.4.3
Release: 4%{?dist}
Summary: The tdb library
License: LGPLv3+
URL: http://tdb.samba.org/
Source0: http://samba.org/ftp/tdb/tdb-%{version}.tar.gz
Source1: http://samba.org/ftp/tdb/tdb-%{version}.tar.asc
# gpg2 --no-default-keyring --keyring ./tdb.keyring --recv-keys 9147A339719518EE9011BCB54793916113084025
Source2: tdb.keyring
Source3: %{name}-LICENSE.txt

# Patches
Patch0001: 0003-wafsamba-Fix-few-SyntaxWarnings-caused-by-regular-ex.patch

BuildRequires: gcc
BuildRequires: gnupg2
BuildRequires: libxslt
BuildRequires: docbook-style-xsl
BuildRequires: which
%if 0%{?with_python3}
BuildRequires: python3-devel
%endif

Provides: bundled(libreplace)
Obsoletes: python2-tdb < 1.4.2-1

%description
A library that implements a trivial database.

%package devel
Summary: Header files need to link the Tdb library
Requires: libtdb = %{version}-%{release}

%description devel
Header files needed to develop programs that link against the Tdb library.

%package -n tdb-tools
Summary: Developer tools for the Tdb library
Requires: libtdb = %{version}-%{release}

%description -n tdb-tools
Tools to manage Tdb files

%if 0%{?with_python3}
%package -n python3-tdb
Summary: Python3 bindings for the Tdb library
Requires: libtdb = %{version}-%{release}
%{?python_provide:%python_provide python3-tdb}

%description -n python3-tdb
Python3 bindings for libtdb
%endif

%prep
%autosetup -n tdb-%{version} -p1
cp %{SOURCE3} ./LICENSE.txt

%build
zcat %{SOURCE0} | gpgv2 --quiet --keyring %{SOURCE2} %{SOURCE1} -
%configure --disable-rpath \
           --bundled-libraries=NONE \
           --builtin-libraries=replace

make %{?_smp_mflags} V=1

%check
make %{?_smp_mflags} check

%install
make install DESTDIR=$RPM_BUILD_ROOT

%files
%license LICENSE.txt
%{_libdir}/libtdb.so.*

%files devel
%doc docs/README
%{_includedir}/tdb.h
%{_libdir}/libtdb.so
%{_libdir}/pkgconfig/tdb.pc

%files -n tdb-tools
%{_bindir}/tdbbackup
%{_bindir}/tdbdump
%{_bindir}/tdbtool
%{_bindir}/tdbrestore
%{_mandir}/man8/tdbbackup.8*
%{_mandir}/man8/tdbdump.8*
%{_mandir}/man8/tdbtool.8*
%{_mandir}/man8/tdbrestore.8*

%if 0%{?with_python3}
%files -n python3-tdb
%{python3_sitearch}/__pycache__/_tdb_text.cpython*.py[co]
%{python3_sitearch}/tdb.cpython*.so
%{python3_sitearch}/_tdb_text.py
%endif

%ldconfig_scriptlets

%changelog
* Fri Dec 10 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.4.3-4
- License verified

* Tue Mar 02 2021 Henry Li <lihl@microsoft.com> - 1.4.3-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove distro condition check
- Add which as BuildRequires

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 22 2020 Lukas Slebodnik <lslebodn@fedoraproject.org> - 1.4.3-1
- rhbz#1783927 - libtdb-1.4.3 is available

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.4.2-2
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 26 2019 Lukas Slebodnik <lslebodn@fedoraproject.org> - 1.4.2-1
- rhbz#1691299 - libtdb-1.4.2 is available
- rhbz#1737644 - libldb, libtalloc, libtevent, libtdb: Remove Python 2 subpackages from Fedora 31+

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.3.18-5
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 14 2019 Lukas Slebodnik <lslebodn@fedoraproject.org> - 1.3.18-3
- rhbz#1718113 - samba fail to build with Python 3.8
  AttributeError: module 'time' has no attribute 'clock'

* Mon Jun 03 2019 Lukas Slebodnik <lslebodn@fedoraproject.org> - 1.3.18-2
- rhbz#1711638 - fails to build with Python 3.8.0a4

* Tue Feb 26 2019 Lukas Slebodnik <lslebodn@fedoraproject.org> - 1.3.18-1
- rhbz#1683185 - libtdb-1.3.18 is available

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Lukas Slebodnik <lslebodn@fedoraproject.org> - 1.3.17-1
- rhbz#1667472 - libtdb-1.3.17 is available

* Fri Jul 13 2018 Jakub Hrozek <jhrozek@redhat.com> - 1.3.16-2
- Drop the unneeded ABI hide patch
- Use pathfix.py instead of a local patch to munge the python path

* Thu Jul 12 2018 Jakub Hrozek <jhrozek@redhat.com> - 1.3.16-1
- New upstream release 1.3.16
- Apply a patch to hide local ABI symbols to avoid issues with new binutils
- Patch the waf script to explicitly call python2 as "env python" doesn't
  yield py2 anymore

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.3.15-5
- Rebuilt for Python 3.7

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1.3.15-3
- Rebuilt for switch to libxcrypt

* Thu Nov 30 2017 Lukas Slebodnik <lslebodn@fedoraproject.org> - 1.3.15-2
- Update spec file conditionals

* Sat Aug 26 2017 Lukas Slebodnik <lslebodn@redhat.com> - 1.3.15-1
- New upstream release 1.3.15

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul  3 2017 Lukas Slebodnik <lslebodn@redhat.com> - 1.3.14-1
- New upstream release 1.3.14
- run unittests

* Fri Apr 28 2017 Lukas Slebodnik <lslebodn@redhat.com> - 1.3.13-1
- New upstream release 1.3.13
- removed Group fields (new packaging policy)
- %%defattr() is no longer needed

* Tue Feb 14 2017 Lukas Slebodnik <lslebodn@redhat.com> - 1.3.12-5
- rhbz#1401175 - Missing symbol versioning provided by libtdb.so
- Fix configure time detection with -Werror=implicit-function-declaration
  -Werror=implicit-int
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.3.12-3
- Rebuild for Python 3.6

* Tue Dec  6 2016 Adam Williamson <awilliam@redhat.com> - 1.3.12-2
- rebuild with reverted redhat-rpm-config to fix missing library symbols

* Fri Dec  2 2016 Jakub Hrozek <jhrozek@redhat.com> - 1.3.12-1
- New upstream release 1.3.12

* Tue Aug 30 2016 Jakub Hrozek <jhrozek@redhat.com> - 1.3.11-1
- New upstream release 1.3.11

* Thu Jul 28 2016 Jakub Hrozek <jhrozek@redhat.com> - 1.3.10-1
- New upstream release 1.3.10

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.9-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Apr 27 2016 Jakub Hrozek <jhrozek@redhat.com> - 1.3.9-1
- New upstream release 1.3.9

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 11 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Nov 11 2015 Jakub Hrozek <jhrozek@redhat.com> - 1.3.8-1
- New upstream release 1.3.8

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Jul 22 2015 Jakub Hrozek <jhrozek@redhat.com> - 1.3.7-1
- New upstream release 1.3.7
- Build Python3 bindings

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 14 2015 Jakub Hrozek <jhrozek@redhat.com> - 1.3.6-1
- New upstream release 1.3.6

* Wed Apr 29 2015 Jakub Hrozek <jhrozek@redhat.com> - 1.3.5-1
- New upstream release 1.3.5

* Mon Jan  5 2015 Jakub Hrozek <jhrozek@redhat.com> - 1.3.4-1
- New upstream release 1.3.4

* Fri Dec  5 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.3.3-1
- New upstream release 1.3.3

* Thu Sep 18 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.3.1-1
- New upstream release 1.3.1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Adam Williamson <awilliam@redhat.com> - 1.3.0-2
- add a missing include to tdb.h (fixes builds against libtdb) (BSO #10625)

* Fri May 23 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.3.0-1
- New upstream release 1.3.0

* Thu Mar 20 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.2.13-1
- New upstream release 1.2.13

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 04 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.2.12-1
- New upstream release 1.2.12

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec 01 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.2.11-1
- New upstream release 1.2.11

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 22 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.2.10-15
- New upstream release 1.2.10
- Remove upstreamed patches
- Provides functionality for the upcoming Samba 4 beta

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.9-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 01 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-13
- Add patch to ignore --disable-silent-rules
- Include README documentation

* Wed Nov 23 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-12
- Add explicit mention of the bundled libreplace
- https://fedorahosted.org/fpc/ticket/120


* Wed Nov 09 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-11
- Rebuild for F17 due to bz#744766

* Tue Apr  5 2011 Simo Sorce <ssorce@redhat.com> - 1.2.9-9
- Add patch to limit database expansion, was causing OOMs in SSSD in some
  extreme situations.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 14 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-8
- Actually fix the verbosity

* Fri Jan 14 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-7
- Let rpmbuild strip binaries, make build more verbose.
- Original patch by Ville SkyttÃ¤ <ville.skytta@iki.fi>

* Wed Jan 12 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-6
- Install python bindings into the correct location

* Tue Jan 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-5
- Run ldconfig on python-tdb

* Tue Jan 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-4
- Do not delete a necessary file during %%install

* Tue Jan 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-3
- Bump release to rebuild with the correct sources in place

* Tue Jan 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-2
- Bump build to rebuild with sources in place

* Tue Jan 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-1
- New upstream bugfix release
- Adds a new tdbrestore utility
- Convert to new WAF build-system
- Add python bindings in new python-tdb subpackage

* Wed Feb 24 2010 Simo Sorce <ssorce@redhat.com> - 1.2.1-3
- add missing build require

* Wed Feb 24 2010 Simo Sorce <ssorce@redhat.com> - 1.2.1-2
- Fix spec file
- Package manpages too

* Wed Feb 24 2010 Simo Sorce <ssorce@redhat.com> - 1.2.1-1
- New upstream bugfix release

* Tue Dec 15 2009 Simo Sorce <ssorce@redhat.com> - 1.2.0-1
- New upstream release

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Simo Sorce <ssorce@redhat.com> - 1.1.5-1
- Original tarballs had a screw-up, rebuild with new fixed tarballs from
  upstream.

* Tue Jun 16 2009 Simo Sorce <ssorce@redhat.com> - 1.1.5-0
- New upstream release

* Wed May 6 2009 Simo Sorce <ssorce@redhat.com> - 1.1.3-15
- First public independent release from upstream
