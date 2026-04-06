# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# ROMS we want for QEMU with format PCIID:QEMUNAME
%global qemuroms \\\
  8086100e:e1000 \\\
  10ec8139:rtl8139 \\\
  1af41000:virtio \\\
  808610d3:e1000e

%if 0%{?fedora}
# Fedora specific roms
%global qemuroms %{qemuroms} \\\
  10222000:pcnet \\\
  10ec8029:ne2k_pci \\\
  80861209:eepro100 \\\
  15ad07b0:vmxnet3
%endif

# We only build the ROMs if on an EFI build host. The resulting
# binary RPM will be noarch, so other archs will still be able
# to use the binary ROMs.
%global buildarches x86_64 aarch64

# debugging firmwares does not go the same way as a normal program.
# moreover, all architectures providing debuginfo for a single noarch
# package is currently clashing in koji, so don't bother.
%global debug_package %{nil}

# Upstream don't do "releases" :-( So we're going to use the date
# as the version, and a GIT hash as the release. Generate new GIT
# snapshots using the folowing commands:
#
# $ hash=`git log -1 --format='%h'`
# $ date=`git log -1 --format='%cd' --date=short | tr -d -`
# $ git archive --prefix ipxe-${date}-git${hash}/ ${hash} | xz -7e > ipxe-${date}-git${hash}.tar.xz
#
# And then change these two:

%global hash de8a0821
%global date 20240119

Name:    ipxe
Version: %{date}
Release: 4.git%{hash}%{?dist}
Summary: A network boot loader

License: BSD-2-Clause AND BSD-3-Clause AND GPL-2.0-only AND (GPL-2.0-only OR MPL-1.1) AND GPL-2.0-or-later AND GPL-2.0-or-later WITH UBDL-exception AND ISC AND MIT
URL:     http://ipxe.org/

Source0: %{name}-%{version}-git%{hash}.tar.xz

# Enable IPv6 for qemu's config
# Sent upstream: http://lists.ipxe.org/pipermail/ipxe-devel/2015-November/004494.html
Patch0001: 0001-build-customize-configuration.patch
Patch0002: 0002-Use-spec-compliant-timeouts.patch
# https://github.com/ipxe/ipxe/issues/1419
Patch0003: gcc15.patch

%ifarch %{buildarches}
BuildRequires: perl-interpreter
BuildRequires: perl-Getopt-Long
%if 0%{?fedora} >= 33 || 0%{?rhel} >= 9
BuildRequires: perl-FindBin
BuildRequires: perl-lib
%endif
%ifarch x86_64
BuildRequires: syslinux
%endif
BuildRequires: mtools
BuildRequires: xorriso
BuildRequires: edk2-tools
BuildRequires: xz-devel
BuildRequires: gcc
BuildRequires: binutils-devel
BuildRequires: make

Obsoletes: gpxe <= 1.0.1
%endif

%ifarch x86_64
%package bootimgs-x86
Summary: X86 Network boot loader images in bootable USB, CD, floppy and GRUB formats
BuildArch: noarch
Provides: %{name}-bootimgs = %{version}-%{release}
Obsoletes: %{name}-bootimgs < 20200823-9.git4bd064de
Obsoletes: gpxe-bootimgs <= 1.0.1

%package roms
Summary: Network boot loader roms in .rom format
Requires: %{name}-roms-qemu = %{version}-%{release}
BuildArch: noarch
Obsoletes: gpxe-roms <= 1.0.1

%package roms-qemu
Summary: Network boot loader roms supported by QEMU, .rom format
BuildArch: noarch
Obsoletes: gpxe-roms-qemu <= 1.0.1

%description bootimgs-x86
iPXE is an open source network bootloader. It provides a direct
replacement for proprietary PXE ROMs, with many extra features such as
DNS, HTTP, iSCSI, etc.

This package contains the iPXE boot images in USB, CD, floppy, and PXE
UNDI formats.

%description roms
iPXE is an open source network bootloader. It provides a direct
replacement for proprietary PXE ROMs, with many extra features such as
DNS, HTTP, iSCSI, etc.

This package contains the iPXE roms in .rom format.


%description roms-qemu
iPXE is an open source network bootloader. It provides a direct
replacement for proprietary PXE ROMs, with many extra features such as
DNS, HTTP, iSCSI, etc.

This package contains the iPXE ROMs for devices emulated by QEMU, in
.rom format.
%endif

%ifarch aarch64
%package bootimgs-aarch64
Summary: ARM Network boot loader images in bootable USB and GRUB formats
BuildArch: noarch

%description bootimgs-aarch64
iPXE is an open source network bootloader. It provides a direct
replacement for proprietary PXE ROMs, with many extra features such as
DNS, HTTP, iSCSI, etc.

This package contains the iPXE ARM boot images in USB and GRUB formats.
%endif

%description
iPXE is an open source network bootloader. It provides a direct
replacement for proprietary PXE ROMs, with many extra features such as
DNS, HTTP, iSCSI, etc.

%prep
%setup -q -n %{name}-%{version}-git%{hash}
%autopatch -p1
# ath9k drivers are too big for an Option ROM, and ipxe devs say it doesn't
# make sense anyways
# http://lists.ipxe.org/pipermail/ipxe-devel/2012-March/001290.html
rm -rf src/drivers/net/ath/ath9k

%build
cd src

make_ipxe() {
    make %{?_smp_mflags} \
        NO_WERROR=1 V=1 \
        GITVERSION=%{hash} \
        "$@"
}

%ifarch x86_64

make_ipxe bin-i386-efi/ipxe.efi bin-x86_64-efi/ipxe.efi \
    bin-x86_64-efi/snponly.efi

make_ipxe ISOLINUX_BIN=/usr/share/syslinux/isolinux.bin \
    bin/undionly.kpxe bin/ipxe.{dsk,iso,usb,lkrn} \
    allroms

# build roms with efi support for qemu
mkdir bin-combined
for romstr in %{qemuroms}; do
  rom=$(echo "$romstr" | cut -d ":" -f 1)

  make_ipxe CONFIG=qemu bin/${rom}.rom
  make_ipxe CONFIG=qemu bin-x86_64-efi/${rom}.efidrv
  vid="0x${rom%%????}"
  did="0x${rom#????}"
  EfiRom -f "$vid" -i "$did" --pci23 \
         -ec bin-x86_64-efi/${rom}.efidrv \
         -o  bin-combined/${rom}.eficrom
  util/catrom.pl \
      bin/${rom}.rom \
      bin-combined/${rom}.eficrom \
      > bin-combined/${rom}.rom
  EfiRom -d  bin-combined/${rom}.rom
  # truncate to at least 256KiB
  truncate -s \>256K bin-combined/${rom}.rom
  # verify rom fits in 256KiB
  test $(stat -c '%s' bin-combined/${rom}.rom) -le $((256 * 1024))
done

%endif

%ifarch aarch64
make_ipxe bin-arm64-efi/snponly.efi
%if 0%{?fedora}
make_ipxe bin-arm64-efi/ipxe.efi
%endif
%endif

%install
%ifarch x86_64
mkdir -p %{buildroot}/%{_datadir}/%{name}/
mkdir -p %{buildroot}/%{_datadir}/%{name}.efi/
pushd src/bin/

cp -a undionly.kpxe ipxe.{iso,usb,dsk,lkrn} %{buildroot}/%{_datadir}/%{name}/

for img in *.rom; do
  if [ -e $img ]; then
    cp -a $img %{buildroot}/%{_datadir}/%{name}/
    echo %{_datadir}/%{name}/$img >> ../../rom.list
  fi
done
popd

cp -a src/bin-i386-efi/ipxe.efi %{buildroot}/%{_datadir}/%{name}/ipxe-i386.efi
cp -a src/bin-x86_64-efi/ipxe.efi %{buildroot}/%{_datadir}/%{name}/ipxe-x86_64.efi
cp -a src/bin-x86_64-efi/snponly.efi %{buildroot}/%{_datadir}/%{name}/ipxe-snponly-x86_64.efi

mkdir -p %{buildroot}%{_datadir}/%{name}/qemu/

for romstr in %{qemuroms}; do
  # the roms supported by qemu will be packaged separatedly
  # remove from the main rom list and add them to qemu.list
  rom=$(echo "$romstr" | cut -d ":" -f 1)
  qemuname=$(echo "$romstr" | cut -d ":" -f 2)
  sed -i -e "/\/${rom}.rom/d" rom.list
  echo %{_datadir}/%{name}/${rom}.rom >> qemu.rom.list

  cp src/bin-combined/${rom}.rom %{buildroot}/%{_datadir}/%{name}.efi/
  echo %{_datadir}/%{name}.efi/${rom}.rom >> qemu.rom.list

  # Set up symlinks with expected qemu firmware names
  ln -s ../../ipxe/${rom}.rom %{buildroot}%{_datadir}/%{name}/qemu/pxe-${qemuname}.rom
  ln -s ../../ipxe.efi/${rom}.rom %{buildroot}%{_datadir}/%{name}/qemu/efi-${qemuname}.rom
done

# endif x86_64
%endif

%ifarch aarch64
mkdir -p %{buildroot}/%{_datadir}/%{name}/arm64-efi
cp -a src/bin-arm64-efi/snponly.efi %{buildroot}/%{_datadir}/%{name}/arm64-efi/snponly.efi
%if 0%{?fedora}
cp -a src/bin-arm64-efi/ipxe.efi %{buildroot}/%{_datadir}/%{name}/arm64-efi/ipxe.efi
%endif
%endif

%ifarch x86_64
%files bootimgs-x86
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/ipxe.iso
%{_datadir}/%{name}/ipxe.usb
%{_datadir}/%{name}/ipxe.dsk
%{_datadir}/%{name}/ipxe.lkrn
%{_datadir}/%{name}/ipxe-i386.efi
%{_datadir}/%{name}/ipxe-x86_64.efi
%{_datadir}/%{name}/undionly.kpxe
%{_datadir}/%{name}/ipxe-snponly-x86_64.efi
%doc COPYING COPYING.GPLv2 COPYING.UBDL

%files roms -f rom.list
%dir %{_datadir}/%{name}
%doc COPYING COPYING.GPLv2 COPYING.UBDL

%files roms-qemu -f qemu.rom.list
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}.efi
%{_datadir}/%{name}/qemu
%doc COPYING COPYING.GPLv2 COPYING.UBDL
%endif

%ifarch aarch64
%files bootimgs-aarch64
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/arm64-efi
%if 0%{?fedora}
%{_datadir}/%{name}/arm64-efi/ipxe.efi
%endif
%{_datadir}/%{name}/arm64-efi/snponly.efi
%endif

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20240119-4.gitde8a0821
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20240119-3.gitde8a0821
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20240119-2.gitde8a0821
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jan 30 2024 Daniel P. Berrangé <berrange@redhat.com> - 20240119-1.gitde8a0821
- Update to latest git snapshot

* Thu Jan 25 2024 Stid Official <stidofficiel@gmail.com> - 20220210-8.git64113751
- Add support of NFS protocol

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20220210-7.git64113751
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20220210-6.git64113751
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 19 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 20220210-5.git64113751
- Fix build with binutils 2.41

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20220210-4.git64113751
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20220210-3.git64113751
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20220210-2.git64113751
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Apr 10 2022 Cole Robinson <crobinso@redhat.com> - 20220210-1.git64113751
- Update to newer git snapshot

* Tue Mar 01 2022 Yaakov Selkowitz <yselkowi@redhat.com> - 20200823-9.git4bd064de
- Add aarch64 EFI artifacts (bz 2058680)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20200823-8.git4bd064de
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild
