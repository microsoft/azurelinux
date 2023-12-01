Vendor:         Microsoft Corporation
Distribution:   Mariner
Name: libwvstreams
Version: 4.6.1
Release: 34%{?dist}
Summary: WvStreams is a network programming library written in C++
Source: http://wvstreams.googlecode.com/files/wvstreams-%{version}.tar.gz
#fixed multilib issue (bug #192717)
Patch1: wvstreams-4.6.1-multilib.patch
#install-xplc target was missing
Patch2: wvstreams-4.5-noxplctarget.patch
#Fix parallel build (#226061)
Patch3: wvstreams-4.6.1-make.patch
#sys/stat.h is missing some files in rawhide build
Patch4: wvstreams-4.6.1-statinclude.patch
#const X509V3_EXT_METHOD * -> X509V3_EXT_METHOD * conversion not allowed
#by rawhide gcc
Patch5: wvstreams-4.6.1-gcc.patch
# fix missing unistd.h header for gcc 4.7
Patch6: wvstreams-4.6.1-gcc47.patch
Patch7: wvstreams-4.6.1-magic.patch
Patch8: 0001-Use-explicit-cast-and-prevent-compiler-error.patch
Patch9: wvstreams-4.6.1-fix-stack-size.patch
Patch10: wvstreams-4.6.1-gcc10.patch
Patch11: wvstreams-4.6.1-openssl11.patch
URL: https://code.google.com/p/wvstreams/
BuildRequires:  gcc-c++
BuildRequires:  openssl-devel, pkgconfig, zlib-devel, readline-devel, dbus-devel
License: LGPLv2+

%description
WvStreams aims to be an efficient, secure, and easy-to-use library for
doing network applications development.

%package devel
Summary: Development files for WvStreams
Requires: %{name} = %{version}-%{release}

%description devel
WvStreams aims to be an efficient, secure, and easy-to-use library for
doing network applications development.  This package contains the files
needed for developing applications which use WvStreams.

%package static
Summary: Static libraries files for WvStreams

%description static
WvStreams aims to be an efficient, secure, and easy-to-use library for
doing network applications development. This package contains static libraries.

%prep
%setup -q -n wvstreams-%{version}
%patch1 -p1 -b .multilib
%patch2 -p1 -b .xplctarget
%patch3 -p1 -b .make
%patch4 -p1 -b .statinclude
%patch5 -p1 -b .gcc
%patch6 -p1 -b .gcc47
%patch7 -p1 -b .magic
%patch8 -p1 -b .cast
%patch9 -p1 -b .fix-stack-size
%patch10 -p1 -b .gcc10
%patch11 -p1 -b .openssl11

%build

export CXXFLAGS="$RPM_OPT_FLAGS -fPIC -fpermissive -fno-strict-aliasing -fno-tree-dce -fno-optimize-sibling-calls"
export CFLAGS="$RPM_OPT_FLAGS -fPIC -fno-strict-aliasing"

#  --without-PACKAGE       do not use PACKAGE (same as --with-PACKAGE=no)
#  --with-dbus             DBUS
#  --with-openssl          OpenSSL >= 0.9.7 (required)
#  --with-pam              PAM
#  --with-tcl              Tcl
#  --with-qt               Qt
#  --with-zlib             zlib (required)
touch configure
%configure --with-dbus=yes \
           --with-pam \
           --with-openssl \
           --without-tcl \
           --with-qt=no \
           --disable-optimization # -O2 will be turned on because of RPM_OPT_FLAFS,
                                  # but it won't be appended at the end of CFLAGS

#upstream is working with .a lib, so hardcoding path to libdbus-1.so to prevent build failures
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
chmod 755 $RPM_BUILD_ROOT%{_libdir}/*.so.*
rm -fr $RPM_BUILD_ROOT/usr/bin

pushd $RPM_BUILD_ROOT
rm -f \
   ./etc/uniconf.conf \
   .%{_bindir}/uni \
   .%{_libdir}/pkgconfig/libwvqt.pc \
   .%{_sbindir}/uniconfd \
   .%{_mandir}/man8/uni.8* \
   .%{_mandir}/man8/uniconfd.8* \
   .%{_var}/lib/uniconf/uniconfd.ini
popd

%files
%doc LICENSE README
%{_libdir}/*.so.*

%files devel
%{_includedir}/wvstreams
%{_libdir}/*.so
%{_libdir}/valgrind/*.supp
%{_libdir}/pkgconfig/*.pc

%files static
%{_libdir}/*.a

%ldconfig_scriptlets

%changelog
* Tue Aug 10 2021 Olivia Crain <oliviacrain@microsoft.com> - 4.6.1-34
- Add patch to enable compatibility with recent versions of openssl

* Tue Jul 06 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.6.1-33
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Removing BR on 'compat-openssl10-devel' and leaving only 'openssl-devel'.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.1-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 25 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 4.6.1-31
- Fixed compilation with gcc-10

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.1-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.1-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 4.6.1-28
- Rebuilt for libcrypt.so.2 (#1666033)

* Fri Jul 20 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 4.6.1-27
- Fixed FTBFS by adding gcc-c++ requirement
  Resolves: rhbz#1604690
- De-fuzzified patches

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar  8 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 4.6.1-25
- Fixed stack size
  Resolves: rhbz#1551334

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.6.1-23
- Switch to %%ldconfig_scriptlets

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 4.6.1-22
- Rebuilt for switch to libxcrypt

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 28 2017 Michal Sekletar <msekleta@redhat.com> - 4.6.1-19
- Build against openssl-1.0.2 because package fails to build against openssl-1.1.0 (#1423893)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 4.6.1-17
- Rebuild for readline 7.x

* Tue Feb 09 2016 Michal Sekletar <msekleta@redhat.com> - 4.6.1-16
- Fix invalid cast and prevent compilation error

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 4.6.1-13
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 09 2013 Michal Sekletar <msekleta@redhat.com> - 4.6.1-9
- put static libraries into subpackage
- disable strict aliasing optimizations to prevent warnings and possible crashes
- fix changelog dates

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Michal Sekletar <msekleta@redhat.com> - 4.6.1-6
- Disabled optimizations which caused crash related to #812651

* Mon Jun 04 2012 Michal Sekletar <msekleta@redhat.com> - 4.6.1-5
- Fix crashes caused by compiler optimizations, #812651

* Thu Jan 05 2012 Jan Synáček <jsynacek@redhat.com> - 4.6.1-4
- Fix missing unistd.h header for gcc 4.7

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 12 2010 Ondrej Vasik <ovasik@redhat.com> - 4.6.1-2
- Merge review changes: added few comments, do not use "-fpermissive"
  for COPTS, use parallel build (#226061)

* Thu Nov 12 2009 Ondrej Vasik <ovasik@redhat.com> - 4.6.1-1
- new upstream release 4.6.1

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 4.6-5
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 27 2009 Ondrej Vasik <ovasik@redhat.com> - 4.6-3
- another fix for build with dbus(#479144)

* Sat Jun 27 2009 Ondrej Vasik <ovasik@redhat.com> - 4.6-2
- add build requires for dbus-devel, build with libdbus-1.so
  (#479144)
- fix multilib issue with wvautoconf.h(#508418)

* Thu Jun 11 2009 Ondrej Vasik <ovasik@redhat.com> - 4.6-1
- new upstream release with dynamically linked dbus(#479144)

* Fri Feb 27 2009 Ondrej Vasik <ovasik@redhat.com> - 4.5.1-5
- fix rebuild failure with gcc 4.4

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 4.5.1-3
- rebuild with new openssl

* Fri Jan 09 2009 Ondrej Vasik <ovasik@redhat.com> - 4.5.1-2
- do not remove libwvdbus.pc (#479144)

* Thu Jan 08 2009 Ondrej Vasik <ovasik@redhat.com> - 4.5.1-1
- new upstream release 4.5.1 , removed applied patches
- activate --with-dbus(#479144)

* Fri Nov 21 2008 Ondrej Vasik <ovasik@redhat.com> - 4.5-1
- new upstream release
- fixed issue with missing install-xplc target and std::sort
  missing gcc-4.3 error
- updated optional configure options list in spec file

* Fri Aug 29 2008 Ondrej Vasik <ovasik@redhat.com> - 4.4.1-5
- patch fuzz clean up

* Tue Feb 12 2008 Ondrej Vasik <ovasik@redhat.com> - 4.4.1-4
- gcc43 rebuild, climits instead limits.h usage

* Wed Dec 05 2007 Ondrej Vasik <ovasik@redhat.com> - 4.4.1-3
- rebuilt because of new OpenSSL

* Wed Nov 28 2007 Ondrej Vasik <ovasik@redhat.com> - 4.4.1-2
- no use of obsolete sa_restorer(#402531- by Oliver Falk)

* Mon Oct 22 2007 Ondrej Vasik <ovasik@redhat.com> - 4.4.1-1
- version 4.4.1

* Fri Aug 17 2007 Harald Hoyer <harald@rawhide.home> - 4.4-1
- version 4.4
- changed license tag to LGPLv2+

* Thu Jun 28 2007 Harald Hoyer <harald@redhat.com> - 4.3-2
- added static libs, esp. xplc-cxx

* Thu Jun 28 2007 Harald Hoyer <harald@redhat.com> - 4.3-1
- version 4.3

* Wed Apr 18 2007 Harald Hoyer <harald@redhat.com> - 4.2.2-4
- specfile review

* Wed Jan 24 2007 Harald Hoyer <harald@redhat.com> - 4.2.2-3
- fixed code for new g++ version

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 4.2.2-2.1
- rebuild

* Fri Jun 02 2006 Harald Hoyer <harald@redhat.com> 4.2.2-2
- more corrections to multilib patch (bug #192717)

* Wed May 24 2006 Harald Hoyer <harald@redhat.com> 4.2.2-1
- version 4.2.2
- fixed multilib issue (bug #192717)

* Fri Mar 10 2006 Bill Nottingham <notting@redhat.com> - 4.2.1-2
- rebuild for ppc TLS issue (#184446)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.2.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.2.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Dec 19 2005 Harald Hoyer <harald@redhat.com> 4.2.1-1
- version 4.2.1

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov  9 2005 Tomas Mraz <tmraz@redhat.com> 3.75.0-6
- rebuilt against new openssl
- the gcc4 patch shouldn't be used anymore

* Mon Mar 14 2005 Harald Hoyer <harald@redhat.com> 3.75.0-5
- gcc4 patch added

* Wed Mar  2 2005 Jindrich Novy <jnovy@redhat.com> 3.75.0-4
- rebuilt

* Wed Feb 09 2005 Harald Hoyer <harald@redhat.com>
- rebuilt

* Mon Jun 28 2004 Harald Hoyer <harald@redhat.com> 3.75.0-2
- added libwvstreams-3.75.0-stringbuf.patch (114996)

* Mon Jun 21 2004 Harald Hoyer <harald@redhat.com> 3.75.0-1
- version 3.75.0

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Oct 10 2003 Nalin Dahyabhai <nalin@redhat.com> 3.70-12
- link libwvstreams shared libs against libcrypt, upon which they depend

* Mon Sep  8 2003 Nalin Dahyabhai <nalin@redhat.com> 3.70-11
- rebuild

* Mon Sep  8 2003 Nalin Dahyabhai <nalin@redhat.com> 3.70-10
- rebuild

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 3.70-7
- rebuild

* Fri Jan  3 2003 Nalin Dahyabhai <nalin@redhat.com>
- correct an const/not-const type mismatch that breaks compilation with newer
  OpenSSL
- add flags from pkgconfig so that OpenSSL is always found

* Tue Sep 10 2002 Mike A. Harris <mharris@redhat.com> 3.70-6
- use FHS macros for multilib systems

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Mon Jul 22 2002 Tim Powers <timp@redhat.com>
- rebuild using gcc-3.2-0.1

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 20 2002 Nalin Dahyabhai <nalin@redhat.com> 3.70-1
- patch to build with gcc 3.x
- build with -fPIC

* Wed Apr 10 2002 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.70

* Wed Mar 27 2002 Nalin Dahyabhai <nalin@redhat.com> 3.69-1
- pull in from upstream tarball

* Wed Feb 27 2002 Nalin Dahyabhai <nalin@redhat.com>
- merge the main and -devel packages into one .spec file
- use globbing to shorten the file lists
- don't define name, version, and release as macros (RPM does this by default)
- use the License: tag instead of Copyright: (equivalent at the package level,
  but License: reflects the intent of the tag better)
- use a URL to point to the source of the source tarball
- add BuildRequires: openssl-devel (libwvcrypto uses libcrypto)
- move the buildroot to be under %%{_tmppath}, so that it can be moved by
  altering RPM's configuration

* Tue Jan 29 2002 Patrick Patterson <ppatters@nit.ca>
- Initial Release of WvStreams
