%define cross 0

# Seabios is noarch, but required on architectures which cannot build it.
# Disable debuginfo because it is of no use to us.
%global debug_package %{nil}

# Similarly, tell RPM to not complain about x86 roms being shipped noarch
%global _binaries_in_noarch_packages_terminate_build   0

# You can build a debugging version of the BIOS by setting this to a
# value > 1.  See src/config.h for possible values, but setting it to
# a number like 99 will enable all possible debugging.  Note that
# debugging goes to a special qemu port that you have to enable.  See
# the SeaBIOS top-level README file for the magic qemu invocation to
# enable this.
%global debug_level 1

Summary:        Open-source legacy BIOS implementation
Name:           seabios
Version:        1.16.2
Release:        1%{?dist}
License:        GPLv3+ AND LGPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.seabios.org/SeaBIOS
Source0:        https://www.seabios.org/downloads/%{name}-%{version}.tar.gz
Source10:       config.vga-cirrus
Source11:       config.vga-isavga
Source12:       config.vga-qxl
Source13:       config.vga-stdvga
Source14:       config.vga-vmware
Source15:       config.csm
Source16:       config.coreboot
Source17:       config.seabios-128k
Source18:       config.seabios-256k
Source19:       config.vga-virtio
Source20:       config.vga-ramfb
Source21:       config.vga-bochs-display
Source22:       config.vga-ati
Source23:       config.seabios-microvm
Patch0001:      0001-Workaround-for-a-win8.1-32-S4-resume-bug.patch
Patch0003:      0003-vgabios-Reorder-video-modes-to-work-around-a-Windows.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  python3

%if 0%{?cross}
BuildRequires:  binutils-x86_64-linux-gnu
BuildRequires:  gcc-x86_64-linux-gnu
BuildArch:      noarch
%else
ExclusiveArch:  x86_64
%endif

Requires:       %{name}-bin = %{version}-%{release}
Requires:       seavgabios-bin = %{version}-%{release}

%description
SeaBIOS is an open-source legacy BIOS implementation which can be used as
a coreboot payload. It implements the standard BIOS calling interfaces
that a typical x86 proprietary BIOS implements.

%package bin
Summary:        Seabios for x86
BuildArch:      noarch

%description bin
SeaBIOS is an open-source legacy BIOS implementation which can be used as
a coreboot payload. It implements the standard BIOS calling interfaces
that a typical x86 proprietary BIOS implements.

%package -n seavgabios-bin
Summary:        Seavgabios for x86
BuildArch:      noarch

%description -n seavgabios-bin
SeaVGABIOS is an open-source VGABIOS implementation.

%prep
%autosetup -p1

%build
%define _lto_cflags %{nil}

# Need to discard ".note.gnu.property" section with "binutils" 2.36+ to avoid build breaks.
# See https://sourceware.org/bugzilla/show_bug.cgi?id=27753 for details.
sed -E -i "s|/DISCARD/ : \{|& *(.note.*)|" vgasrc/vgalayout.lds.S

mkdir binaries

build_bios() {
    make clean distclean
    cp $1 .config
    echo "CONFIG_DEBUG_LEVEL=%{debug_level}" >> .config
    make oldnoconfig V=1

    make V=1 \
        EXTRAVERSION="-%{release}" \
        PYTHON=python3 \
%if 0%{?cross}
        HOSTCC=gcc \
        CC=x86_64-linux-gnu-gcc \
        AS=x86_64-linux-gnu-as \
        LD=x86_64-linux-gnu-ld \
        OBJCOPY=x86_64-linux-gnu-objcopy \
        OBJDUMP=x86_64-linux-gnu-objdump \
        STRIP=x86_64-linux-gnu-strip \
%endif
        $4

    cp out/$2 binaries/$3
}

# seabios
build_bios %{_sourcedir}/config.seabios-128k bios.bin bios.bin
build_bios %{_sourcedir}/config.seabios-256k bios.bin bios-256k.bin
build_bios %{_sourcedir}/config.csm Csm16.bin bios-csm.bin
build_bios %{_sourcedir}/config.coreboot bios.bin.elf bios-coreboot.bin
build_bios %{_sourcedir}/config.seabios-microvm bios.bin bios-microvm.bin

# seavgabios
%global vgaconfigs bochs-display cirrus isavga qxl stdvga ramfb vmware virtio ati
for config in %{vgaconfigs}; do
    build_bios %{_sourcedir}/config.vga-${config} \
               vgabios.bin vgabios-${config}.bin out/vgabios.bin
done

%install
mkdir -p %{buildroot}%{_datadir}/seabios
mkdir -p %{buildroot}%{_datadir}/seavgabios
install -m 0644 binaries/bios.bin %{buildroot}%{_datadir}/seabios/bios.bin
install -m 0644 binaries/bios-256k.bin %{buildroot}%{_datadir}/seabios/bios-256k.bin
install -m 0644 binaries/bios-csm.bin %{buildroot}%{_datadir}/seabios/bios-csm.bin
install -m 0644 binaries/bios-coreboot.bin %{buildroot}%{_datadir}/seabios/bios-coreboot.bin
install -m 0644 binaries/bios-microvm.bin %{buildroot}%{_datadir}/seabios/bios-microvm.bin
install -m 0644 binaries/vgabios*.bin %{buildroot}%{_datadir}/seavgabios

%files
%license COPYING COPYING.LESSER
%doc README

%files bin
%dir %{_datadir}/seabios/
%{_datadir}/seabios/bios*.bin

%files -n seavgabios-bin
%dir %{_datadir}/seavgabios/
%{_datadir}/seavgabios/vgabios*.bin

%changelog
* Mon Jan 22 2024 Sindhu Karri <lakarri@microsoft.com> - 1.16.2-1
- Upgrade to 1.16.2

* Thu Aug 26 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.14.0-7
- License verified.
- Updated project's URL.
- Removing unused BR on "iasl".
- Manually discarding ".note.gnu.property" section from "vgalayout.lds.S"
  to fix build issues with "binutils" 2.36+.

* Thu Aug 26 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.14.0-6
- Initial CBL-Mariner import from Fedora 35 (license: MIT).
- Turn off cross-compilation.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 18 2021 Cole Robinson <crobinso@redhat.com> - 1.14.0-4
- Install vgabios-ati and bios-microvm

* Wed Jun 02 2021 Cole Robinson <crobinso@redhat.com> - 1.14.0-3
- Fix boot from nvme (bz 1963255)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Nov 24 2020 Cole Robinson <aintdiscole@gmail.com> - 1.14.0-1
- Update to 1.14.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 09 2019 Cole Robinson <aintdiscole@gmail.com> - 1.13.0-1
- Update to 1.13.0

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 11 2019 Cole Robinson <aintdiscole@gmail.com> - 1.12.1-2
- Add config.vga-ati from qemu 4.1

* Wed Mar 27 2019 Cole Robinson <aintdiscole@gmail.com> - 1.12.1-1
- Update to 1.12.1 for qemu 4.0

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Nov 17 2018 Cole Robinson <crobinso@redhat.com> - 1.12.0-1
- Rebase to version 1.12.0 for qemu-3.1.0

* Tue Jul 24 2018 Cole Robinson <crobinso@redhat.com> - 1.11.2-1
- Rebased to version 1.11.2
- Add BuildRequires: gcc (bz #1606326)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 22 2018 Cole Robinson <crobinso@redhat.com> - 1.11.1-1
- Rebased to version 1.11.1

* Mon Mar 19 2018 Paolo Bonzini <pbonzini@redhat.com> - 1.11.0-2
- Build with Python 3

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Nov 17 2017 Paolo Bonzini <pbonzini@redhat.com> - 1.11.0-1
- Rebased to version 1.11.0
- Add three patches from RHEL

* Fri Nov 17 2017 Paolo Bonzini <pbonzini@redhat.com> - 1.10.2-3
- Disable cross-compilation on RHEL

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 15 2017 Cole Robinson <crobinso@redhat.com> - 1.10.2-1
- Rebased to version 1.10.2

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Dec 04 2016 Cole Robinson <crobinso@redhat.com> - 1.10.1-1
- Rebased to version 1.10.1

* Wed Aug 03 2016 Cole Robinson <crobinso@redhat.com> - 1.9.3-1
- Rebased to version 1.9.3

* Thu Mar 24 2016 Paolo Bonzini <pbonzini@redhat.com> - 1.9.1-3
- Include MPT Fusion driver, in preparation for QEMU 2.6
- Include XHCI and SD in 128k ROM, sacrifice bootsplash instead

* Thu Mar 17 2016 Cole Robinson <crobinso@redhat.com> - 1.9.1-1
- Rebased to version 1.9.1
- Fix incorrect UUID format in boot output (bz #1284259)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 17 2015 Cole Robinson <crobinso@redhat.com> 1.9.0-1
- Rebased to version 1.9.0

* Tue Jul 14 2015 Cole Robinson <crobinso@redhat.com> 1.8.2-1
- Rebased to version 1.8.2

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 18 2015 Cole Robinson <crobinso@redhat.com> - 1.8.1-1
- Rebased to version 1.8.1

* Sat Feb 21 2015 Cole Robinson <crobinso@redhat.com> - 1.8.0-1
- Rebased to version 1.8.0
- Initial support for USB3 hubs
- Initial support for SD cards (on QEMU only)
- Initial support for transitioning to 32bit mode using SMIs (on QEMU TCG
  only)
- SeaVGABIOS improvements

* Sat Nov 15 2014 Cole Robinson <crobinso@redhat.com> - 1.7.5.1-1
- Update to seabios-1.7.5.1

* Wed Jul 09 2014 Cole Robinson <crobinso@redhat.com> - 1.7.5-3
- Fix PCI-e hotplug (bz #1115598)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 31 2014 Cole Robinson <crobinso@redhat.com> - 1.7.5-1
- Rebased to version 1.7.5
- Support for obtaining SMBIOS tables directly from QEMU.
- XHCI USB controller fixes for real hardware
- seavgabios: New driver for "coreboot native vga" support
- seavgabios: Improved detection of x86emu versions with incorrect
  emulation.
- Several bug fixes and code cleanups

* Wed Mar 26 2014 Matthias Clasen <mclasen@redhat.com> 1.7.4-5
- Fix booting FreeBSD VMs in virt-manager

* Mon Mar 17 2014 Cole Robinson <crobinso@redhat.com> 1.7.4-3
- Build 256k bios images for qemu 2.0

* Thu Mar 13 2014 Cole Robinson <crobinso@redhat.com> - 1.7.4-2
- Fix kvm migration with empty virtio-scsi controller (bz #1032208)

* Mon Jan 06 2014 Cole Robinson <crobinso@redhat.com> - 1.7.4-1
- Rebased to version 1.7.4
- Support for obtaining ACPI tables directly from QEMU.
- Initial support for XHCI USB controllers (initially for QEMU only).
- Support for booting from "pvscsi" devices on QEMU.
- Enhanced floppy driver - improved support for real hardware.
- coreboot cbmem console support.

* Tue Nov 19 2013 Cole Robinson <crobinso@redhat.com> - 1.7.3.2-1
- Update to 1.7.3.2 for qemu 1.7

* Thu Nov 14 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.7.3.1-3
- Fix pasto in CONFIG_DEBUG_LEVEL.

* Thu Nov 14 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.7.3.1-2
- Compile as all three of BIOS, CSM and CoreBoot payload.

* Wed Aug 14 2013 Cole Robinson <crobinso@redhat.com> - 1.7.3.1-1
- Rebased to version 1.7.3.1
- Fix USB EHCI detection that was broken in hlist conversion of
  PCIDevices.
- Fix bug in CBFS file walking with compressed files.
- acpi: sync FADT flags from PIIX4 to Q35

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 09 2013 Cole Robinson <crobinso@redhat.com> - 1.7.3-2
- Install aml files for use by qemu

* Mon Jul 08 2013 Cole Robinson <crobinso@redhat.com> - 1.7.3-1
- Rebased to version 1.7.3
- Initial support for using SeaBIOS as a UEFI CSM
- Support for detecting and using ACPI reboot ports.
- Non-standard floppy sizes now work again with recent QEMU versions.
- Several bug fixes and code cleanups
- Again fix vgabios obsoletes (bz #981147)

* Mon May 27 2013 Cole Robinson <crobinso@redhat.com> - 1.7.2.2-1
- Update to seabios stable 1.7.2.2
- Obsolete vgabios (bz #967315)

* Thu Jan 24 2013 Cole Robinson <crobinso@redhat.com> - 1.7.2-1
- Rebased to version 1.7.2
- Support for ICH9 host chipset ("q35") on emulators
- Support for booting from LSI MegaRAID SAS controllers
- Support for using the ACPI PM timer on emulators
- Improved Geode VGA BIOS support.
- Several bug fixes

* Thu Dec  6 2012 Peter Robinson <pbrobinson@fedoraproject.org> 1.7.1-4
- Root seabios package is noarch too because it only contains docs

* Fri Oct 19 2012 Cole Robinson <crobinso@redhat.com> - 1.7.1-3
- Add seavgabios subpackage

* Wed Oct 17 2012 Paolo Bonzini <pbonzini@redhat.com> - 1.7.1-2
- Build with cross compiler.  Resolves: #866664.

* Wed Sep 05 2012 Cole Robinson <crobinso@redhat.com> - 1.7.1-1
- Rebased to version 1.7.1
- Initial support for booting from USB attached scsi (USB UAS) drives
- USB EHCI 64bit controller support
- USB MSC multi-LUN device support
- Support for booting from LSI SCSI controllers on emulators
- Support for booting from AMD PCscsi controllers on emulators

* Mon Aug 13 2012 Richard W.M. Jones <rjones@redhat.com> - 1.7.0-4
- Modernise and tidy up the RPM.
- Allow debug versions of SeaBIOS to be built easily.

* Mon Aug 06 2012 Cole Robinson <crobinso@redhat.com> - 1.7.0-3
- Enable S3/S4 support for guests (it's an F18 feature after all)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 28 2012 Cole Robinson <crobinso@redhat.com> - 1.7.0-1
- Rebased to version 1.7.0
- Support for virtio-scsi
- Improved USB drive support
- Several USB controller bug fixes and improvements

* Wed Mar 28 2012 Paolo Bonzini <pbonzini@redhat.com> - 1.6.3-2
- Fix bugs in booting from host (or redirected) USB pen drives

* Wed Feb 08 2012 Justin M. Forbes <jforbes@redhat.com> - 1.6.3-1
- Update to 1.6.3 upstream
- Add virtio-scsi

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 05 2011 Justin M. Forbes <jforbes@redhat.com> - 0.6.2-3
- Stop advertising S3 and S4 in DSDT (bz#741375)
- incdule iasl buildreq

* Wed Jul 13 2011 Justin M. Forbes <jforbes@redhat.com> - 0.6.2-2
- Fix QXL bug in 0.6.2

* Wed Jul 13 2011 Justin M. forbes <jforbes@redhat.com> - 0.6.2-1
- Update to 0.6.2 upstream for a number of bugfixes

* Mon Feb 14 2011 Justin M. forbes <jforbes@redhat.com> - 0.6.1-1
- Update to 0.6.1 upstream for a number of bugfixes

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 10 2010 Justin M. Forbes <jforbes@redhat.com> 0.6.0-1
- Update seabios to latest stable so we can drop patches.

* Tue Apr 20 2010 Justin M. Forbes <jforbes@redhat.com> 0.5.1-2
- Ugly hacks to make package noarch and available for arch that cannot build it.
- Disable useless debuginfo

* Wed Mar 03 2010 Justin M. Forbes <jforbes@redhat.com> 0.5.1-1
- Update to 0.5.1 stable release
- Pick up patches required for current qemu

* Thu Jan 07 2010 Justin M. Forbes <jforbes@redhat.com> 0.5.1-0.1.20100108git669c991
- Created initial package
