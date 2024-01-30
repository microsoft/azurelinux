Summary:        Universally Unique Identifier library
Name:           uuid
Version:        1.6.2
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://www.ossp.org/pkg/lib/uuid/
Source0:        ftp://ftp.ossp.org/pkg/lib/uuid/uuid-%{version}.tar.gz
Patch0:         uuid-1.6.1-ossp.patch
Patch1:         uuid-1.6.1-mkdir.patch
Patch2:         uuid-1.6.2-php54.patch
# rhbz#829532
Patch3:         uuid-1.6.2-hwaddr.patch
# do not strip binaries
Patch4:         uuid-1.6.2-nostrip.patch
Patch5:         uuid-1.6.2-manfix.patch
Patch6:         uuid-aarch64.patch
BuildRequires:  gcc
BuildRequires:  libtool
Obsoletes:      %{name}-pgsql < 1.6.2-24

%description
OSSP uuid is a ISO-C:1999 application programming interface (API)
and corresponding command line interface (CLI) for the generation
of DCE 1.1, ISO/IEC 11578:1996 and RFC 4122 compliant Universally
Unique Identifier (UUID). It supports DCE 1.1 variant UUIDs of version
1 (time and node based), version 3 (name based, MD5), version 4
(random number based) and version 5 (name based, SHA-1). Additional
API bindings are provided for the languages ISO-C++:1998 and Perl:5
Optional backward compatibility exists for the ISO-C DCE-1.1 and Perl
Data::UUID APIs.

%package devel
Summary:        Development support for Universally Unique Identifier library
Requires:       %{name} = %{version}-%{release}
Requires:       pkg-config

%description devel
Development headers and libraries for OSSP uuid.

%package c++
Summary:        C++ support for Universally Unique Identifier library
Requires:       %{name} = %{version}-%{release}

%description c++
C++ libraries for OSSP uuid.

%package c++-devel
Summary:        C++ development support for Universally Unique Identifier library
Requires:       %{name}-c++ = %{version}-%{release}
Requires:       %{name}-devel = %{version}-%{release}

%description c++-devel
C++ development headers and libraries for OSSP uuid.

%package dce
Summary:        DCE support for Universally Unique Identifier library
Requires:       %{name} = %{version}-%{release}

%description dce
DCE OSSP uuid library.

%package dce-devel
Summary:        DCE development support for Universally Unique Identifier library
Requires:       %{name}-dce = %{version}-%{release}
Requires:       %{name}-devel = %{version}-%{release}

%description dce-devel
DCE development headers and libraries for OSSP uuid.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1 -b .php54
%patch3 -p1 -b .hwaddr
%patch4 -p1 -b .nostrip
%patch5 -p1 -b .manfix
%patch6 -p1 -b .aarch64

%build
# Build the library.
export LIB_NAME=libossp-uuid.la
export DCE_NAME=libossp-uuid_dce.la
export CXX_NAME=libossp-uuid++.la
export PHP_NAME=$(pwd)/php/modules/ossp-uuid.so
export PGSQL_NAME=$(pwd)/pgsql/libossp-uuid.so
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
%configure \
    --disable-static \
    --without-perl \
    --without-php \
    --with-dce \
    --with-cxx \
    --without-pgsql

make LIBTOOL="%{_bindir}/libtool --tag=CC" CFLAGS="$CFLAGS" CXXFLAGS="$CXXFLAGS" %{?_smp_mflags}

%install

make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la %{buildroot}%{_libdir}/*.a
chmod 755 %{buildroot}%{_libdir}/*.so.*.*.*

find %{buildroot} -type f -name '*.bs' -size 0 -exec rm -f {} \;
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check
make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog HISTORY NEWS PORTING README SEEALSO THANKS TODO USERS
%{_bindir}/uuid
%{_libdir}/libossp-uuid.so.*
%{_mandir}/man1/*
%exclude %{_mandir}/man1/uuid-config.*

%files devel
%{_bindir}/uuid-config
%{_includedir}/uuid.h
%{_libdir}/libossp-uuid.so
%{_libdir}/pkgconfig/ossp-uuid.pc
%{_mandir}/man3/ossp-uuid.3*
%{_mandir}/man1/uuid-config.*

%files c++
%{_libdir}/libossp-uuid++.so.*

%files c++-devel
%{_includedir}/uuid++.hh
%{_libdir}/libossp-uuid++.so
%{_mandir}/man3/uuid++.3*

%files dce
%{_libdir}/libossp-uuid_dce.so.*

%files dce-devel
%{_includedir}/uuid_dce.h
%{_libdir}/libossp-uuid_dce.so

%changelog
* Mon Jan 29 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.6.2-1
- Auto-upgrade to 1.6.2 - none

* Mon Nov 30 2020 Nicolas Ontiveros <niontive@microsoft.com> - 1.6.2-50
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- Replace ldconfig_scriptlets with post/postun ldconfig calls
- Use gcc for BR
- Use pkg-config for devel package BR
- Remove perl package
- Remove Fedora/RHEL check for filter_setup
- Add CC tag to libtool for make

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.6.2-48
- Perl 5.32 rebuild

* Mon Mar 16 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.6.2-47
- Specify all perl dependencies

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.6.2-44
- Perl 5.30 rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.6.2-41
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.6.2-37
- Rebuild due to bug in RPM (RHBZ #1468476)

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.6.2-36
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Sep 1 2016 Matias Kreder <mkreder@gmail.com> - 1.6.2-34
- Removed uuid-php subpackage since php(api) is no longer provided on
- PHP 7 and there is a replacement (pecl/uuid extension)

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.6.2-33
- Perl 5.24 rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.6.2-30
- Perl 5.22 rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.6.2-29
- Rebuilt for GCC 5 C++11 ABI change

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.6.2-28
- Perl 5.20 rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 19 2014 Remi Collet <rcollet@redhat.com> - 1.6.2-26
- rebuild for https://fedoraproject.org/wiki/Changes/Php56
- add numerical prefix to PHP extension configuration file

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Oct 30 2013 Michal Hlavinka <mhlavink@redhat.com> - 1.6.2-24
- drop uuid-pgsql subpackage, it is outdated and does not work, use 
  uuid-ossp module from postgresql-contrib instead

* Mon Sep 16 2013 Paul Howarth <paul@city-fan.org> - 1.6.2-23
- drop the perl(Data::UUID) compatibility shim and require the real thing
  instead (#998591)

* Thu Sep 12 2013 Michal Hlavinka <mhlavink@redhat.com> - 1.6.2-22
- rebuild for postgresql api change

* Wed Aug 14 2013 Michal Hlavinka <mhlavink@redhat.com> - 1.6.2-21
- fix aarch64 support (#926687)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.6.2-19
- Perl 5.18 rebuild

* Thu May 30 2013 Michal Hlavinka <mhlavink@redhat.com> - 1.6.2-18
- describe -r in man page

* Fri Mar 22 2013 Remi Collet <rcollet@redhat.com> - 1.6.2-17
- rebuild for http://fedoraproject.org/wiki/Features/Php55

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 06 2012 Michal Hlavinka <mhlavink@redhat.com> - 1.6.2-15
- make uuid-php compatible with php 5.4 (#873594)

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 1.6.2-13
- Perl 5.16 rebuild

* Tue Jun 19 2012 Michal Hlavinka <mhlavink@redhat.com> - 1.6.2-12
- enforce usage of our c(xx)flags

* Tue Jun 19 2012 Michal Hlavinka <mhlavink@redhat.com> - 1.6.2-11
- fix debuginfo

* Tue Jun 19 2012 Michal Hlavinka <mhlavink@redhat.com> - 1.6.2-10
- fix generation of MAC address based uuids (#829532), 
  patch by Philip Prindeville

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 1.6.2-9
- Perl 5.16 rebuild

* Thu Jan 19 2012 Remi Collet <remi@fedoraproject.org> - 1.6.2-8
- build against php 5.4, with patch
- add filter_provides to avoid private-shared-object-provides shout.so
- add minimal %%check for php extension

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.6.2-6
- Perl mass rebuild

* Sat May 14 2011 Iain Arnell <iarnell@gmail.com> 1.6.2-5
- fix php_zend_api check

* Thu Mar 03 2011 Karsten Hopp <karsten@redhat.com> 1.6.2-4
- fix build

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jun 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.6.2-2
- Mass rebuild with perl-5.12.0

* Wed Apr 21 2010 Michal Hlavinka <mhlavink@redhat.com> - 1.6.2-1
- updated to 1.6.2
- uuid-config man page moved to sub-package containing uuid-config (#562838)

* Mon Feb  1 2010 Stepan Kasal <skasal@redhat.com> - 1.6.1-10
- silence rpmlint by using $(pwd) instead of shell variable RPM_SOURCE_DIR

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.6.1-9
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.6.1-7
- rebuild for new PHP 5.3.0 ABI (20090626)
- add PHP ABI check
- use php_extdir
- add php configuration file (/etc/php.d/uuid.ini)

* Thu May  7 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.6.1-6
- Using plain old "Requires: pkgconfig" instead -- see my post to
  fedora-devel-list made today.

* Mon May  4 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.6.1-5
- Replace expensive %%{_libdir}/pkgconfig dependency in uuid-devel
  with pkgconfig%%{_isa} for Fedora >= 11 (#484849).

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.6.1-3
- Rebuild for new perl

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.6.1-2
- forgot to cvs add patch

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.6.1-1
- 1.6.1

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.6.0-4
- rebuild for new perl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.6.0-3
- Autorebuild for GCC 4.3

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.6.0-2
- Rebuild for selinux ppc32 issue.

* Tue Jul 24 2007 Steven Pritchard <steve@kspei.com> 1.6.0-1
- Update to 1.6.0.
- BR Test::More.

* Tue Apr 17 2007 Steven Pritchard <steve@kspei.com> 1.5.1-3
- Fix find option order.
- Use fixperms macro instead of our own chmod incantation.
- BR ExtUtils::MakeMaker.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 1.5.1-2
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Aug 28 2006 Steven Pritchard <steve@kspei.com> 1.5.1-1
- Update to 1.5.1.

* Sat Jul 29 2006 Steven Pritchard <steve@kspei.com> 1.5.0-1
- Update to 1.5.0.
- Rename libuuid* to libossp-uuid*, uuid.3 to ossp-uuid.3, and uuid.pc
  to ossp-uuid.pc to avoid conflicts with e2fsprogs-devel (#198520).
- Clean out the pgsql directory.  (Some cruft shipped with this release.)

* Wed May 24 2006 Steven Pritchard <steve@kspei.com> 1.4.2-4
- Remove static php module.

* Tue May 23 2006 Steven Pritchard <steve@kspei.com> 1.4.2-3
- Force use of system libtool.
- Make libs executable.

* Tue May 23 2006 Steven Pritchard <steve@kspei.com> 1.4.2-2
- License is MIT(-ish).

* Fri May 19 2006 Steven Pritchard <steve@kspei.com> 1.4.2-1
- Initial packaging attempt.
