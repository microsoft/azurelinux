# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# No, please don't break the build.  Thanks.
%undefine _auto_set_build_flags

%global buildarches %{ix86} x86_64
%ifnarch %{buildarches}
%global debug_package %{nil}
%endif

Summary: Simple kernel loader which boots from a FAT filesystem
Name: syslinux
Version: 6.04
%define tarball_version 6.04-pre1
Release: 0.33%{?dist}
License: GPL-2.0-or-later
URL: http://syslinux.zytor.com/wiki/index.php/The_Syslinux_Project
Source0: http://www.kernel.org/pub/linux/utils/boot/syslinux/%{name}-%{tarball_version}.tar.xz
Patch0001: 0001-Add-install-all-target-to-top-side-of-HAVE_FIRMWARE.patch
Patch0002: 0002-ext4-64bit-feature.patch
Patch0003: 0003-include-sysmacros-h.patch
Patch0004: 0004-Add-RPMOPTFLAGS-to-CFLAGS-for-some-stuff.patch
Patch0005: 0005-Workaround-multiple-definition-of-symbol-errors.patch
Patch0006: 0006-Replace-builtin-strlen-that-appears-to-get-optimized.patch
Patch0007: 0007-Fix-backspace-when-editing-a-multiline-cmdline.patch
Patch0008: 0008-Fix-build-with-GCC-14.patch
Patch0009: 0009-Rewrite_Digest_SHA1_to_SHA.patch
Patch0010: 0010-Fix-reported-SAST-findings.patch

# this is to keep rpmbuild from thinking the .c32 / .com / .0 / memdisk files
# in noarch packages are a reason to stop the build.
%define _binaries_in_noarch_packages_terminate_build 0

BuildRequires: make
BuildRequires: git
%ifarch %{buildarches}
BuildRequires:  gcc
BuildRequires: nasm >= 0.98.38-1, perl-interpreter, perl-generators, netpbm-progs
BuildRequires: perl(FileHandle)
BuildRequires: (glibc-devel(x86-32) or glibc32)
BuildRequires: libuuid-devel
Requires: syslinux-nonlinux = %{version}-%{release}
%endif
%ifarch %{ix86}
Requires: mtools, libc.so.6
BuildRequires: mingw32-gcc
%endif
%ifarch x86_64
Requires: mtools, libc.so.6()(64bit)
BuildRequires: mingw32-gcc mingw64-gcc
%endif

%description
SYSLINUX is a suite of bootloaders, currently supporting DOS FAT
filesystems, Linux ext2/ext3 filesystems (EXTLINUX), PXE network boots
(PXELINUX), or ISO 9660 CD-ROMs (ISOLINUX).  It also includes a tool,
MEMDISK, which loads legacy operating systems from these media.

%package perl
Summary: Syslinux tools written in perl

%description perl
Syslinux tools written in perl

%package devel
Summary: Headers and libraries for syslinux development.
Provides: %{name}-static = %{version}-%{release}

%description devel
Headers and libraries for syslinux development.

%package extlinux
Summary: The EXTLINUX bootloader, for booting the local system.
Requires: syslinux
Requires: syslinux-extlinux-nonlinux = %{version}-%{release}

%description extlinux
The EXTLINUX bootloader, for booting the local system, as well as all
the SYSLINUX/PXELINUX modules in /boot.

%ifarch x86_64
%package tftpboot
Summary: SYSLINUX modules in /tftpboot, available for network booting
BuildArch: noarch

%description tftpboot
All the SYSLINUX/PXELINUX modules directly available for network
booting in the /tftpboot directory.

%package extlinux-nonlinux
Summary: The parts of the EXTLINUX bootloader which aren't run from linux.
Requires: syslinux
BuildArch: noarch
ExclusiveArch: %{ix86} x86_64

%description extlinux-nonlinux
All the EXTLINUX binaries that run from the firmware rather than
from a linux host.

%package nonlinux
Summary: SYSLINUX modules which aren't run from linux.
Requires: syslinux
BuildArch: noarch
ExclusiveArch: %{ix86} x86_64

%description nonlinux
All the SYSLINUX binaries that run from the firmware rather than from a
linux host. It also includes a tool, MEMDISK, which loads legacy operating
systems from media.
%endif

%ifarch x86_64
%package efi64
Summary: SYSLINUX binaries and modules for 64-bit UEFI systems

%description efi64
SYSLINUX binaries and modules for 64-bit UEFI systems
%endif

%prep
%autosetup -S git_am -n syslinux-%{tarball_version}

%build
%ifarch %{buildarches}
make RPMCFLAGS='%{optflags}' RPMLDFLAGS='%{build_ldflags}' bios clean all
%endif
%ifarch x86_64
make RPMCFLAGS='%{optflags}' RPMLDFLAGS='%{build_ldflags}' efi64 clean all
%endif

%install
%ifarch %{buildarches}
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_prefix}/lib/syslinux
mkdir -p %{buildroot}%{_includedir}
make bios install-all \
	INSTALLROOT=%{buildroot} BINDIR=%{_bindir} SBINDIR=%{_sbindir} \
	LIBDIR=%{_prefix}/lib DATADIR=%{_datadir} \
	MANDIR=%{_mandir} INCDIR=%{_includedir} \
	TFTPBOOT=/tftpboot EXTLINUXDIR=/boot/extlinux \
	LDLINUX=ldlinux.c32
%ifarch x86_64
make efi64 install netinstall \
	INSTALLROOT=%{buildroot} BINDIR=%{_bindir} SBINDIR=%{_sbindir} \
	LIBDIR=%{_prefix}/lib DATADIR=%{_datadir} \
	MANDIR=%{_mandir} INCDIR=%{_includedir} \
	TFTPBOOT=/tftpboot EXTLINUXDIR=/boot/extlinux \
	LDLINUX=ldlinux.c32
%endif

mkdir -p %{buildroot}%{_pkgdocdir}/sample
install -m 644 sample/sample.* %{buildroot}%{_pkgdocdir}/sample/
mkdir -p %{buildroot}/etc
( cd %{buildroot}/etc && ln -s ../boot/extlinux/extlinux.conf . )

# don't ship libsyslinux, at least, not for now
rm -f %{buildroot}%{_prefix}/lib/libsyslinux*
rm -f %{buildroot}%{_includedir}/syslinux.h
%endif

%ifarch %{buildarches}
%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README*
%doc doc/* 
%doc sample
%{_mandir}/man1/gethostip*
%{_mandir}/man1/syslinux*
%{_mandir}/man1/isohybrid*
%{_mandir}/man1/memdiskfind*
%{_bindir}/gethostip
%{_bindir}/isohybrid
%{_bindir}/memdiskfind
%{_bindir}/syslinux
%dir %{_datadir}/syslinux
%dir %{_datadir}/syslinux/dosutil
%{_datadir}/syslinux/dosutil/*
%dir %{_datadir}/syslinux/diag
%{_datadir}/syslinux/diag/*
%ifarch %{ix86}
%{_datadir}/syslinux/syslinux.exe
%else
%{_datadir}/syslinux/syslinux64.exe
%endif

%files perl
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_mandir}/man1/lss16toppm*
%{_mandir}/man1/ppmtolss16*
%{_mandir}/man1/syslinux2ansi*
%{_bindir}/keytab-lilo
%{_bindir}/lss16toppm
%{_bindir}/md5pass
%{_bindir}/mkdiskimage
%{_bindir}/ppmtolss16
%{_bindir}/pxelinux-options
%{_bindir}/sha1pass
%{_bindir}/syslinux2ansi
%{_bindir}/isohybrid.pl

%files devel
%{!?_licensedir:%global license %%doc}
%license COPYING
%dir %{_datadir}/syslinux/com32
%{_datadir}/syslinux/com32/*

%files extlinux
%{_sbindir}/extlinux
%{_mandir}/man1/extlinux*
%config /etc/extlinux.conf

%ifarch x86_64
%files tftpboot
/tftpboot

%files nonlinux
%{_datadir}/syslinux/*.com
%{_datadir}/syslinux/*.exe
%{_datadir}/syslinux/*.c32
%{_datadir}/syslinux/*.bin
%{_datadir}/syslinux/*.0
%{_datadir}/syslinux/memdisk

%files extlinux-nonlinux
/boot/extlinux

%else
%exclude %{_datadir}/syslinux/memdisk
%exclude %{_datadir}/syslinux/*.com
%exclude %{_datadir}/syslinux/*.exe
%exclude %{_datadir}/syslinux/*.c32
%exclude %{_datadir}/syslinux/*.bin
%exclude %{_datadir}/syslinux/*.0
%exclude /boot/extlinux
%exclude /tftpboot
%endif

%ifarch x86_64
%files efi64
%{!?_licensedir:%global license %%doc}
%license COPYING
%dir %{_datadir}/syslinux/efi64
%{_datadir}/syslinux/efi64
%endif

%post extlinux
# If we have a /boot/extlinux.conf file, assume extlinux is our bootloader
# and update it.
if [ -f /boot/extlinux/extlinux.conf ]; then \
	extlinux --update /boot/extlinux ; \
elif [ -f /boot/extlinux.conf ]; then \
	mkdir -p /boot/extlinux && \
	mv /boot/extlinux.conf /boot/extlinux/extlinux.conf && \
	extlinux --update /boot/extlinux ; \
fi
%endif

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-0.33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Apr 29 2025 Leo Sandoval <lsandova@redhat.com> - 6.04-0.32
- Remove _sbindir macro, it is not required anymore
- Resolves: #2362819

* Wed Feb 19 2025 Leo Sandoval <lsandova@redhat.com> - 6.04-0.31
- Fix true positives SAST findings

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-0.30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-0.29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 10 2024 Michal Josef Špaček <mspacek@redhat.com> - 6.04-0.28
- Rewrite Digest::SHA1 to SHA

* Wed Jun 26 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 6.04-0.27
- Build tftpboot and nonlinux on x86_64

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-0.26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Dec 13 2023 Nicolas Frayer <nfrayer@redhat.com>
- Migrate to SPDX license
- Please refer to https://fedoraproject.org/wiki/Changes/SPDX_Licenses_Phase_2

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-0.25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-0.24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-0.23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 27 2022 Robbie Harwood <rharwood@redhat.com> - 6.04-0.22
- Cope with Fedora insisting harder on default buildflags
- Resolves: #2047034

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-0.21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Oct 21 2021 Robbie Harwood <rharwood@redhat.com> - 6.04-0.20
- Fix behavior of backspace in multiline cmdline editing

* Wed Sep 01 2021 Robbie Harwood <rharwood@redhat.com> - 6.04-0.19
- Place extlinux(1) in the extlinux subpackage
- Resolves: #977004

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-0.18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-0.17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-0.16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed May 13 2020 Merlin Mathesius <mmathesi@redhat.com> - 6.04-0.15
- Patches to fix FTBFS in F32/F33/ELN (RHBZ#1800180)

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-0.14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Sep 27 2019 Javier Martinez Canillas <javierm@redhat.com> - 6.04-0.13
- Fix a bunch of annocheck problems (pjones)
- Drop x86_64 ExclusiveArch for tftpboot subpackage
- Make tftpboot subpackage completely noarch (yselkowi)

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-0.12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 10 2019 Scott Talbert <swt@techie.net> - 6.04-0.11
- Add upstream patch to include sysmacros.h to fix FTBFS (#1676107)

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-0.10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-0.9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-0.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Nov 26 2017 Robert Scheck <robert@fedoraproject.org> - 6.04-0.7
- Add upstream patch for ext4 64bit feature (#1369934)

* Mon Nov 20 2017 Robert Scheck <robert@fedoraproject.org> - 6.04-0.6
- Correct non-existent macro %%{x86_64} to x86_64 (#1312748)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-0.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Mar 25 2017 Robert Scheck <robert@fedoraproject.org> - 6.04-0.3
- Own %%{_datadir}/syslinux/diag directory (#894529)
- Allow rebuilding on RHEL/CentOS 6 and 7 (#1291428)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 04 2016 Peter Jones <pjones@redhat.com> - - 6.04-0.1
- Update to 6.04-pre1
  Resolves: rhbz#1135793

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.03-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Oct 15 2015 Adam Williamson <awilliam@redhat.com> - 6.03-6
- backport GCC 5 fixes from upstream ML: RHBZ #1263988, #1264012

* Fri Jul 03 2015 Adam Williamson <awilliam@redhat.com> - 6.03-5
- backport a commit from git master which appears to fix RHBZ #1234653

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 6.03-3
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sat Jan 10 2015 Michael Schwendt <mschwendt@fedoraproject.org> - 6.03-2
- Add -static Provides to -devel package to meet Fedora's
  Packaging Static Libraries guidelines (rhbz #609617)

* Wed Oct 08 2014 Peter Jones <pjones@redhat.com> - 6.03-1
- Update to 6.03

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.02-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug  5 2014 Tom Callaway <spot@fedoraproject.org> - 6.02-6
- fix license handling

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.02-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Peter Jones <pjones@redhat.com> - 6.02-4
- Do our firmware/nonlinux packages as .noarch + ExclusiveArch
  Related: rhbz#1086446

* Tue Apr 15 2014 Peter Jones <pjones@redhat.com> - 6.02-3
- -2 was entirely the wrong thing to do.

* Tue Apr 15 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 6.02-2
- Undo packaging changes that break live image composes (#1086446)

* Tue Apr 08 2014 Peter Jones <pjones@redhat.com> - 6.02-1
- Update this to 6.02

* Mon Aug 05 2013 Peter Jones <pjones@redhat.com> - 4.05-7
- Fixing %%doc path.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.05-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 4.05-6
- Perl 5.18 rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug 06 2012 Peter Jones <pjones@redhat.com> - 4.05-4
- Fix build problem from kernel-headers' removeal of ext2_fs.h
  (fix backported from as-yet-unreleased upstream version.)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 4.05-2
- Remove old Obsoletes/Provides for syslinux-devel as such a subpkg
  was introduced with 3.83-2 (#756733).

* Wed Feb 15 2012 Matthew Garrett <mjg@redhat.com> - 4.05-1
- New upstream release
- syslinux-isohybrid-fix-mbr.patch: generate a full MBR for UEFI images

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.02-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 24 2011 Matthew Garrett <mjg@redhat.com> - 4.02-5
- Add support for building Mac and GPT bootable hybrid images

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 20 2010 Matt Domsch <mdomsch@fedoraproject.org> - 4.02-2
- add perl subpackage, move perl apps there

* Fri Aug 06 2010 Peter Jones <pjones@redhat.com> - 4.02-2
- Split out extlinux and tftpboot.
- remove duplicate syslinux/com32/ left in base package after 3.83-2

* Thu Aug 05 2010 Peter Jones <pjones@redhat.com> - 4.02-1
- Update to 4.02

* Mon Jan 11 2010 Peter Jones <pjones@redhat.com> - 3.84-1
- Update to 3.84

* Thu Dec 17 2009 Peter Jones <pjones@redhat.com> - 3.83-2
- Split out -devel

* Thu Oct 29 2009 Peter Jones <pjones@redhat.com> - 3.83-1
- update to 3.83

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.75-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 28 2009 Jeremy Katz <katzj@redhat.com> - 3.75-3
- Stop suppressing requirements of the package (#465299)

* Tue Apr 28 2009 Jeremy Katz <katzj@redhat.com> - 3.75-2
- Don't strip binaries to fix debuginfo (#249970)

* Thu Apr 16 2009 Jeremy Katz <katzj@redhat.com> - 3.75-1
- update to 3.75

* Fri Apr 10 2009 Jeremy Katz <katzj@redhat.com> - 3.74-1
- update to 3.74

* Fri Feb 27 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 3.73-2
- fix arch issues 

* Fri Feb 27 2009 Jeremy Katz <katzj@redhat.com> - 3.73-1
- Update to 3.73

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.61-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Sep  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.61-3
- fix license tag

* Mon Feb 25 2008 Peter Jones <pjones@redhat.com> - 3.61-2
- Remove 16bpp patch, hpa says that's there to cover a bug that's fixed.
- Remove x86_64 patch; building without it works now.

* Thu Feb 21 2008 Peter Jones <pjones@redhat.com> - 3.61-1
- Update to 3.61 .

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.36-9
- Autorebuild for GCC 4.3

* Wed Jan 09 2008 Florian La Roche <laroche@redhat.com> - 3.36-8
- spec in utf-8
- add URL tag
- own /usr/share/syslinux (rhbz#427816)

* Wed Oct 17 2007 Peter Jones <pjones@redhat.com> - 3.36-7
- Add necessary files for makebootfat to make usb images (patch from
  Joel Granados <jgranado@redhat.com>)

* Wed Oct  3 2007 Jeremy Katz <katzj@redhat.com> - 3.36-6
- fix menu system memory corruption (#239585)

* Tue Aug 14 2007 Jeremy Katz <katzj@redhat.com> - 3.36-5
- backport "menu hidden" support from upstream git

* Fri May  4 2007 Jeremy Katz <katzj@redhat.com> - 3.36-4
- switch to preferring 16bpp for graphical menu; this fixes the display for 
  qemu, kvm, etc

* Tue May  1 2007 Jeremy Katz <katzj@redhat.com> - 3.36-3
- fix countdown on boot images (#229491)

* Tue Apr 03 2007 Florian La Roche <laroche@redhat.com> - 3.36-2
- add upstream patch from 3.3x branch

* Mon Feb 12 2007 Florian La Roche <laroche@redhat.com> - 3.36-1
- update to 3.36

* Thu Feb 08 2007 Florian La Roche <laroche@redhat.com> - 3.35-1
- update to 3.35

* Thu Jan 18 2007 Jesse Keating <jkeating@redhat.com> - 3.31-2
- Make syslinux own /usr/lib/syslinux.

* Wed Jan 17 2007 Jeremy Katz <katzj@redhat.com> - 3.31-1
- update to 3.31

* Tue Aug 22 2006 Jesse Keating <jkeating@redhat.com> - 3.11-4
- Obsolete syslinux-devel.
- Couple cleanups for packaging guidelines

* Fri Jul 14 2006 David Cantrell <dcantrell@redhat.com> - 3.11-3
- Remove com32/include/time.h and com32/include/sys/times.h
- Replace CLK_TCK macros with CLOCKS_PER_SEC

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.11-2.1
- rebuild

* Mon Jun 12 2006 Peter Jones <pjones@redhat.com> - 3.11-2
- Fold -devel subpackage into "syslinux"

* Mon Jun 05 2006 Jesse Keating <jkeating@redhat.com> - 3.10-5
- Use the actual file as a BuildRequire

* Mon Jun 05 2006 Jesse Keating <jkeating@redhat.com> - 3.10-4
- Changed glibc-devel to glibc32 to get the 32bit package in

* Mon Jun 05 2006 Jesse Keating <jkeating@redhat.com> - 3.10-3
- Added missing glibc-devel BuildRequires

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.10-2.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Aug 22 2005 Peter Jones <pjones@redhat.com> - 3.10-2
- Update to 3.10
- Don't do "make clean", so we actually ship the bins hpa gives us

* Sat Jul  9 2005 Peter Jones <pjones@redhat.com> - 3.09-2
- Update to 3.09

* Thu Jun 16 2005 Peter Jones <pjones@redhat.com> - 3.08.92-1
- Update to 3.09-pre2, to fix the i915 .bss overflow bug

* Thu May 19 2005 Peter Jones <pjones@redhat.com> - 3.08-3
- Fix filespec for samples in -devel

* Thu May 19 2005 Peter Jones <pjones@redhat.com> - 3.08-2
- update to 3.08

* Wed Mar 16 2005 Peter Jones <pjones@redhat.com> - 3.07-2
- gcc4 update

* Thu Jan 13 2005 Peter Jones <pjones@redhat.com> - 3.07-1
- update to 3.07

* Tue Jan 11 2005 Peter Jones <pjones@redhat.com> - 3.06-1
- update to 3.06 , which should fix the directory parsing bug that wedges it
  with diskboot.img
- change README to README* in doc, to include README.menu and README.usbkey

* Tue Jan  4 2005 Peter Jones <pjones@redhat.com> - 3.02-2
- Beehive doesn't let you build in scratch and then build someplace else,
  arrrrgh.

* Tue Jan  4 2005 Peter Jones <pjones@redhat.com> - 3.02-1
- 3.02
- Make the spec a little closer to hpa's.

* Mon Jan  3 2005 Peter Jones <pjones@redhat.com> - 3.00-2
- make tag says the tag is there, make build says it's not.
  Bump release, try again.

* Mon Jan  3 2005 Peter Jones <pjones@redhat.com> - 3.00-1
- 3.00

* Mon Aug 16 2004 Jeremy Katz <katzj@redhat.com> - 2.11-1
- 2.11

* Fri Jul 30 2004 Jeremy Katz <katzj@redhat.com> - 2.10-1
- update to 2.10

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Apr 17 2004 Jeremy Katz <katzj@redhat.com> 2.0.8-3
- add syslinux-nomtools binary to be used for creating some installer images

* Tue Feb 17 2004 Jeremy Katz <katzj@redhat.com> 
- add netpbm-progs BuildRequires (#110255)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Dec 14 2003 Jeremy Katz <katzj@redhat.com> 2.08-1
- 2.08

* Fri Aug 22 2003 Jeremy Katz <katzj@redhat.com> 2.06-1
- 2.06

* Thu Aug 14 2003 Jeremy Katz <katzj@redhat.com> 2.05-1
- update to 2.05

* Mon Apr 21 2003 Jeremy Katz <katzj@redhat.com> 2.04-2
- add patch for samples to build on x86_64
- integrate some changes from upstream specfile (#88593)

* Fri Apr 18 2003 Jeremy Katz <katzj@redhat.com> 2.04-1
- update to 2.04

* Mon Feb  3 2003 Jeremy Katz <katzj@redhat.com> 2.01-1
- update to 2.01

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 14 2003 Jeremy Katz <katzj@redhat.com> 2.00-3
- fix deps for x86_64

* Wed Nov 27 2002 Tim Powers <timp@redhat.com> 2.00-2
- build on both x86_64 and i386

* Fri Nov  1 2002 Jeremy Katz <katzj@redhat.com>
- update to 2.00
- add additional files as requested by hpa (#68073)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jun 18 2002 Jeremy Katz <katzj@redhat.com>
- lss16toppm and ppmtolss16 are both perl scripts... turn off find-requires
  so we don't suck in perl as a dependency for syslinux

* Mon Jun 17 2002 Jeremy Katz <katzj@redhat.com>
- update to 1.75
- include tools to create graphical image format needed by syslinux
- include isolinux 
- include pxelinux (#64942)

* Fri Jun 14 2002 Preston Brown <pbrown@redhat.com>
- upgrade to latest version w/graphical screen support

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Sat Feb 10 2001 Matt Wilson <msw@redhat.com>
- 1.52

* Wed Jan 24 2001 Matt Wilson <msw@redhat.com>
- 1.51pre7

* Mon Jan 22 2001 Matt Wilson <msw@redhat.com>
- 1.51pre5

* Fri Jan 19 2001 Matt Wilson <msw@redhat.com>
- 1.51pre3, with e820 detection

* Tue Dec 12 2000 Than Ngo <than@redhat.com>
- rebuilt with fixed fileutils

* Thu Nov 9 2000 Than Ngo <than@redhat.com>
- update to 1.49
- update ftp site
- clean up specfile
- add some useful documents

* Tue Jul 18 2000 Nalin Dahyabhai <nalin@redhat.com>
- add %%defattr (release 4)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jul 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%{_tmppath}
- change application group (Applications/Internet doesn't seem
  right to me)
- added BuildRequires

* Tue Apr 04 2000 Erik Troan <ewt@redhat.com>
- initial packaging
