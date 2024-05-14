Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global udevdir %{_prefix}/lib/udev

Summary: Library for using OBEX
Name: openobex
Version: 1.7.2
Release: 12%{?dist}
License: GPLv2+ and LGPLv2+
URL: https://openobex.sourceforge.net
# git clone https://git.gitorious.org/openobex/mainline.git
Source: https://downloads.sourceforge.net/%{name}/%{name}-%{version}-Source.tar.gz
Patch0:  openobex-apps-flush.patch
Patch1:  openobex-1.7-obex_push.patch
Patch2:  openobex-1.7-udev_rule.patch
Patch3:  openobex-1.7-strtoul.patch

# gcc is no longer in buildroot by default
BuildRequires: gcc

BuildRequires: bluez-libs-devel, libusb-devel
BuildRequires: cmake, doxygen, libxslt, docbook-style-xsl
ExcludeArch: s390 s390x

%description
OBEX (OBject EXchange) is a protocol usually used by various mobile
devices to exchange all kind of objects like files, pictures, calendar
entries (vCal) and business cards (vCard).  This package contains the
Open OBEX shared C library.

%package devel
Summary: Files for development of applications which will use OBEX
Requires: %{name} = %{version}-%{release}
Requires: bluez-libs-devel libusb-devel

%description devel
Header files for development of applications which use OpenOBEX.

%package apps
Summary: Applications for using OBEX

%description apps
Open OBEX Applications to exchange all kind of objects like files, pictures,
calendar entries (vCal) and business cards (vCard) using the OBEX protocol.

%prep
%setup -q -n %{name}-%{version}-Source
%patch 0 -p1 -b .flush
%patch 1 -p1 -b .push
%patch 2 -p1 -b .udev
%patch 3 -p1 -b .strtoul

%build
export CFLAGS="%{optflags} -std=gnu99 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE"

%cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} \
       -DCMAKE_SKIP_RPATH=YES \
       -DCMAKE_VERBOSE_MAKEFILE=YES \
       -DCMAKE_INSTALL_DOCDIR=%{_pkgdocdir} \
       -DCMAKE_INSTALL_UDEVRULESDIR=%{udevdir}/rules.d

make %{?_smp_mflags}
make openobex-apps %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
# we do not want .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# don't ship obex_test program, that is for testing purposes only
# and has some problems (multiple buffer overflows etc.)
rm -f $RPM_BUILD_ROOT%{_bindir}/obex_test
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/obex_test.1*

%ldconfig_scriptlets

%files
%doc AUTHORS COPYING COPYING.LIB ChangeLog README
# the HTML doc is distributed in the %%{name}-devel subpackage
%exclude %{_pkgdocdir}/html
%{_libdir}/libopenobex*.so.*
%{_sbindir}/obex-check-device
%{udevdir}/rules.d/60-openobex.rules

%files devel
%doc %{_pkgdocdir}/html
%{_libdir}/libopenobex*.so
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/pkgconfig/openobex.pc
%dir %{_libdir}/cmake
%{_libdir}/cmake/OpenObex-%{version}

%files apps
%{_bindir}/irobex_palm3
%{_mandir}/man1/irobex_palm3.1*
%{_bindir}/irxfer
%{_mandir}/man1/irxfer.1*
%{_bindir}/ircp
%{_mandir}/man1/ircp.1*
%{_bindir}/obex_tcp
%{_mandir}/man1/obex_tcp.1*
%{_bindir}/obex_find
%{_mandir}/man1/obex_find.1*
%{_bindir}/obex_push
%{_mandir}/man1/obex_push.1*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.7.2-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 19 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.7.2-7
- gcc is no longer in buildroot by default

* Thu Feb 08 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.7.2-6
- remove old stuff https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/MRWOMRZ6KPCV25EFHJ2O67BCCP3L4Y6N/

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 18 2016 Filip Čáp cap.filip.dev@gmail.com - 1.7.2-1
- Update to 1.7.2

* Fri Mar 18 2016 Zdenek Dohnal zdohnal@redhat.com - 1.7.1-9
- Fixing strtoul bug

* Thu Mar 17 2016 Zdenek Dohnal zdohnal@redhat.com - 1.7.1-8
- Fixing FTBFS bug by adding special build flags

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Oct 01 2014 Tomas Hozza <thozza@redhat.com> - 1.7.1-5
- Fix udev rule to not use plugdev group (#1136580)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 09 2014 Tomas Hozza <thozza@redhat.com> - 1.7.1-2
- Distribute Cmake config files
- Minor packaging / spec file changes

* Thu Sep 26 2013 Tomas Hozza <thozza@redhat.com> - 1.7.1-1
- New version 1.7.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 07 2012 Tomas Hozza <thozza@redhat.com> - 1.5-7
- Fixed errors found by Coverity scan.

* Thu Nov 15 2012 Tomas Hozza <thozza@redhat.com> - 1.5-6
- changing not working Source0 URL and some minor changes in %%prep
- new source archive openobex-1.5.0-Source.zip

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Apr 28 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 1.5-3
- Drop obex_test program, as it is just for testing purposes
  and has some problems with multiple stack overflows etc.
  Resolves: #521663

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Mar 14 2010 Jiri Moskovcak <jmoskovc@redhat.com> - 1.5-1
- updated to a new version
- removed unused patches

* Fri Feb 26 2010 Jiri Moskovcak <jmoskovc@redhat.com> - 1.4-5
- properly fixed license

* Fri Feb 26 2010 Jiri Moskovcak <jmoskovc@redhat.com> - 1.4-4
- fixed license

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Nov 18 2008 Jiri Moskovcak <jmoskovc@redhat.com> 1.4.1
- New upstream version
- Spec file cleanup
- Removed unneeded patches

* Thu Oct  2 2008 Jiri Moskovcak <jmoskovc>@redhat.com> 1.3.15
- rebuilt against new bluez-libs

* Thu Oct  2 2008 Jiri Moskovcak <jmoskovc@redhat.com> 1.3.14
- bump release

* Wed Jun 18 2008 Jiri Moskovcak <jmoskovc@redhat.com> 1.3-13
- fixed problem when ircp tries to write files to /
- Resolves: #451493

* Mon Jun  2 2008 Jiri Moskovcak <jmoskovc@redhat.com> - 1.3-12
- improved utf(non ascii) support
- Resolves: #430128

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3-11
- Autorebuild for GCC 4.3

* Mon Oct 29 2007 Jiri Moskovcak <jmoskovc@redhat.com> - 1.3-10
- Spec file cleanup

* Fri Oct 26 2007 Jiri Moskovcak <jmoskovc@redhat.com> - 1.3-9
- Spec file cleanup
- Fixed wrong lib path in autoconf

* Tue Sep 18 2007 Jiri Moskovcak <jmoskovc@redhat.com> - 1.3-8
- Changed sources in specfile URL to point to the right location

* Fri Aug 24 2007 Jiri Moskovcak <jmoskovc@redhat.com> - 1.3-7
- Added ipv6 support
- Resolves: #198396

* Wed Aug 22 2007 Harald Hoyer <harald@redhat.com> - 1.3-6
- changed license tag

* Fri Mar 23 2007 Harald Hoyer <harald@redhat.com> - 1.3-5
- specfile cleanup

* Wed Feb  7 2007 Harald Hoyer <harald@redhat.com> - 1.3-4
- readded obex_push

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.3-3.1
- rebuild

* Tue Jun 27 2006 Harald Hoyer <harald@redhat.com> - 1.3-3
- removed more patches

* Tue Jun 27 2006 Harald Hoyer <harald@redhat.com> - 1.3-2
- added more build requirements
- built now with enable-usb

* Fri Jun 16 2006 Harald Hoyer <harald@redhat.com> - 1.3-1
- version 1.3

* Tue Jun 13 2006 Harald Hoyer <harald@redhat.com> - 1.2-2
- more build requirements

* Tue Jun 13 2006 Harald Hoyer <harald@redhat.com> - 1.2-1
- version 1.2

* Thu Feb 16 2006 Harald Hoyer <harald@redhat.com> 1.1-1
- version 1.1

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.1-4.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.1-4.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon May 02 2005 Harald Hoyer <harald@redhat.com> 1.0.1-4
- added `OBEX_ServerAccept' to the exported symbols (bug rh#146353)

* Wed Mar 02 2005 Harald Hoyer <harald@redhat.com>
- rebuilt

* Wed Feb 09 2005 Harald Hoyer <harald@redhat.com>
- rebuilt

* Mon Sep 13 2004 Harald Hoyer <harald@redhat.de> 1.0.1-1
- version 1.0.1

* Tue Jun 22 2004 Alan Cox <alan@redhat.com>
- removed now unneeded glib requirement

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Apr 19 2004 David Woodhouse <dwmw2@redhat.com> 1.0.0-5
- import for for #121271 from openobex CVS tree

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun  4 2003 Harald Hoyer <harald@redhat.de> 1.0.0-2
- excludeArch s390 s390x

* Wed Jun  4 2003 Harald Hoyer <harald@redhat.de> 1.0.0-1
- redhatified specfile
- bump to version 1.0.0

* Thu May 18 2000 Pontus Fuchs <pontus.fuchs@tactel.se>
- Initial RPM


