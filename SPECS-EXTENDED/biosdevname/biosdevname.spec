Name:		biosdevname
Version:	0.7.3
Release:	7%{?dist}
Summary:	Udev helper for naming devices per BIOS names
License:	GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:		https://github.com/dell/biosdevname
# SMBIOS only exists on these arches.  It's also likely that other
# arches don't expect the PCI bus to be sorted breadth-first, or of
# so, there haven't been any comments about that on LKML.
ExclusiveArch:	%{ix86} x86_64
Source0:	https://github.com/dell/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  pciutils-devel
BuildRequires:  zlib-devel

Patch1: 0001-Disable-biosdevname-by-default.patch
Patch2: 0002-Place-udev-rules-to-usr-lib.patch

%description
biosdevname in its simplest form takes a kernel device name as an
argument, and returns the BIOS-given name it "should" be.  This is necessary
on systems where the BIOS name for a given device (e.g. the label on
the chassis is "Gb1") doesn't map directly and obviously to the kernel
name (e.g. eth0).

%prep
%setup -q
%autopatch

%build
autoreconf -fvi
%configure --prefix=%{_prefix}
make %{?_smp_mflags}

%install
make install install-data DESTDIR=%{buildroot}

%files
%license COPYING
%doc README
%{_sbindir}/%{name}
%{_prefix}/lib/udev/rules.d/*.rules
%{_mandir}/man1/%{name}.1*

%changelog
* Wed Jan 12 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.7.3-7
- License verified.
- Updated source and project URLs.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.7.3-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 22 2018 Michal Sekletar <msekleta@redhat.com> - 0.7.3-1
- rebase to biosdevname-0.7.3

* Wed Mar 21 2018 Michal Sekletar <msekleta@redhat.com> - 0.7.2-1
- rebase to biosdevname-0.7.2

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 26 2015 Michal Sekletar <msekleta@redhat.com> - 0.6.2-1
- Rebase to 0.6.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Sep 02 2013 Harald Hoyer <harald@redhat.com> 0.5.0-2
- not only NAME KERNEL=="eth*", but every ethernet device

* Tue Jul 30 2013 Václav Pavlín <vpavlin@redhat.com> - 0.5.0-1
- Updating the sources to 0.5.0 version. Following are the changes:
- Change scan of SMBIOS slot <-> PCI methods, recurse to set SMBIOS slot field
- Save off secondary bus of PCI device for PCI tree traversal
- Add version number to biosdevname

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 14 2012 Václav Pavlín <vpavlin@redhat.com> - 0.4.1-3
- Source link update

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Praveen K Paladugu <praveen_paladugu@dell.com> - 0.4.1-1
- Fix autoconfig for Fedora systems
- Make sure that vpd scan only runs on Dell systems, also blacklist Atheros
  wireless cards which hang when vpd is read.
- Add fixes to biosdevname to support cards that export multiple network
  ports per PCI device (chelsio/mellanox).



* Thu May 3 2012 Praveen K Paladugu <praveen_paladugu@dell.com> - 0.4.0-1
- Create detached signature
- Fix man page to use new naming convention
- Remove unused variables from Stephen Hemminger [shemminger@vyatta.com]
- Use Physical device for slot numbering for embedded SR-IOV cards
- Add tracking of ifindex to eths structure
- Fix naming for add-in network adapters when SMBIOS version is invalid
- Read VPD-R on Dell systems only

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct  4 2011 Praveen K Paladugu <praveen_paladugu@dell.com> - 0.3.11-5
- Added automake as a build dependency

* Tue Oct  4 2011 Praveen K Paladugu <praveen_paladugu@dell.com> - 0.3.11-4
- Added autoconf as a build dependency

* Tue Oct  4 2011 Praveen K Paladugu <praveen_paladugu@dell.com> - 0.3.11-3
- Generating the configure script if it doesn't exist

* Tue Oct  4 2011 Praveen K Paladugu <praveen_paladugu@dell.com> - 0.3.11-2
- Fixed the dir structure inside the archive

* Tue Oct  4 2011 Praveen K Paladugu <praveen_paladugu@dell.com> - 0.3.11-1
- Updating the sources to 0.3.11 version. Following are the changes:
- Fix man page for PCI slot naming
- Fix clearing of buffer for NPAR/SRIOV naming
- Add --nopirq and --smbios options to manpage.
- Verify length of VPD on network device
- Close file handle on sysfs read
- Fix naming policy for NPAR devices.
  Match each PCI device to its VPD 'physical' device to get correct index
- Exclude  building on ia64 arch
- Add support functions for determining PCIE slot
- Scan full path to parent when getting PCIE slot
- Fix NPAR naming for add-in cards
- Don't display _vf suffix on NPAR devices with single function
- Fix PCIe/PIRQ slot mapping

* Thu Apr 21 2011 Praveen K Paladugu <praveen_paladugu@dell.com> - 0.3.8-1
- Add changes to parse VPD structure for device mapping on NPAR devices
- Fix pathname
- Cleanup and comment NPAR code
- Fix debian packaging rules to regenerate configure script
- Change pciX to pX for shortened names for PCI add-on devices
- Fix manpage typo
- Delete CR-LF in script
- Change default signing key
- Add command line arguments for checking SMBIOS version and ignore $PIRQ.

* Thu Feb 17 2011 Matt Domsch <Matt_Domsch@dell.com> - 0.3.7-1
- drop dump_pirq, suggest use biosdecode instead
- don't use '#' in names, use 'p' instead, by popular demand
- properly look for SMBIOS, then $PIR, then recurse
- Add kernel command line parameter "biosdevname={0|1}" to turn off/on biosdevname
- Fix segfault when BIOS advertises zero sized PIRQ Routing Table
- Add 'bonding' and 'openvswitch' to the virtual devices list
- fail PIRQ lookups if device domain is not 0
- Don't suggest names if running in a virtual machine (Xen, KVM,
  VMware tested, but should work on others)
- Typo fixes

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Matt Domsch <Matt_Domsch@dell.com> - 0.3.6-1
- drop biosdevnameS, it's unused and fails to build on F15

* Tue Jan 25 2011 Matt Domsch <Matt_Domsch@dell.com> - 0.3.5-1
- install dump_pirq into /usr/sbin
- fix udev rule, skip running if NAME is already set
- move udev rule to /lib/udev/rules.d by default

* Thu Dec 16 2010 Matt Domsch <mdomsch@fedoraproject.org> - 0.3.4-1
- drop unnecessary explicit version requirement on udev
- bugfix: start indices at 1 not 0, to match Dell and HP server port designations
- bugfix: don't assign names to unknown devices
- bugfix: don't assign duplicate names

* Thu Dec  9 2010 Matt Domsch <Matt_Domsch@dell.com> - 0.3.3-1
- add back in use of PCI IRQ Routing Table, if info is not provided by
  sysfs or SMBIOS

* Thu Dec  2 2010 Matt Domsch <Matt_Domsch@dell.com> - 0.3.2-1
- fix for multi-port cards with bridges
- removal of code for seriously obsolete systems

* Sun Nov 28 2010 Matt Domsch <Matt_Domsch@dell.com> 0.3.1-1
- remove all policies except 'physical' and 'all_ethN'
- handle SR-IOV devices properly

* Wed Nov 10 2010 Matt Domsch <Matt_Domsch@dell.com> 0.3.0-1
- add --policy=loms, make it default
- read index and labels from sysfs if available

* Mon Jul 27 2009 Jordan Hargrave <Jordan_Hargrave@dell.com> 0.2.5-1
- fix mmap error checking

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue May 06 2008 Matt Domsch <Matt_Domsch@dell.com> 0.2.4-5
- use policy=all_names to find breakage

* Sun Feb 10 2008 Matt Domsch <Matt_Domsch@dell.com> 0.2.4-4
- rebuild for gcc43

* Fri Sep 21 2007 Matt Domsch <Matt_Domsch@dell.com> 0.2.4-3
- fix manpage entry in files
 
* Fri Sep 21 2007 Matt Domsch <Matt_Domsch@dell.com> 0.2.4-2
- rebuild with Requires: udev > 115-3.20070920git

* Fri Sep 21 2007 Matt Domsch <Matt_Domsch@dell.com> 0.2.4-1
- coordinate udev rules usage with udev maintainer
- fix crashes in pcmcia search, in_ethernet(), and incorrect command
  line parsing.

* Mon Aug 27 2007 Matt Domsch <Matt_Domsch@dell.com> 0.2.3-1
- eliminate libbiosdevname.*, pre and post scripts

* Fri Aug 24 2007 Matt Domsch <Matt_Domsch@dell.com> 0.2.2-1
- ExclusiveArch those arches with SMBIOS and PCI IRQ Routing tables
- eliminate libsysfs dependency, move app to / for use before /usr is mounted.
- build static

* Mon Aug 20 2007 Matt Domsch <Matt_Domsch@dell.com> 0.2.1-1
- initial release
