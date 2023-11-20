%global dropdir %(pkg-config libpcsclite --variable usbdropdir 2>/dev/null)
%global pcsc_lite_ver 1.8.9
Summary:        Generic USB CCID smart card reader driver
Name:           pcsc-lite-ccid
Version:        1.4.33
Release:        4%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://ccid.apdu.fr/files
Source0:        https://ccid.apdu.fr/files/ccid-%{version}.tar.bz2
Patch0:         ccid-1.4.26-omnikey-3121.patch

BuildRequires:  perl-interpreter
BuildRequires:  perl-Getopt-Long
BuildRequires:  libusb1-devel
BuildRequires:  pcsc-lite-devel >= %{pcsc_lite_ver}
BuildRequires:  gnupg2 gcc
Requires(post): systemd
Requires(postun): systemd
Requires:       pcsc-lite%{?_isa} >= %{pcsc_lite_ver}
Provides:       pcsc-ifd-handler
# Provide upgrade path from 'ccid' package
Obsoletes:      ccid < 1.4.0-3
Provides:       ccid = %{version}-%{release}
# This is bundled from pcsc-lite upstream
Provides:       bundled(simclist) = 1.6

%description
Generic USB CCID (Chip/Smart Card Interface Devices) driver for use with the
PC/SC Lite daemon.

%prep
%setup -q -n ccid-%{version}
%patch0 -p1 -b .omnikey

%build
%configure --enable-twinserial
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
cp -p src/openct/LICENSE LICENSE.openct

%post
/bin/systemctl try-restart pcscd.service >/dev/null 2>&1 || :

%postun
/bin/systemctl try-restart pcscd.service >/dev/null 2>&1 || :

%files
%doc AUTHORS ChangeLog README.md
%license COPYING LICENSE.openct
%{dropdir}/ifd-ccid.bundle/
%{dropdir}/serial/
%config(noreplace) %{_sysconfdir}/reader.conf.d/libccidtwin

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.4.33-4
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Feb 10 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.4.33-3
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.33-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jun 25 2020 Jakub Jelen <jjelen@redhat.com> - 1.4.33-1
- New upstream release (#1851217)

* Wed Apr 22 2020 Jakub Jelen <jjelen@redhat.com> - 1.4.32-1
- New upstream release (#1826675)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 19 2019 Jakub Jelen <jjelen@redhat.com> - 1.4.31-1
- New upstream release (#1742657)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 20 2018 Jakub Jelen <jjelen@redhat.com> - 1.4.30-1
- New upstream release (#1651350)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 21 2018 Jakub Jelen <jjelen@redhat.com> - 1.4.29-1
- New upstream release (#1547482)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Oct 20 2017 Jakub Jelen <jjelen@redhat.com> - 1.4.28-1
- New upstream release (#1504404)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 22 2017 Jakub Jelen <jjelen@redhat.com> - 1.4.27-1
- New upstream release (#1453026)

* Thu Mar 02 2017 Jakub Jelen <jjelen@redhat.com> - 1.4.26-3
- Return support for OMNIKEY CardMan 3121 long writes (#1420024)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan  9 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.4.26-1
- Updated to 1.4.26

* Mon Nov 21 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.4.25-1
- Updated to 1.4.25

* Tue Jun 21 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.4.24-1
- Updated to 1.4.24

* Mon Apr 25 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.4.23-1
- Updated to 1.4.23 (#1328849, #1330087)
- Added gpg verification of package as part of build process

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.4.22-1
- Updated to 1.4.22

* Thu Nov 12 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.4.21-1
- Updated to 1.4.21

* Wed Aug  5 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.4.20-1
- Updated to 1.4.20

* Fri Jul 10 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.4.19-1
- Updated to 1.4.19 (#1241842)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Sep 18 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.4.18-1
- Update to 1.4.18

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 12 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.4.17-1
- Update to 1.4.17

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Oct 20 2013 Kalev Lember <kalevlember@gmail.com> - 1.4.13-1
- Update to 1.4.13
- Tighten pcsc-lite deps with %%{?_isa}

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 12 2013 Kalev Lember <kalevlember@gmail.com> - 1.4.11-1
- Update to 1.4.11

* Wed Apr 17 2013 Kalev Lember <kalevlember@gmail.com> - 1.4.10-1
- Update to 1.4.10

* Thu Feb 28 2013 Kalev Lember <kalevlember@gmail.com> - 1.4.9-1
- Update to 1.4.9

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Oct 07 2012 Kalev Lember <kalevlember@gmail.com> - 1.4.8-1
- Update to 1.4.8

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Kalev Lember <kalevlember@gmail.com> - 1.4.7-1
- Update to 1.4.7

* Sat Apr 07 2012 Kalev Lember <kalevlember@gmail.com> - 1.4.6-1
- Update to 1.4.6

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 14 2011 Kalev Lember <kalevlember@gmail.com> - 1.4.5-1
- Update to 1.4.5
- Switch to systemctl for restarting pcscd after upgrade now that it is using
  native systemd unit files.

* Fri May 27 2011 Kalev Lember <kalev@smartlink.ee> - 1.4.4-1
- Update to 1.4.4
- Clean up the spec file for modern rpmbuild

* Sat Apr 02 2011 Kalev Lember <kalev@smartlink.ee> - 1.4.3-1
- Update to 1.4.3
- GPLv2+ licensed RSA_SecurID no longer gets installed, which changes
  the license of the binary RPM from 'LGPLv2+ and GPLv2+' to 'LGPLv2+'.

* Tue Mar 29 2011 Kalev Lember <kalev@smartlink.ee> - 1.4.2-2
- Don't install the udev rules

* Fri Feb 25 2011 Kalev Lember <kalev@smartlink.ee> - 1.4.2-1
- Update to 1.4.2

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 13 2010 Kalev Lember <kalev@smartlink.ee> - 1.4.1-1
- Update to 1.4.1

* Thu Dec 09 2010 Kalev Lember <kalev@smartlink.ee> - 1.4.0-4
- Install src/openct/LICENSE file as LICENSE.openct in docs (#660600)
- Added 'and GPLv2+' to license tag to cover RSA_SecurID (#660600)

* Tue Dec 07 2010 Kalev Lember <kalev@smartlink.ee> - 1.4.0-3
- Renamed ccid package to pcsc-lite-ccid (#654377)
- Mark files under reader.conf.d as config(noreplace)
- Don't mark udev rules as config

* Tue Dec 07 2010 Kalev Lember <kalev@smartlink.ee> - 1.4.0-2
- Removed ExcludeArch: s390 s390x as these arches now have libusb1
- Updated description

* Wed Aug 04 2010 Kalev Lember <kalev@smartlink.ee> - 1.4.0-1
- Update to 1.4.0
- Build against libusb1 instead of libusb 0.1
- Install libccidtwin configuration file
- Spec file clean up

* Sun Jul 04 2010 Kalev Lember <kalev@smartlink.ee> - 1.3.13-1
- Update to 1.3.13

* Thu Nov 19 2009 Kalev Lember <kalev@smartlink.ee> - 1.3.11-1
- Updated to ccid 1.3.11
- Removed iso-8859-1 to utf-8 conversion as the files are in utf-8 now

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Bob Relyea <rrelyea@redhat.com> - 1.3.9-1
- update to ccid 1.3.9

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Aug 26 2008 Bob Relyea <rrelyea@redhat.com> - 1.3.8-1
- update to ccid 1.3.8

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.1-4
- Autorebuild for GCC 4.3

* Mon Aug 20 2007 Bob Relyea <rrelyea@redhat.com> - 1.2.1-3
- Update License description to the new Fedora standard

* Mon Apr 30 2007 Bob Relyea <rrelyea@redhat.com> - 1.2.1-2
- Fix the missed use of the version macro

* Tue Feb 06 2007 Bob Relyea <rrelyea@redhat.com> - 1.2.1-1
- Pick up ccid 1.2.1
- use pcscd 'hotplug' feature instead of restarting the daemon
- add enable_udev

* Mon Nov 06 2006 Bob Relyea <rrelyea@redhat.com> - 1.1.0-2
- Fix version macro to remove '-'

* Thu Nov 02 2006 Bob Relyea <rrelyea@redhat.com> - 1.1.0-1
- Pickup ccid 1.1.0

* Thu Jul 20 2006 Florian La Roche <laroche@redhat.com> - 1.0.1-5
- require initscripts for post/postun

* Sun Jul 16 2006 Florian La Roche <laroche@redhat.com> - 1.0.1-4
- fix excludearch line

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.1-3.1
- rebuild

* Mon Jul 10 2006 Bob Relyea <rrelyea@redhat.com> - 1.0.1-3
- remove s390 from the build

* Mon Jun  5 2006 Bob Relyea <rrelyea@redhat.com> - 1.0.1-2
- Move to Fedora Core, removed %%{_dist}.

* Sat Apr 22 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0.1-1
- 1.0.1.

* Mon Mar  6 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0.0-1
- 1.0.0, license changed to LGPL.

* Wed Feb 15 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.1-7
- Rebuild.

* Thu Nov  3 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.4.1-6
- Clean up build dependencies.
- Convert docs to UTF-8.

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.4.1-5
- rebuilt

* Fri Feb 25 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.4.1-4
- Drop Epoch: 0.
- Improve summary.
- Build with dependency tracking disabled.

* Thu Jul  1 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.1-0.fdr.3
- Restart pcscd in post(un)install phase if it's available and running.

* Thu May 13 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.1-0.fdr.2
- Provide pcsc-ifd-handler (idea from Debian).

* Sat Feb 14 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.1-0.fdr.1
- Update to 0.4.1.

* Fri Feb 13 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.0-0.fdr.1
- Update to 0.4.0.

* Wed Nov  5 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.3.2-0.fdr.1
- Update to 0.3.2.
- Update URL.

* Thu Oct 16 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.3.1-0.fdr.1
- Update to 0.3.1.

* Wed Sep 10 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.3.0-0.fdr.1
- Update to 0.3.0.

* Wed Aug 27 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.2.0-0.fdr.1
- Update to 0.2.0.

* Tue Aug 19 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.1.0-0.fdr.1
- First build.
