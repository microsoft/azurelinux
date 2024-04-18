%global         snapshot 0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary:        Off-The-Record Messaging library and toolkit
Name:           libotr
Version:        4.1.1
Release:        11%{?dist}
License:        GPLv2 and LGPLv2
Source0:        http://otr.cypherpunks.ca/%{name}-%{version}.tar.gz
Url:            http://otr.cypherpunks.ca/
Patch0:         libotr-4.1.1-socket-h.patch
Provides:       libotr-toolkit = %{version}
Obsoletes:      libotr-toolkit < %{version}
Requires:       libgcrypt >= 1.2.0
Requires:       pkgconfig
BuildRequires:  gcc
BuildRequires:  libgcrypt-devel >= 1.2.0
BuildRequires:  libgpg-error-devel
%if %{snapshot}
Buildrequires:  autoconf
Buildrequires:  automake
Buildrequires:  libtool
%endif

%description
Off-the-Record Messaging Library and Toolkit
This is a library and toolkit which implements Off-the-Record (OTR) Messaging.
OTR allows you to have private conversations over IM by providing Encryption,
Authentication, Deniability and Perfect forward secrecy.

%package devel
Summary: Development library and include files for libotr
Requires: %{name} = %{version}-%{release}, libgcrypt-devel >= 1.2.0
Conflicts: libotr3-devel

%description devel
The devel package contains the libotr library and include files.

%prep
%autosetup -p1

%if %{snapshot}
aclocal
intltoolize --force --copy
autoreconf -s -i
%endif

%build
%configure --with-pic --disable-rpath --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags} all

%install
rm -rf $RPM_BUILD_ROOT
make \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBINSTDIR=%{_libdir} \
	install
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la

%ldconfig_scriptlets

%files
%license COPYING COPYING.LIB
%doc AUTHORS README NEWS Protocol*
%{_libdir}/libotr.so.*
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%doc ChangeLog
%{_libdir}/libotr.so
%{_libdir}/pkgconfig/libotr.pc
%dir %{_includedir}/libotr
%{_includedir}/libotr/*
%{_datadir}/aclocal/*


%changelog
* Wed Apr 17 2024 Andrew Phelps <anphel@microsoft.com> - 4.1.1-11
- Add patch to fix build break
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.1.1-10
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Mar 09 2016 Paul Wouters <pwouters@redhat.com> - 4.1.1-1
- Updated to 4.1.1
- Resolves rhbz#CVE-2016-2851

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Oct 21 2014 Paul Wouters <pwouters@redhat.com> - 4.1.0-1
- Updated to 4.1.0 (minor security enhancements, fragmentation bugfixes)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 12 2014 Paul Wouters <pwouters@redhat.com> - 4.0.0-3
- Added four git fixes, of which two were crashers

* Wed Aug 21 2013 Paul Wouters <pwouters@redhat.com> - 4.0.0-2
- Conflict libotr-devel with libotr3-devel (rhbz#998382)

* Sat Jul 27 2013 Paul Wouters <pwouters@redhat.com> - 4.0.0-1
- Upgraded to libotr-4.0.0
- Since this is API incompatible, there is also a libotr3 package

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 15 2012 Paul Wouters <pwouters@redhat.com> - 3.2.1-1
- Updated to 3.2.1, updates patch for rhbz#846377, CVE-2012-3461

* Wed Aug 08 2012 Paul Wouters <pwouters@redhat.com> - 3.2.0-9
- Patch for Multiple heap-based buffer overflows in the Base64 decoder
  (rhbz#846377, upstream will not release 3.2.1 for this)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon May 24 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2.0-5
- disable static libs
- disable rpath

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2.0-2
- fix license tag

* Sun Jun 15 2008 Paul Wouters <paul@cypherpunks.ca> 3.2.0-1
- Upgraded to 3.2.0

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.1.0-2
- Autorebuild for GCC 4.3

* Wed Aug  1 2007 Paul Wouters <paul@cypherpunks.ca> 3.1.0-1
- Upgraded to current version
- Updated URLS and configure line

* Mon Sep 11 2006 Paul Wouters <paul@cypherpunks.ca> 3.0.0-2
- Rebuild requested for PT_GNU_HASH support from gcc

* Mon Oct 17 2005 Paul Wouters <paul@cypherpunks.ca> 3.0.0-1
- Minor change to allow for new documentation files. Fixed Requires:

* Sun Jun 19 2005 Paul Wouters <paul@cypherpunks.ca>
- Fixed defattr, groups, description and duplicate files in devel

* Fri Jun 17 2005 Tom "spot" Callaway <tcallawa@redhat.com>
- reworked for Fedora Extras

* Tue May  3 2005 Ian Goldberg <ian@cypherpunks.ca>
- Bumped version number to 2.0.2
* Wed Feb 16 2005 Ian Goldberg <ian@cypherpunks.ca>
- Bumped version number to 2.0.1
* Tue Feb  8 2005 Ian Goldberg <ian@cypherpunks.ca>
- Bumped version number to 2.0.0
* Wed Feb  2 2005 Ian Goldberg <ian@cypherpunks.ca>
- Added libotr.m4 to the devel package
- Bumped version number to 1.99.0
* Wed Jan 19 2005 Paul Wouters <paul@cypherpunks.ca>
- Updated spec file for the gaim-otr libotr split
* Tue Dec 21 2004 Ian Goldberg <otr@cypherpunks.ca>
- Bumped to version 1.0.2.
* Fri Dec 17 2004 Paul Wouters <paul@cypherpunks.ca>
- instll fix for x86_64
* Sun Dec 12 2004 Ian Goldberg <otr@cypherpunks.ca>
- Bumped to version 1.0.0.
* Fri Dec 10 2004 Ian Goldberg <otr@cypherpunks.ca>
- Bumped to version 0.9.9rc2. 
* Thu Dec  9 2004 Ian Goldberg <otr@cypherpunks.ca>
- Added CFLAGS to "make all", removed DESTDIR
* Wed Dec  8 2004 Ian Goldberg <otr@cypherpunks.ca>
- Bumped to version 0.9.9rc1. 
* Fri Dec  3 2004 Ian Goldberg <otr@cypherpunks.ca>
- Bumped to version 0.9.1. 
* Wed Dec  1 2004 Paul Wouters <paul@cypherpunks.ca>
- Bumped to version 0.9.0. 
- Fixed install for tools and cos
- Added Obsoletes: target for otr-plugin so rpm-Uhv gaim-otr removes it.
* Mon Nov 22 2004 Ian Goldberg <otr@cypherpunks.ca>
- Bumped version to 0.8.1
* Sun Nov 21 2004 Paul Wouters <paul@cypherpunks.ca>
- Initial version
