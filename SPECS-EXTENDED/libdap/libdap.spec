Name: libdap
Summary: The C++ DAP2 library from OPeNDAP
Version: 3.20.5
Release: 2%{?dist}

License: LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL: https://www.opendap.org/
Source0: https://www.opendap.org/pub/source/libdap-%{version}.tar.gz
#Don't run HTTP tests - builders don't have network connections
Patch0: libdap-offline.patch

BuildRequires: gcc-c++
# For autoreconf
BuildRequires: libtool
BuildRequires: bison >= 3.0
BuildRequires: cppunit-devel
BuildRequires: curl-devel
BuildRequires: doxygen
BuildRequires: flex
BuildRequires: graphviz
BuildRequires: libtirpc-devel
BuildRequires: libuuid-devel
BuildRequires: libxml2-devel
BuildRequires: openssl-devel
BuildRequires: pkgconfig
%ifnarch s390 %{mips}
BuildRequires: valgrind
%endif

Provides: bundled(gnulib)


%description
The libdap++ library contains an implementation of DAP2. This package
contains the library, dap-config, and getdap. The script dap-config
simplifies using the library in other projects. The getdap utility is a
simple command-line tool to read from DAP2 servers. It is built using the
library and demonstrates simple uses of it.


%package devel
Summary: Development and header files from libdap
Requires: %{name} = %{version}-%{release}
Requires: curl-devel
Requires: libxml2-devel
Requires: pkgconfig
# for the /usr/share/aclocal directory ownership
Requires: automake

%description devel
This package contains all the files needed to develop applications that
will use libdap.


%package doc
Summary: Documentation of the libdap library

%description doc
Documentation of the libdap library.


%prep
%autosetup -n %{name}-%{version} -p1
iconv -f latin1 -t utf8 < COPYRIGHT_W3C > COPYRIGHT_W3C.utf8
touch -r COPYRIGHT_W3C COPYRIGHT_W3C.utf8
mv COPYRIGHT_W3C.utf8 COPYRIGHT_W3C


%build
# To fix rpath
autoreconf -f -i
%configure --disable-static --disable-dependency-tracking
# --enable-valgrind - missing valgrind exclusions file
%make_build

make docs


%install
%make_install INSTALL="%{__install} -p"
mkdir -p $RPM_BUILD_ROOT%{_libdir}/libdap
mv $RPM_BUILD_ROOT%{_libdir}/libtest-types.a $RPM_BUILD_ROOT%{_libdir}/libdap/
rm $RPM_BUILD_ROOT%{_libdir}/*.la
mv $RPM_BUILD_ROOT%{_bindir}/dap-config-pkgconfig $RPM_BUILD_ROOT%{_bindir}/dap-config

rm -rf __dist_docs
cp -pr html __dist_docs
# those .map and .md5 are of dubious use, remove them
rm -f __dist_docs/*.map __dist_docs/*.md5
# use the ChangeLog timestamp to have the same timestamps for the doc files 
# for all arches
touch -r ChangeLog __dist_docs/*


%check
# tarball is missing some needed files
make check || :


%ldconfig_scriptlets


%files
%license COPYRIGHT_W3C COPYING COPYRIGHT_URI
%doc README NEWS README.dodsrc
%{_bindir}/getdap
%{_bindir}/getdap4
%{_libdir}/libdap.so.25*
%{_libdir}/libdapclient.so.6*
%{_libdir}/libdapserver.so.7*
%{_mandir}/man1/getdap.1*
%{_mandir}/man1/getdap4.1*

%files devel
%{_libdir}/libdap.so
%{_libdir}/libdapclient.so
%{_libdir}/libdapserver.so
%{_libdir}/libdap/
%{_libdir}/pkgconfig/libdap*.pc
%{_bindir}/dap-config
%{_includedir}/libdap/
%{_datadir}/aclocal/*
%{_mandir}/man1/dap-config.1*

%files doc
%license COPYING COPYRIGHT_URI COPYRIGHT_W3C
%doc __dist_docs/


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.20.5-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Sat Feb 08 2020 Orion Poplawski <orion@nwra.com> - 3.20.5-1
- Update to 3.20.5

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.20.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jul 29 2019 Orion Poplawski <orion@nwra.com> - 3.20.4-1
- Update to 3.20.4

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.20.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Orion Poplawski <orion@nwra.com> - 3.20.3-1
- Update to 3.20.3

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Orion Poplawski <orion@nwra.com> - 3.19.1-1
- Update to 3.19.1
- Add patch to use libtirpc
- Add BR gcc-c++

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 11 2017 Orion Poplawski <orion@cora.nwra.com> - 3.18.3-1
- Update to 3.18.3

* Tue Dec 6 2016 Orion Poplawski <orion@cora.nwra.com> - 3.18.2-1
- Update to 3.18.2
- Drop getopt and big endian baselines patches applied upstream

* Fri Aug 26 2016 Dan Horák <dan[at]danny.cz> - 3.18.1-2
- Add missing big endian baselines (#1366787)

* Fri Aug 12 2016 Orion Poplawski <orion@cora.nwra.com> - 3.18.1-1
- Update to 3.18.1
- Add patch to fix getopt usage again

* Thu Aug 11 2016 Michal Toman <mtoman@fedoraproject.org> - 3.17.2-2
- No valgrind on MIPS

* Fri Apr 15 2016 Than Ngo <than@redhat.com> - 3.17.2-1
- update to 3.17.2

* Fri Apr 15 2016 Dan Horák <dan[at]danny.cz> - 3.17.1-1
- Update to 3.17.1
- Switch to github for source archive
- Add missing big endian baselines (#1325114)

* Tue Feb 9 2016 Orion Poplawski <orion@cora.nwra.com> - 3.17.0-1
- Update to 3.17.0
- Add patch for gcc 6 support

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 14 2016 Orion Poplawski <orion@cora.nwra.com> - 3.16.0-1
- Update to 3.16.0

* Wed Sep 23 2015 Orion Poplawski <orion@cora.nwra.com> - 3.15.1-1
- Update to 3.15.1
- Drop flex, getopt, and include patches fixed upstream

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.14.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Dan Horák <dan[at]danny.cz> - 3.14.0-4
- valgrind available only on selected arches

* Fri Apr 17 2015 Orion Poplawski <orion@cora.nwra.com> - 3.14.0-3
- Add patch to add needed includes

* Fri Apr 17 2015 Orion Poplawski <orion@cora.nwra.com> - 3.14.0-2
- Ship libtest-types.a for dependent package tests

* Thu Apr 16 2015 Orion Poplawski <orion@cora.nwra.com> - 3.14.0-1
- Update to 3.14.0
- Add patch to fix flex compilation
- Add patch to fix getopt usage
- Update offline patch for new test

* Mon Feb 23 2015 Orion Poplawski <orion@cora.nwra.com> - 3.13.3-1
- Update to 3.13.3

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 15 2014 Orion Poplawski <orion@cora.nwra.com> - 3.13.1-2
- Add patch to fix tests on ppc and arm

* Wed Jul 9 2014 Orion Poplawski <orion@cora.nwra.com> - 3.13.1-1
- Update to 3.13.1
- Run autoreconf to fix rpaths

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 29 2013 Orion Poplawski <orion@cora.nwra.com> - 3.11.7-1
- Update to 3.11.7
- Drop gcc47 patch applied upstream
- spec cleanup
- Add BR openssl-devel

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 15 2012 Orion Poplawski <orion@cora.nwra.com> - 3.11.3-1
- Update to 3.11.3
- Drop curl and test patches applied upstream
- Add Provides: bundled(gnulib) (bug 821766)

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11.1-5
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Orion Poplawski <orion@cora.nwra.com> - 3.11.1-4
- Add patch to compile with gcc 4.7

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 28 2011 Orion Poplawski <orion@cora.nwra.com> - 3.11.1-2
- Add upstream patch to fix failing test

* Tue Nov 22 2011 Orion Poplawski <orion@cora.nwra.com> - 3.11.1-1
- Update to 3.11.1
- Add patch for current libcurl

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 10 2010 Orion Poplawski <orion@cora.nwra.com> - 3.11.0-1
- Update to 3.11.0
- Drop libuuid patch fixed upstream
- Drop soname patch

* Thu Jul 15 2010 Orion Poplawski <orion@cora.nwra.com> - 3.10.2-3
- Add patch to bump soname as this dropped the AIS* functions
- Add BR cppunit-devel and %%check section
- Add patch to not run HTTP network tests

* Wed Jul 14 2010 Orion Poplawski <orion@cora.nwra.com> - 3.10.2-2
- Add patch to remove -luuid from pkg-config libs

* Tue Jul 13 2010 Orion Poplawski <orion@cora.nwra.com> - 3.10.2-1
- Update to 3.10.2
- Deflate is no longer shipped
- Drop includes patch fixed upstream
- Add license to doc sub-package

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Orion Poplawski <orion@cora.nwra.com> - 3.9.3-1
- Update to 3.9.3

* Tue Mar  3 2009 Caolán McNamara <caolanm@redhat.com> - 3.8.2-3
- include cstdio for std::sprintf

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep  5 2008 Patrice Dumas <pertusus@free.fr> 3.8.2-1
- update to 3.8.2

* Sun Mar 16 2008 Patrice Dumas <pertusus@free.fr> 3.8.0-1
- update to 3.8.0

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.7.10-3
- Autorebuild for GCC 4.3

* Wed Jan  2 2008 Patrice Dumas <pertusus@free.fr> 3.7.10-2
- use pkg-config in dap-config

* Mon Dec 17 2007 Patrice Dumas <pertusus@free.fr> 3.7.10-1
- update to 3.7.10

* Sun Oct 21 2007 Patrice Dumas <pertusus@free.fr> 3.7.8-3
- remove reference to libdir in dap-config

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 3.7.8-2
- Rebuild for selinux ppc32 issue.

* Thu Jul  5 2007 Patrice Dumas <pertusus@free.fr> 3.7.8-1.1
- update to 3.7.8

* Thu May 31 2007 Patrice Dumas <pertusus@free.fr> 3.7.7-1.1
- update to 3.7.7

* Sat May 12 2007 Patrice Dumas <pertusus@free.fr> 3.7.6-4
- remove static libs
- set the same doc file timestamps for all arches

* Mon Apr 30 2007 Patrice Dumas <pertusus@free.fr> 3.7.6-3
- correct the library install order
- keep timestamps
- add documentation in a subpackage

* Mon Apr 30 2007 Patrice Dumas <pertusus@free.fr> 3.7.6-2
- update to 3.7.6

* Tue Oct 31 2006 Patrice Dumas <pertusus@free.fr> 3.7.2-3
- rebuild for new libcurl soname

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 3.7.2-2
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Patrice Dumas <pertusus@free.fr> 3.7.2-1
- update to 3.7.2

* Wed Sep  6 2006 Patrice Dumas <pertusus@free.fr> 3.7.1-1
- update to 3.7.1
- set licence to LGPL instead of W3C/LGPL, since only deflate is W3C, so
  the whole is under the LGPL

* Fri Jul 21 2006 Patrice Dumas <pertusus@free.fr> 3.7.0-1
- update to 3.7.0

* Mon Feb 27 2006 James Gallagher <jgallagher@opendap.org> - 3.6.0-1
- update to 3.6.0

* Mon Nov 21 2005 Patrice Dumas <pertusus@free.fr> - 3.5.3-2
- fix Source0

* Tue Aug 30 2005 Patrice Dumas <pertusus@free.fr> - 3.5.2-3
- Add missing Requires

* Sat Jul  2 2005 Patrice Dumas <pertusus@free.fr> - 3.5.1-2
- Support for shared libraries
- Add COPYING
- Update with fedora template

* Thu May 12 2005 James Gallagher <jimg@comet.opendap.org> - 3.5.0-1
- Changed: Requires xml2 to libxml2

* Wed May 11 2005 James Gallagher <jimg@zoey.opendap.org> 3.5.0-1
- Removed version numbers from .a and includes directory.

* Tue May 10 2005 James Gallagher <jimg@zoey.opendap.org> 
- Mostly works. Problems: Not sure if the %%post script stuff works.
- Must also address the RHEL3 package deps issue (curl 7.12.0 isn't available;
  not sure about xml2 2.5.7). At least the deps fail when they are not present!

* Fri May  6 2005 James Gallagher <jimg@zoey.opendap.org> 
- Initial build.
