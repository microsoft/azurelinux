Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: fxload
Version: 2008_10_13
Release: 17%{?dist}
Summary: A helper program to download firmware into FX and FX2 EZ-USB devices

License: GPLv2+
URL: https://linux-hotplug.sourceforge.net/
Source0: %{_distro_sources_url}/fxload-%{version}-noa3load.tar.gz
# The above file is derived from:
# https://downloads.sourceforge.net/project/linux-hotplug/fxload/2008_10_13/fxload-2008_10_13.tar.gz
# This file contains code that is copyright Cypress Semiconductor Inc,
# and cannot be distributed. Therefore we use this script to remove the
# copyright code before shipping it. Download the upstream tarball and
# invoke this script while in the tarball's directory:
# ./fxload-generate-tarball.sh 2008_10_13
Source1: fxload-generate-tarball.sh
Patch0: fxload-noa3load.patch
Patch1: fxload-cflags-ldflags.patch

BuildRequires: gcc kernel-headers
Requires: udev
Conflicts: hotplug-gtk hotplug

%description 
This program is conveniently able to download firmware into FX and FX2
EZ-USB devices, as well as the original AnchorChips EZ-USB.  It is
intended to be invoked by udev scripts when the unprogrammed device
appears on the bus.

%prep
%setup -q 
%patch 0 -p1 -b .fxload-noa3load
%patch 1 -p1 -b .cflags

%build 
make CC=gcc CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS"

%install
mkdir -p -m 755 %{buildroot}/sbin
install -m 755 fxload %{buildroot}/sbin
mkdir -p -m 755 %{buildroot}/%{_mandir}/man8/
install -m 644 fxload.8 %{buildroot}/%{_mandir}/man8/

%files
%license COPYING
%doc README.txt
%attr(0755, root, root) /sbin/fxload
%{_mandir}/*/*

%changelog
* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 2008_10_13-17
- Updating naming for 3.0 version of Azure Linux.

* Mon Apr 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2008_10_13-16
- Updating source URLs.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2008_10_13-15
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2008_10_13-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2008_10_13-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2008_10_13-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2008_10_13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Feb 25 2018 Charles R. Anderson <cra@wpi.edu> - 2008_10_13-10
- Patch to apply CFLAGS/LDFLAGS to final link so RPM_OPT_FLAGS are picked up (rhbz#1548426)
- Use CC=gcc explicitly
- Regenerate fxload-noa3load.patch

* Sun Feb 18 2018 Charles R. Anderson <cra@wpi.edu> - 2008_10_13-9
- add BR gcc
- remove Group:, BuildRoot: and rm -rf in install section

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2008_10_13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2008_10_13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2008_10_13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2008_10_13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2008_10_13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2008_10_13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2008_10_13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 16 2014 Charles R. Anderson <cra@wpi.edu> - 2008_10_13-1
- update to 2008_10_13 to support Cypress EZ-USB FX2LP parts (rhbz#1102654)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2002_04_11-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2002_04_11-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2002_04_11-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2002_04_11-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2002_04_11-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2002_04_11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2002_04_11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2002_04_11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 9 2008 Stephen Warren <s-t-rhbugzilla@wwwdotorg.org> - 2002_04_11-7
- Bump version to rebuild with gcc-4.3

* Sat Nov 17 2007 Stephen Warren <s-t-rhbugzilla@wwwdotorg.org> - 2002_04_11-6
- Rework the spec file formatting to match templates from rpmdev
- Be explicit about file attributes, just in case

* Sat Nov 17 2007 Stephen Warren <s-t-rhbugzilla@wwwdotorg.org> - 2002_04_11-5
- Updates after reading packaging guide-lines more thoroughly:
- Make license version more explicit
- Add generate-tarball.sh, and associated comments
- Added BuildRequires on kernel-headers
- Added COPYING as a doc
- Use dollar v.s. percent macros more consitently

* Fri Nov 16 2007 Stephen Warren <s-t-rhbugzilla@wwwdotorg.org> - 2002_04_11-4
- Repackage the source tarball to remove a3load.hex
- Added instructions to spec file on how to do the above
- Remove reference to a3load.hex from the man page too

* Thu Nov 15 2007 Stephen Warren <s-t-rhbugzilla@wwwdotorg.org> - 2002_04_11-3
- Update BuildRoot per Fedora wiki
- Fixed rpmlint complaint about not cleaning buildroot
- Updated source patch file to match latest kernel file layout
- Add patch to remove reference to non-shipped non-free a3load.hex firmware

* Fri Dec 8 2006 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> - 2002_04_11-2
- Fixed some rpmlint complaints
- Added patch to fix an include header
- Added dist tag

* Wed Apr 12 2006 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> - 2002_04_11-1
- First version of fxload spec based on hotplug spec
