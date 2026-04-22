# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global hash c3a19c1
%global date 20240913

# https://fedoraproject.org/wiki/Changes/SetBuildFlagsBuildCheck
# breaks cross-building
%undefine _auto_set_build_flags

# Disable unhelpful RPM test.
%global _binaries_in_noarch_packages_terminate_build 0

Name:           openbios
Version:        %{date}
Release: 2.git%{hash}%{?dist}
Epoch:          1
Summary:        OpenBIOS implementation of IEEE 1275-1994

License:        GPL-2.0-only
URL:            http://www.openfirmware.info/OpenBIOS
BuildArch:      noarch

# There are no upstream tarballs.  This tarball is prepared as follows:
#
# git clone https://github.com/openbios/openbios
# cd openbios
# hash=`git log -1 --format='%h'`
# date=`git log -1 --format='%cd' --date=short | tr -d -`
# git archive --prefix openbios-${date}-git${hash}/ ${hash} | xz -7e > ../openbios-${date}-git${hash}.tar.xz
Source0:        %{name}-%{date}-git%{hash}.tar.xz

# Note that these packages build 32 bit binaries with the -m32 flag.
BuildRequires: make
BuildRequires:  gcc-powerpc64-linux-gnu
BuildRequires:  gcc-sparc64-linux-gnu

BuildRequires:  gcc
BuildRequires:  fcode-utils
BuildRequires:  libxslt


ExclusiveArch: x86_64
%description
The OpenBIOS project provides you with most free and open source Open
Firmware implementations available. Here you find several
implementations of IEEE 1275-1994 (Referred to as Open Firmware)
compliant firmware. Among its features, Open Firmware provides an
instruction set independent device interface. This can be used to boot
the operating system from expansion cards without native
initialization code.

It is Open Firmware's goal to work on all common platforms, like x86,
AMD64, PowerPC, ARM and Mips. With its flexible and modular design,
Open Firmware targets servers, workstations and embedded systems,
where a sane and unified firmware is a crucial design goal and reduces
porting efforts noticably.

Open Firmware is found on many servers and workstations and there are
sever commercial implementations from SUN, Firmworks, CodeGen, Apple,
IBM and others.

In most cases, the Open Firmware implementations provided on this site
rely on an additional low-level firmware for hardware initialization,
such as coreboot or U-Boot.


%prep
%setup -q -n %{name}-%{date}-git%{hash}


%build
# Disable -Werror, cross-gcc-6.0.0-0.1.fc24 has some issues but they are fixed
# in gcc upstream
sed -i -e "s/-Werror/-Wno-error/" Makefile.target

/bin/sh config/scripts/switch-arch ppc
make build-verbose V=1 %{?_smp_mflags}
/bin/sh config/scripts/switch-arch sparc32
make build-verbose V=1 %{?_smp_mflags}
/bin/sh config/scripts/switch-arch sparc64
make build-verbose V=1 %{?_smp_mflags}


%install
qemudir=$RPM_BUILD_ROOT%{_datadir}/qemu
mkdir -p $qemudir
cp -a obj-ppc/openbios-qemu.elf $qemudir/openbios-ppc
cp -a obj-sparc32/openbios-builtin.elf $qemudir/openbios-sparc32
cp -a obj-sparc64/openbios-builtin.elf $qemudir/openbios-sparc64


%files
%doc COPYING
%doc README
%doc VERSION
%dir %{_datadir}/qemu
%{_datadir}/qemu/openbios-ppc
%{_datadir}/qemu/openbios-sparc32
%{_datadir}/qemu/openbios-sparc64


%changelog
* Mon Dec 15 2025 Daniel P. Berrangé <berrange@redhat.com> - 1:20240913-1.gitc3a19c1
- Update to openbios c3a19c1 to match qemu

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:20230126-6.gitaf97fd7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:20230126-5.gitaf97fd7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:20230126-4.gitaf97fd7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:20230126-3.gitaf97fd7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:20230126-2.gitaf97fd7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Aug 20 2023 Cole Robinson <crobinso@redhat.com> - 20230126-1.gitaf97fd7
- Update to openbios af97fd7

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:20200725-7.git7f28286
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:20200725-6.git7f28286
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:20200725-5.git7f28286
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:20200725-4.git7f28286
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:20200725-3.git7f28286
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:20200725-2.git7f28286
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 03 2020 Cole Robinson <aintdiscole@gmail.com> - 20200725-1.git7f282863.git
- Update to openbios 7f28286

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:20191022-3.git7e5b89e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:20191022-2.git7e5b89e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 12 2019 Cole Robinson <aintdiscole@gmail.com> - 20191022-1.git7e5b89e
- Update to openbios 7e5b89e for qemu-4.2

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:20190626-2.gitc79e0ec
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 11 2019 Cole Robinson <aintdiscole@gmail.com> - 20190626-1.gitc79e0ec
- Update to openbios c79e0ec for qemu-4.1

* Wed Mar 27 2019 Cole Robinson <aintdiscole@gmail.com> - 20190208-1.git3464681
- Update to openbios 3464681 for qemu-4.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20181005-2.git441a84d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 15 2018 Cole Robinson <crobinso@redhat.com> - 20181005-1.git441a84d
- Update to openbios 441a84d for qemu-3.1

* Tue Jul 31 2018 Cole Robinson <crobinso@redhat.com> - 20180609-1.git8fe6f5f
- Update to openbios 8fe6f5f for qemu-3.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20180213-2.git54d959d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 22 2018 Cole Robinson <crobinso@redhat.com> - 20180213-1.git54d959d
- Update to openbios 54d959d for qemu-2.12

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20171016-2.git83818bd
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Nov 20 2017 Cole Robinson <crobinso@redhat.com> - 20171016-1.git83818bd
- Update to openbios 83818bd for qemu-2.11

* Thu Aug 03 2017 Cole Robinson <crobinso@redhat.com> - 20170712-1.gitfbc1b4a
- Update to fbc1b4a for qemu 2.10

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170311-2.gitf233c3f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 21 2017 Cole Robinson <crobinso@redhat.com> - 20170311-1.gitf233c3f
- Update to f233c3f for qemu 2.9

* Wed Mar 15 2017 Cole Robinson <crobinso@redhat.com> - 20170213-1.git0cd97cc
- Update to 0cd97cc for qemu 2.9

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20161123-2.gitef8a14e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Dec 04 2016 Cole Robinson <crobinso@redhat.com> - 20161123-1.gitef8a14e
- Update to ef8a14e for qemu 2.8

* Mon Apr 18 2016 Cole Robinson <crobinso@redhat.com> 1.1.svn1395-1
- Update to r1395 for qemu 2.6

* Thu Apr 07 2016 Cole Robinson <crobinso@redhat.com> 1.1.svn1394-1
- Update to r1394, pulls in some -Werror fixes

* Sat Mar 05 2016 Cole Robinson <crobinso@redhat.com> 1.1.svn1378-3
- Disable -Werror, hitting issues on gcc6

* Fri Feb 05 2016 Cole Robinson <crobinso@redhat.com> 1.1.svn1378-2
- Update to r1378
- Fix build with latest cross-gcc (bz 1282890)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.svn1353-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 17 2015 Cole Robinson <crobinso@redhat.com> 1.1.svn1353-1
- Update to r1353 for qemu 2.5

* Tue Jul 14 2015 Cole Robinson <crobinso@redhat.com> 1.1.svn1340-1
- Update to r1340 for qemu 2.4

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.svn1334-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 18 2015 Cole Robinson <crobinso@redhat.com> 1.1.svn1334-1
- Update to r1334 for qemu 2.3

* Sat Nov 15 2014 Cole Robinson <crobinso@redhat.com> - 1.1.svn1321-1
- Update to r1321 for qemu 2.2

* Wed Jul 02 2014 Cole Robinson <crobinso@redhat.com> - 1.1.svn1306-1
- Update to svn1306 shipped with qemu 2.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.svn1280-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Mar 16 2014 Cole Robinson <crobinso@redhat.com> - 1.1.svn1280-1
- Update to openbios version queued for qemu 2.0

* Mon Dec 16 2013 Cole Robinson <crobinso@redhat.com> - 1.1.svn1239-1
- Update from SVN to fix building on arm

* Tue Nov 19 2013 Cole Robinson <crobinso@redhat.com> - 1.1.svn1229-1
- Update to svn1229 for qemu 1.7

* Tue Aug 20 2013 Cole Robinson <crobinso@redhat.com> 1.1.svn1198-1
- Update to svn1198 for qemu 1.6

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.svn1136-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 21 2013 Cole Robinson <crobinso@redhat.com> - 1.1.svn1136-1
- Update to openbios 1.1 for qemu 1.5

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.svn1063-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 16 2012 Paolo Bonzini <pbonzini@redhat.com> - 1.0.svn1063-1
- Move date from release to version.

* Mon Sep 17 2012 Cole Robinson <crobinso@redhat.com> - 1.0-6.svn1063
- Update to r1063, version qemu 1.2 shipped with

* Tue Jul 31 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0-5.svn1061
- Initial release in Fedora.
