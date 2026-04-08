# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global so_major_version 2
%global so_minor_version 0
%global so_patch_version 1

Name:           sysfsutils
Version:        2.1.1
Release:        11%{?dist}
Summary:        Utilities for interfacing with sysfs
URL:            https://github.com/linux-ras/sysfsutils
License:        GPL-2.0-only

Source0:        https://github.com/linux-ras/sysfsutils/archive/v%{version}.tar.gz

Patch0:         sysfsutils-2.1.1-fix-my-strncat.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  gcc
Requires:       libsysfs = %{version}-%{release}

%description
This package's purpose is to provide a set of utilities for interfacing
with sysfs.

%package -n libsysfs
Summary: Shared library for interfacing with sysfs
License: LGPL-2.1-or-later

%description -n libsysfs
Library used in handling linux kernel sysfs mounts and their various files.

%package -n libsysfs-devel
Summary: Static library and headers for libsysfs
License: LGPL-2.1-or-later
Requires: libsysfs = %{version}-%{release}

%description -n libsysfs-devel
libsysfs-devel provides the header files and static libraries required
to build programs using the libsysfs API.

%prep
%autosetup -p1

%build
./autogen
%configure --disable-static
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name "*.la" -delete

%ldconfig_scriptlets -n libsysfs

%files
%license COPYING cmd/GPL
%doc AUTHORS README CREDITS docs/libsysfs.txt
%{_bindir}/systool
%{_mandir}/man1/systool.1.gz

%files -n libsysfs
%license COPYING lib/LGPL
/%{_libdir}/libsysfs.so.%{so_major_version}
/%{_libdir}/libsysfs.so.%{so_major_version}.%{so_minor_version}.%{so_patch_version}

%files -n libsysfs-devel
%dir %{_includedir}/sysfs
%{_includedir}/sysfs/libsysfs.h
%{_includedir}/sysfs/dlist.h
/%{_libdir}/libsysfs.so
/%{_libdir}/pkgconfig/libsysfs.pc


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Apr 25 2025 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.1.1-10
- Fix erroneous my_strncat implementation

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Feb 20 2021 Christopher Engelhard <ce@lcts.de> - 2.1.1-1
- Update to 2.1.1
- Remove all patches merged upstream
- Switched build to autotools
- Include upstream pkgconfig module
- Sysfsutils no longer includes /usr/bin/get_module

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Sep 21 2020 Christopher Engelhard <ce@lcts.de> - 2.1.0-32
- fix GCC-11 build failure due to buffer overread, h/t Jeff Law

* Mon Aug 17 2020 Christopher Engelhard <ce@lcts.de> - 2.1.0-31
- use tarball hosted at new upstream site
- Fedora's patches have been merged upstream, so use those instead
- apply various unreleased upstream fixes that deal with compiler warnings

* Wed Jul 29 2020 Christopher Engelhard <ce@lcts.de> - 2.1.0-30
- specify .so and release versions via global vars
- update URL to reflect new upstream

* Tue Jun 23 2020 Christopher Engelhard <ce@lcts.de> - 2.1.0-29
- list .so files explicitly in %%files instead of via glob, cleanup spec

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jul 22 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2.1.0-25
- Fix build deps, use %%License, cleanup spec

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat May 11 2013 Anton Arapov <anton@redhat.com> - 2.1.0-14
- We don't support aarch64, do the appropriate changes (#926600)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Mar 22 2011 Anton Arapov <anton@redhat.com> - 2.1.0-10
- Better manpages. (#673849)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jun 17 2010 Anton Arapov <anton@redhat.com> - 2.1.0-8
- Move libraries from /usr/lib to /lib since we need them
  during the system boot. (#605546)

* Mon Jan 18 2010 Anton Arapov <anton@redhat.com> - 2.1.0-7
- Don't build and ship statically linked library (#556096)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue May 20 2008 Jarod Wilson <jwilson@redhat.com> - 2.1.0-4
- Fix up get_link on kernel 2.6.25+ (#447220)

* Mon Feb 25 2008 Jarod Wilson <jwilson@redhat.com> - 2.1.0-3
- Review cleanups from Todd Zullinger (#226447)

* Thu Feb 14 2008 Jarod Wilson <jwilson@redhat.com> - 2.1.0-2
- Bump and rebuild with gcc 4.3

* Mon Sep 29 2007 Jarod Wilson <jwilson@redhat.com> - 2.1.0-1
- Update to upstream release 2.1.0

* Mon Sep 11 2006 Neil Horman <nhorman@redhat.com> - 2.0.0-6
- Integrate patch for bz 205808

* Mon Jul 17 2006 Jesse Keating <jkeating@redhat.com> - 2.0.0-5
- rebuild

* Mon Jul 10 2006 Neil Horman  <nhorman@redhat.com> - 2.0.0-4
- Obsoleting old sysfsutil-devel package for upgrade path (bz 198054)

* Fri Jul  7 2006 Doug Ledford <dledford@redhat.com> - 2.0.0-3
- Split the library and devel files out to libsysfs and leave the utils
  in sysfsutils.  This is for multilib arch requirements.

* Thu May 25 2006 Neil Horman <nhorman@redhat.com> - 2.0.0-2
- Fixed devel rpm to own sysfs include dir
- Fixed a typo in changelog

* Wed May 24 2006 Neil Horman <nhorman@redhat.com> - 2.0.0-1
- Rebase to sysfsutils-2.0.0 for RHEL5

* Thu Apr 27 2006 Jeremy Katz <katzj@redhat.com> - 1.3.0-2
- move .so to devel subpackage

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.3.0-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.3.0-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Jul 08 2005 Bill Nottingham  <notting@redhat.com> 1.3.0-1
- update to 1.3.0

* Wed Mar 02 2005 AJ Lewis <alewis@redhat.com> 1.2.0-4
- Rebuild

* Wed Feb 09 2005 AJ Lewis <alewis@redhat.com> 1.2.0-3
- start using %%configure instead of calling configure directly

* Wed Feb 09 2005 AJ Lewis <alewis@redhat.com> 1.2.0-2
- rebuild

* Mon Oct 11 2004 AJ Lewis <alewis@redhat.com> 1.2.0-1
- Update to upstream version 1.2.0

* Wed Sep 22 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- added /sbin/ldconfig calls to post/postun

* Thu Sep 01 2004 AJ Lewis <alewis@redhat.com> 1.1.0-2
- Fix permissions on -devel files

* Fri Aug 13 2004 AJ Lewis <alewis@redhat.com> 1.1.0-1.1
- Rebuild

* Fri Aug 13 2004 AJ Lewis <alewis@redhat.com> 1.1.0-1
- Initial package for FC3
