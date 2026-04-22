# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: fxload
Version: 2008_10_13
Release: 34%{?dist}
Summary: A helper program to download firmware into FX and FX2 EZ-USB devices

License: GPL-2.0-or-later
URL: http://linux-hotplug.sourceforge.net/
Source0: fxload-%{version}-noa3load.tar.gz
# The above file is derived from:
# http://downloads.sourceforge.net/project/linux-hotplug/fxload/2008_10_13/fxload-2008_10_13.tar.gz
# This file contains code that is copyright Cypress Semiconductor Inc,
# and cannot be distributed. Therefore we use this script to remove the
# copyright code before shipping it. Download the upstream tarball and
# invoke this script while in the tarball's directory:
# ./fxload-generate-tarball.sh 2008_10_13
Source1: fxload-generate-tarball.sh
Patch0: fxload-noa3load.patch
Patch1: fxload-ldflags.patch

BuildRequires: gcc kernel-headers make
Requires: udev
Conflicts: hotplug-gtk hotplug

%description
This program is conveniently able to download firmware into FX and FX2
EZ-USB devices, as well as the original AnchorChips EZ-USB.  It is
intended to be invoked by udev scripts when the unprogrammed device
appears on the bus.

%prep
%setup -q
%patch -P0 -p1 -b .fxload-noa3load
%patch -P1 -p1 -b .ldflags

%build
%{make_build} CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS -pie"

%install
install -m 755 -Dt %{buildroot}%{_sbindir}/ fxload
install -m 644 -Dt %{buildroot}%{_mandir}/man8/ fxload.8

%files
%doc COPYING
%doc README.txt
%{_sbindir}/fxload
%{_mandir}/man8/fxload.8*

%changelog
* Wed Oct 22 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2008_10_13-33
- Use %%_sbindir for the binary (rhbz#2405414)

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2008_10_13-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2008_10_13-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Dec 18 2024 Jaroslav Kysela <perex@perex.cz> - 2008_10_13-29
- use /usr/sbin directory

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2008_10_13-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2008_10_13-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2008_10_13-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep  7 2023 Jaroslav Kysela <perex@perex.cz> - 2008_10_13-25
- SPDX license

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2008_10_13-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2008_10_13-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2008_10_13-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2008_10_13-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2008_10_13-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2008_10_13-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 08 2020 Charles R. Anderson <cra@alum.wpi.edu> - 2008_10_13-18
- BR: make

* Tue Dec 08 2020 Charles R. Anderson <cra@alum.wpi.edu> - 2008_10_13-17
- Merge PR#2: Make annocheck pass, pass -pie to linker, use make_build macro

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2008_10_13-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Feb 03 2020 Tom Stellard <tstellar@redhat.com> - 2008_10_13-15
- Use __cc macro instead of hard-coding gcc

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

