Name:           sysfsutils
Version:        2.1.1
Release:        1%{?dist}
Summary:        Utilities for interfacing with sysfs
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            http://sourceforge.net/projects/linux-diag/
License:        GPLv2

Source0:        https://github.com/linux-ras/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         sysfsutils-2.0.0-redhatify.patch
Patch1:         sysfsutils-2.0.0-class-dup.patch
Patch2:         sysfsutils-2.1.0-get_link.patch
Patch3:         sysfsutils-2.1.0-manpages.patch
Patch4:         sysfsutils-aarch64.patch

BuildRequires:  gcc

%description
This package's purpose is to provide a set of utilities for interfacing
with sysfs.

%package -n libsysfs
Summary: Shared library for interfacing with sysfs
License: LGPLv2+

%description -n libsysfs
Library used in handling linux kernel sysfs mounts and their various files.

%package -n libsysfs-devel
Summary: Static library and headers for libsysfs
License: LGPLv2+
Requires: libsysfs = %{version}-%{release}

%description -n libsysfs-devel
libsysfs-devel provides the header files and static libraries required
to build programs using the libsysfs API.

%prep
%setup -q
%patch 0 -p1 -b .redhatify
%patch 1 -p1
%patch 2 -p1
%patch 3 -p1
%patch 4 -p1

%build
%configure --disable-static --libdir=/%{_lib}
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT%{_bindir}/dlist_test $RPM_BUILD_ROOT%{_bindir}/get_bus_devices_list $RPM_BUILD_ROOT%{_bindir}/get_class_dev $RPM_BUILD_ROOT%{_bindir}/get_classdev_parent $RPM_BUILD_ROOT%{_bindir}/get_device $RPM_BUILD_ROOT%{_bindir}/get_driver $RPM_BUILD_ROOT%{_bindir}/testlibsysfs $RPM_BUILD_ROOT%{_bindir}/write_attr
find %{buildroot} -type f -name "*.la" -delete

%ldconfig_scriptlets -n libsysfs

%files
%license COPYING cmd/GPL
%doc AUTHORS README NEWS CREDITS ChangeLog docs/libsysfs.txt
%{_bindir}/systool
%{_bindir}/get_module
%{_mandir}/man1/systool.1.gz

%files -n libsysfs
%license COPYING lib/LGPL
/%{_lib}/libsysfs.so.*

%files -n libsysfs-devel
%dir %{_includedir}/sysfs
%{_includedir}/sysfs/libsysfs.h
%{_includedir}/sysfs/dlist.h
/%{_lib}/libsysfs.so


%changelog
* Tue Jul 30 2024 Aditya Dubey <adityadubey@microsoft.com> - 2.1.1-1
- Upgrading to 2.1.1 with new source

* Mon Jul 22 2024 Aditya Dubey <adityadubey@microsoft.com> - 2.1.0-30
- Promoting package from SPECS-EXTENDED to SPECS

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.1.0-29
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- License verified

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
