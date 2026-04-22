## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 6;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# https://fedoraproject.org/wiki/Changes/SetBuildFlagsBuildCheck
# breaks cross-building
%undefine _auto_set_build_flags

# actual firmware builds support cross-compiling.  edk2-tools
# in theory should build everywhere without much trouble, but
# in practice the edk2 build system barfs on archs it doesn't know
# (such as ppc), so lets limit things to the known-good ones.
#
# We allow rpm builds on all arches (so the noarch rpms with the
# firmware binaries land in all arch repos).  On unsupported archs
# the 'build' and 'install' phases do nothing though.
#
%define build_arches x86_64 aarch64 riscv64
%ifnarch %{build_arches}
%global debug_package %{nil}
%endif

# edk2-stable202511
%define GITDATE        20251119
%define GITCOMMIT      46548b1adac8
%define TOOLCHAIN      GCC

%define PLATFORMS_COMMIT 1e64c1109ae2

%define OPENSSL_VER    3.5.5

%define DBXDATE        20251016

# Undefine this to get *HUGE* (50MB+) verbose build logs
%define silent --silent

%if %{defined rhel}
%if %{rhel} < 10
  %define rhelcfg rhel-9
  %define RHELCFG RHEL-9
  %define qemuvars 0
%else
  %define rhelcfg rhel-10
  %define RHELCFG RHEL-10
  %define qemuvars 1
%endif
%define build_ovmf 0
%define build_aarch64 0
%ifarch x86_64
  %define build_ovmf 1
%endif
%ifarch aarch64
  %define build_aarch64 1
%endif
%define build_riscv64 0
%define build_loongarch64 0
%else
%define build_ovmf 1
%define build_aarch64 1
%define build_riscv64 1
%define build_loongarch64 1
%define qemuvars 1
%endif

%define cross %{defined fedora}
%define disable_werror %{defined fedora}

%if 0%{?copr_projectname:1}
  %define dist %{buildtag}
%endif

Name:       edk2
Version:    %{GITDATE}
Release:    %autorelease
Summary:    UEFI firmware for 64-bit virtual machines
License:    Apache-2.0 AND (BSD-2-Clause OR GPL-2.0-or-later) AND BSD-2-Clause-Patent AND BSD-3-Clause AND BSD-4-Clause AND ISC AND MIT AND LicenseRef-Fedora-Public-Domain
URL:        http://www.tianocore.org

# The source tarball is created using following commands:
# COMMIT=bb1bba3d7767
# git archive --format=tar --prefix=edk2-$COMMIT/ $COMMIT \
# | xz -9ev >/tmp/edk2-$COMMIT.tar.xz
Source0: edk2-%{GITCOMMIT}.tar.xz
Source1: ovmf-whitepaper-c770f8c.txt
Source2: openssl-%{OPENSSL_VER}.tar.gz
Source4: edk2-platforms-%{PLATFORMS_COMMIT}.tar.xz
Source5: jansson-2.13.1.tar.bz2
Source6: dtc-1.7.0.tar.xz
Source9: README.experimental

# json description files
Source10: 50-edk2-aarch64-qcow2.json
Source11: 51-edk2-aarch64-raw.json
Source12: 52-edk2-aarch64-verbose-qcow2.json
Source13: 53-edk2-aarch64-verbose-raw.json

Source40: 30-edk2-ovmf-4m-qcow2-x64-sb-enrolled.json
Source41: 31-edk2-ovmf-2m-raw-x64-sb-enrolled.json
Source42: 40-edk2-ovmf-4m-qcow2-x64-sb.json
Source43: 41-edk2-ovmf-2m-raw-x64-sb.json
Source44: 50-edk2-ovmf-x64-microvm.json
Source45: 50-edk2-ovmf-4m-qcow2-x64-nosb.json
Source46: 51-edk2-ovmf-2m-raw-x64-nosb.json
Source47: 60-edk2-ovmf-x64-stateless.json
Source48: 61-edk2-ovmf-x64-amdsev.json
Source49: 61-edk2-ovmf-x64-inteltdx.json

Source50: 50-edk2-riscv-qcow2.json

Source60: 50-edk2-loongarch64.json

# https://gitlab.com/kraxel/edk2-build-config
Source80: edk2-build.py
Source81: edk2-build.fedora
Source82: edk2-build.fedora.platforms
Source83: edk2-build.rhel-9
Source84: edk2-build.rhel-10

Source90: DBXUpdate-%{DBXDATE}.x64.bin
Source92: DBXUpdate-%{DBXDATE}.aa64.bin

Patch0001: 0001-BaseTools-do-not-build-BrotliCompress-RH-only.patch
Patch0002: 0002-MdeModulePkg-remove-package-private-Brotli-include-p.patch
Patch0003: 0003-MdeModulePkg-TerminalDxe-set-xterm-resolution-on-mod.patch
Patch0004: 0004-OvmfPkg-take-PcdResizeXterm-from-the-QEMU-command-li.patch
Patch0005: 0005-ArmVirtPkg-take-PcdResizeXterm-from-the-QEMU-command.patch
Patch0006: 0006-OvmfPkg-enable-DEBUG_VERBOSE-RHEL-only.patch
Patch0007: 0007-OvmfPkg-silence-DEBUG_VERBOSE-0x00400000-in-QemuVide.patch
Patch0008: 0008-ArmVirtPkg-silence-DEBUG_VERBOSE-0x00400000-in-QemuR.patch
Patch0009: 0009-OvmfPkg-QemuRamfbDxe-Do-not-report-DXE-failure-on-Aa.patch
Patch0010: 0010-OvmfPkg-silence-EFI_D_VERBOSE-0x00400000-in-NvmExpre.patch
Patch0011: 0011-OvmfPkg-QemuKernelLoaderFsDxe-suppress-error-on-no-k.patch
Patch0012: 0012-SecurityPkg-Tcg2Dxe-suppress-error-on-no-swtpm-in-si.patch
Patch0013: 0013-CryptoPkg-CrtLib-add-stat.h.patch
Patch0014: 0014-CryptoPkg-CrtLib-add-access-open-read-write-close-sy.patch
Patch0015: 0015-OvmfPkg-set-PcdVariableStoreSize-PcdMaxVolatileVaria.patch
%if 0%{?fedora} >= 38 || 0%{?rhel} >= 10
Patch0016: 0016-silence-.-has-a-LOAD-segment-with-RWX-permissions-wa.patch
%endif
Patch0017: 0017-OvmfPkg-X64-add-opt-org.tianocore-UninstallMemAttrPr.patch
Patch0018: 0018-openssl-silence-unused-variable-warning.patch
Patch0019: 0019-OvmfPkg-PlatformDxe-register-page-fault-handler-for-.patch
Patch0020: 0020-OvmfPkg-PlatformDxe-add-check-for-1g-page-support.patch
Patch0021: 0021-UefiCpuPkg-CpuExceptionHandlerLib-fix-push-instructi.patch
Patch0022: 0022-OvmfPkg-PlatformPei-Do-not-enable-S3-support-for-con.patch
Patch0023: 0023-OvmfPkg-MemDebugLogLib-use-AcquireSpinLockOrFail.patch
Patch0024: 0024-BaseTools-EfiRom-fix-compiler-warning.patch


# needed by %prep
BuildRequires:  git

%ifarch %{build_arches}
# python3-devel and libuuid-devel are required for building tools.
# python3-devel is also needed for varstore template generation and
# verification with "ovmf-vars-generator".
BuildRequires:  python3-devel
BuildRequires:  libuuid-devel
BuildRequires:  /usr/bin/iasl
BuildRequires:  binutils gcc gcc-c++ make
BuildRequires:  qemu-img

# openssl configure
BuildRequires:  perl(FindBin)
BuildRequires:  perl(IPC::Cmd)
BuildRequires:  perl(File::Compare)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(JSON)
BuildRequires:  perl(Time::Piece)

%if %{build_ovmf}
# Only OVMF includes 80x86 assembly files (*.nasm*).
BuildRequires:  nasm

# Only OVMF includes the Secure Boot feature, for which we need to separate out
# the UEFI shell.
BuildRequires:  dosfstools
BuildRequires:  mtools
BuildRequires:  xorriso

# For generating the variable store template with the default certificates
# enrolled.
BuildRequires:  python3-virt-firmware >= 24.2

%if %{defined fedora}
# generate igvm files (using igvm-wrap)
%endif

# endif build_ovmf
%endif

%if %{cross}
BuildRequires:  gcc-aarch64-linux-gnu
BuildRequires:  gcc-x86_64-linux-gnu
BuildRequires:  gcc-riscv64-linux-gnu
BuildRequires:  gcc-loongarch64-linux-gnu
%endif

%endif

%description
EDK II is a modern, feature-rich, cross-platform firmware development
environment for the UEFI and PI specifications. This package contains sample
64-bit UEFI firmware builds for QEMU and KVM.


%ifarch %{build_arches}

%package ovmf
Summary:    UEFI firmware for x86_64 virtual machines
BuildArch:  noarch
Provides:   OVMF = %{version}-%{release}
Obsoletes:  OVMF < 20180508-100.gitee3198e672e2.el7
Recommends: edk2-shell-x64

# need libvirt version with qcow2 support
Conflicts:  libvirt-daemon-driver-qemu < 9.7.0

# OVMF includes the Secure Boot and IPv6 features; it has a builtin OpenSSL
# library.
Provides:   bundled(openssl) = %{OPENSSL_VER}
License:    Apache-2.0 AND (BSD-2-Clause OR GPL-2.0-or-later) AND BSD-2-Clause-Patent AND BSD-4-Clause AND ISC AND LicenseRef-Fedora-Public-Domain

# URL taken from the Maintainers.txt file.
URL:        http://www.tianocore.org/ovmf/

%description ovmf
OVMF (Open Virtual Machine Firmware) is a project to enable UEFI support for
Virtual Machines. This package contains a sample 64-bit UEFI firmware for QEMU
and KVM.


%package shell-x64
Summary:        EFI Shell for x64
BuildArch:      noarch

%description shell-x64
EFI Shell for x64


%package aarch64
Summary:    UEFI firmware for aarch64 virtual machines
BuildArch:  noarch
Provides:   AAVMF = %{version}-%{release}
Obsoletes:  AAVMF < 20180508-100.gitee3198e672e2.el7
Recommends: edk2-shell-aa64

# need libvirt version with qcow2 support
Conflicts:  libvirt-daemon-driver-qemu < 9.7.0

# No Secure Boot for AAVMF yet, but we include OpenSSL for the IPv6 stack.
Provides:   bundled(openssl) = %{OPENSSL_VER}
License:    Apache-2.0 AND (BSD-2-Clause OR GPL-2.0-or-later) AND BSD-2-Clause-Patent AND BSD-4-Clause AND ISC AND LicenseRef-Fedora-Public-Domain

# URL taken from the Maintainers.txt file.
URL:        https://github.com/tianocore/tianocore.github.io/wiki/ArmVirtPkg

%description aarch64
AAVMF (ARM Architecture Virtual Machine Firmware) is an EFI Development Kit II
platform that enables UEFI support for QEMU/KVM ARM Virtual Machines. This
package contains a 64-bit build.


%package shell-aa64
Summary:        EFI Shell for aa64
BuildArch:      noarch

%description shell-aa64
EFI Shell for aa64


%package tools
Summary:        EFI Development Kit II Tools
License:        BSD-2-Clause-Patent AND LicenseRef-Fedora-Public-Domain
URL:            https://github.com/tianocore/tianocore.github.io/wiki/BaseTools
%description tools
This package provides tools that are needed to
build EFI executables and ROMs using the GNU tools.

%package tools-doc
Summary:        Documentation for EFI Development Kit II Tools
BuildArch:      noarch
License:        BSD-2-Clause-Patent
URL:            https://github.com/tianocore/tianocore.github.io/wiki/BaseTools
%description tools-doc
This package documents the tools that are needed to
build EFI executables and ROMs using the GNU tools.


%if %{defined fedora}
%package experimental
Summary:        Open Virtual Machine Firmware, experimental builds
License:        Apache-2.0 AND BSD-2-Clause-Patent AND BSD-4-Clause AND ISC AND LicenseRef-Fedora-Public-Domain
Provides:       bundled(openssl)
Obsoletes:      edk2-ovmf-experimental < 20230825
BuildArch:      noarch
%description experimental
EFI Development Kit II
Open Virtual Machine Firmware (experimental builds)

%package riscv64
Summary:        RISC-V Virtual Machine Firmware
BuildArch:      noarch
License:        Apache-2.0 AND (BSD-2-Clause OR GPL-2.0-or-later) AND BSD-2-Clause-Patent AND LicenseRef-Fedora-Public-Domain
Recommends:     shell-riscv64

# need libvirt version with qcow2 support
Conflicts:  libvirt-daemon-driver-qemu < 9.7.0

%description riscv64
EFI Development Kit II
RISC-V UEFI Firmware

%package shell-riscv64
Summary:        EFI Shell for riscv64
BuildArch:      noarch

%description shell-riscv64
EFI Shell for riscv64

%package loongarch64
Summary:        loongarch Virtual Machine Firmware
BuildArch:      noarch
License:        Apache-2.0 AND (BSD-2-Clause OR GPL-2.0-or-later) AND BSD-2-Clause-Patent AND LicenseRef-Fedora-Public-Domain
Recommends:     shell-loongarch64

%description loongarch64
EFI Development Kit II
loongarch UEFI Firmware

%package ext4
Summary:        Ext4 filesystem driver
License:        Apache-2.0 AND BSD-2-Clause-Patent
BuildArch:      noarch
%description ext4
EFI Development Kit II
Ext4 filesystem driver

%package shell-loongarch64
Summary:        EFI Shell for loongarch64
BuildArch:      noarch

%description shell-loongarch64
EFI Shell for loongarch64

%package tools-python
Summary:        EFI Development Kit II Tools
Requires:       python3
BuildArch:      noarch

%description tools-python
This package provides tools that are needed to build EFI executables
and ROMs using the GNU tools.  You do not need to install this package;
you probably want to install edk2-tools only.

# endif fedora
%endif

%endif


%prep
# We needs some special git config options that %%autosetup won't give us.
# We init the git dir ourselves, then tell %%autosetup not to blow it away.
%setup -q -n edk2-%{GITCOMMIT}
tar -xf %{SOURCE4} --strip-components=1 "*/Drivers" "*/Features" "*/Platform" "*/Silicon"
git init -q
git config core.whitespace cr-at-eol
git config am.keepcr true
# -T is passed to %%setup to not re-extract the archive
# -D is passed to %%setup to not delete the existing archive dir
%autosetup -T -D -n edk2-%{GITCOMMIT} -S git_am

cp -a -- %{SOURCE1} .
# extract tarballs into place
tar -xf %{SOURCE2} --strip-components=1 --directory CryptoPkg/Library/OpensslLib/openssl
tar -xf %{SOURCE5} --strip-components=1 --directory RedfishPkg/Library/JsonLib/jansson
tar -xf %{SOURCE6} --strip-components=1 --directory MdePkg/Library/BaseFdtLib/libfdt
# include paths pointing to unused submodules
mkdir -p MdePkg/Library/MipiSysTLib/mipisyst/library/include
mkdir -p CryptoPkg/Library/MbedTlsLib/mbedtls/include
mkdir -p CryptoPkg/Library/MbedTlsLib/mbedtls/include/mbedtls
mkdir -p CryptoPkg/Library/MbedTlsLib/mbedtls/library
mkdir -p SecurityPkg/DeviceSecurity/SpdmLib/libspdm/include

# Done by %%setup, but we do not use it for the auxiliary tarballs
chmod -Rf a+rX,u+w,g-w,o-w .

cp -a -- \
   %{SOURCE9} \
   %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} \
   %{SOURCE40} %{SOURCE41} %{SOURCE42} %{SOURCE43} %{SOURCE44} \
   %{SOURCE45} %{SOURCE46} %{SOURCE47} %{SOURCE48} %{SOURCE49} \
   %{SOURCE50} \
   %{SOURCE60} \
   %{SOURCE80} %{SOURCE81} %{SOURCE82} %{SOURCE83} %{SOURCE84} \
   %{SOURCE90} %{SOURCE92} \
   .

%build
%ifarch %{build_arches}

build_iso() {
  dir="$1"
  UEFI_SHELL_BINARY=${dir}/Shell.efi
  ENROLLER_BINARY=${dir}/EnrollDefaultKeys.efi
  UEFI_SHELL_IMAGE=uefi_shell.img
  ISO_IMAGE=${dir}/UefiShell.iso

  UEFI_SHELL_BINARY_BNAME=$(basename -- "$UEFI_SHELL_BINARY")
  UEFI_SHELL_SIZE=$(stat --format=%s -- "$UEFI_SHELL_BINARY")
  ENROLLER_SIZE=$(stat --format=%s -- "$ENROLLER_BINARY")

  # add 1MB then 10% for metadata
  UEFI_SHELL_IMAGE_KB=$((
    (UEFI_SHELL_SIZE + ENROLLER_SIZE + 1 * 1024 * 1024) * 11 / 10 / 1024
  ))

  # create non-partitioned FAT image
  rm -f -- "$UEFI_SHELL_IMAGE"
  mkdosfs -C "$UEFI_SHELL_IMAGE" -n UEFI_SHELL -- "$UEFI_SHELL_IMAGE_KB"

  # copy the shell binary into the FAT image
  export MTOOLS_SKIP_CHECK=1
  mmd   -i "$UEFI_SHELL_IMAGE"                       ::efi
  mmd   -i "$UEFI_SHELL_IMAGE"                       ::efi/boot
  mcopy -i "$UEFI_SHELL_IMAGE"  "$UEFI_SHELL_BINARY" ::efi/boot/bootx64.efi
  mcopy -i "$UEFI_SHELL_IMAGE"  "$ENROLLER_BINARY"   ::
  mdir  -i "$UEFI_SHELL_IMAGE"  -/                   ::

  # build ISO with FAT image file as El Torito EFI boot image
  mkisofs -input-charset ASCII -J -rational-rock \
    -e "$UEFI_SHELL_IMAGE" -no-emul-boot \
    -o "$ISO_IMAGE" "$UEFI_SHELL_IMAGE"
}

export EXTRA_OPTFLAGS="%{optflags}"
export EXTRA_LDFLAGS="%{__global_ldflags}"
export RELEASE_DATE="$(echo %{GITDATE} | sed -e 's|\(....\)\(..\)\(..\)|\2/\3/\1|')"

touch OvmfPkg/AmdSev/Grub/grub.efi   # dummy
python3 CryptoPkg/Library/OpensslLib/configure.py

%if %{build_ovmf}
%if %{defined rhel}

./edk2-build.py --config edk2-build.%{rhelcfg} %{?silent} --release-date "$RELEASE_DATE" -m ovmf
virt-fw-vars --input   %{RHELCFG}/ovmf/OVMF_VARS.fd \
             --output  %{RHELCFG}/ovmf/OVMF_VARS.secboot.fd \
             --set-dbx DBXUpdate-%{DBXDATE}.x64.bin \
             --enroll-redhat --secure-boot
virt-fw-vars --input   %{RHELCFG}/ovmf/OVMF.inteltdx.fd \
             --output  %{RHELCFG}/ovmf/OVMF.inteltdx.secboot.fd \
             --set-dbx DBXUpdate-%{DBXDATE}.x64.bin \
             --enroll-redhat --secure-boot
build_iso %{RHELCFG}/ovmf
cp DBXUpdate-%{DBXDATE}.x64.bin %{RHELCFG}/ovmf

%else

./edk2-build.py --config edk2-build.fedora %{?silent} --release-date "$RELEASE_DATE" -m ovmf
./edk2-build.py --config edk2-build.fedora.platforms %{?silent} -m x64
virt-fw-vars --input   Fedora/ovmf/OVMF_VARS.fd \
             --output  Fedora/ovmf/OVMF_VARS.secboot.fd \
             --set-dbx DBXUpdate-%{DBXDATE}.x64.bin \
             --enroll-redhat --secure-boot
virt-fw-vars --input   Fedora/ovmf/OVMF_VARS_4M.fd \
             --output  Fedora/ovmf/OVMF_VARS_4M.secboot.fd \
             --set-dbx DBXUpdate-%{DBXDATE}.x64.bin \
             --enroll-redhat --secure-boot
virt-fw-vars --input   Fedora/ovmf/OVMF.inteltdx.fd \
             --output  Fedora/ovmf/OVMF.inteltdx.secboot.fd \
             --set-dbx DBXUpdate-%{DBXDATE}.x64.bin \
             --enroll-redhat --secure-boot
build_iso Fedora/ovmf
cp DBXUpdate-%{DBXDATE}.x64.bin Fedora/ovmf

: igvm-wrap --input Fedora/ovmf/OVMF_CODE_4M.fd \
          --vars Fedora/ovmf/OVMF_VARS_4M.fd \
          --output Fedora/ovmf/OVMF.igvm \
          --meta --inspect --snp

for raw in */ovmf/*_4M*.fd; do
    qcow2="${raw%.fd}.qcow2"
    qemu-img convert -f raw -O qcow2 -o cluster_size=4096 -S 4096 "$raw" "$qcow2"
    rm -f "$raw"
done

# stateless builds
virt-fw-vars --input   Fedora/ovmf/OVMF.stateless.fd \
             --output  Fedora/ovmf/OVMF.stateless.secboot.fd \
             --set-dbx DBXUpdate-%{DBXDATE}.x64.bin \
             --enroll-redhat --secure-boot \
             --set-fallback-no-reboot

for image in \
	Fedora/ovmf/OVMF_CODE.secboot.fd \
	Fedora/ovmf/OVMF_CODE_4M.secboot.qcow2 \
	Fedora/ovmf/OVMF.stateless.secboot.fd \
; do
	pcr="${image}"
	pcr="${pcr%.fd}"
	pcr="${pcr%.qcow2}"
	pcr="${pcr}.pcrlock"
	python3 /usr/share/doc/python3-virt-firmware/experimental/measure.py \
		--image "$image" \
		--version "%{name}-%{version}-%{release}" \
                --no-shim --pcrlock \
                --bank sha256 --bank sha384 \
		> "$pcr"
done

%endif
%endif

%if %{build_aarch64}
%if %{defined rhel}
./edk2-build.py --config edk2-build.%{rhelcfg} %{?silent} --release-date "$RELEASE_DATE" -m armvirt
cp DBXUpdate-%{DBXDATE}.aa64.bin %{RHELCFG}/aarch64
%else
./edk2-build.py --config edk2-build.fedora %{?silent} --release-date "$RELEASE_DATE" -m armvirt
./edk2-build.py --config edk2-build.fedora.platforms %{?silent} -m aa64
virt-fw-vars --input   Fedora/aarch64/vars-template-pflash.raw \
             --output  Fedora/experimental/vars-template-secboot-testonly-pflash.raw \
             --set-dbx DBXUpdate-%{DBXDATE}.aa64.bin \
             --enroll-redhat --secure-boot --distro-keys rhel
cp DBXUpdate-%{DBXDATE}.aa64.bin Fedora/aarch64
%endif
for raw in */aarch64/*.raw; do
    qcow2="${raw%.raw}.qcow2"
    qemu-img convert -f raw -O qcow2 -o cluster_size=4096 -S 4096 "$raw" "$qcow2"
done
%endif

%if %{build_riscv64}
./edk2-build.py --config edk2-build.fedora %{?silent} --release-date "$RELEASE_DATE" -m riscv
./edk2-build.py --config edk2-build.fedora.platforms %{?silent} -m riscv
for raw in */riscv/*.raw; do
    qcow2="${raw%.raw}.qcow2"
    qemu-img convert -f raw -O qcow2 -o cluster_size=4096 -S 4096 "$raw" "$qcow2"
    rm -f "$raw"
done
%endif

%if %{build_loongarch64}
./edk2-build.py --config edk2-build.fedora %{?silent} -m loongarch
find Build -name *.fd
%endif
%endif

%install
%ifarch %{build_arches}

cp -a OvmfPkg/License.txt License.OvmfPkg.txt
cp -a CryptoPkg/Library/OpensslLib/openssl/LICENSE.txt LICENSE.openssl
mkdir -p %{buildroot}%{_datadir}/qemu/firmware

# install the tools
mkdir -p %{buildroot}%{_bindir} \
         %{buildroot}%{_datadir}/%{name}/Conf \
         %{buildroot}%{_datadir}/%{name}/Scripts
install BaseTools/Source/C/bin/* \
        %{buildroot}%{_bindir}
install BaseTools/BinWrappers/PosixLike/LzmaF86Compress \
        %{buildroot}%{_bindir}
install BaseTools/BuildEnv \
        %{buildroot}%{_datadir}/%{name}
install BaseTools/Conf/*.template \
        %{buildroot}%{_datadir}/%{name}/Conf
install BaseTools/Scripts/GccBase.lds \
        %{buildroot}%{_datadir}/%{name}/Scripts

# install firmware images
mkdir -p %{buildroot}%{_datadir}/%{name}
%if %{defined rhel}
cp -av %{RHELCFG}/* %{buildroot}%{_datadir}/%{name}
%else
cp -av Fedora/* %{buildroot}%{_datadir}/%{name}
%endif


%if %{build_ovmf}

# compat symlinks
mkdir -p %{buildroot}%{_datadir}/OVMF
ln -s ../%{name}/ovmf/OVMF_CODE.fd         %{buildroot}%{_datadir}/OVMF/
ln -s ../%{name}/ovmf/OVMF_CODE.secboot.fd %{buildroot}%{_datadir}/OVMF/
ln -s ../%{name}/ovmf/OVMF_VARS.fd         %{buildroot}%{_datadir}/OVMF/
ln -s ../%{name}/ovmf/OVMF_VARS.secboot.fd %{buildroot}%{_datadir}/OVMF/
ln -s ../%{name}/ovmf/UefiShell.iso        %{buildroot}%{_datadir}/OVMF/
ln -s OVMF_CODE.fd %{buildroot}%{_datadir}/%{name}/ovmf/OVMF_CODE.cc.fd

# json description files
mkdir -p %{buildroot}%{_datadir}/qemu/firmware
install -m 0644 \
        30-edk2-ovmf-4m-qcow2-x64-sb-enrolled.json \
        31-edk2-ovmf-2m-raw-x64-sb-enrolled.json \
        40-edk2-ovmf-4m-qcow2-x64-sb.json \
        41-edk2-ovmf-2m-raw-x64-sb.json \
        50-edk2-ovmf-4m-qcow2-x64-nosb.json \
        51-edk2-ovmf-2m-raw-x64-nosb.json \
        61-edk2-ovmf-x64-amdsev.json \
        61-edk2-ovmf-x64-inteltdx.json \
        %{buildroot}%{_datadir}/qemu/firmware
%if %{defined fedora}
install -m 0644 \
        50-edk2-ovmf-x64-microvm.json \
        60-edk2-ovmf-x64-stateless.json \
        %{buildroot}%{_datadir}/qemu/firmware
%endif

# endif build_ovmf
%endif

%if %{build_aarch64}

# compat symlinks
mkdir -p %{buildroot}%{_datadir}/AAVMF
ln -s ../%{name}/aarch64/QEMU_EFI-pflash.raw \
  %{buildroot}%{_datadir}/AAVMF/AAVMF_CODE.verbose.fd
ln -s ../%{name}/aarch64/QEMU_EFI-silent-pflash.raw \
  %{buildroot}%{_datadir}/AAVMF/AAVMF_CODE.fd
ln -s ../%{name}/aarch64/vars-template-pflash.raw \
  %{buildroot}%{_datadir}/AAVMF/AAVMF_VARS.fd

# json description files
install -m 0644 \
        50-edk2-aarch64-qcow2.json \
        51-edk2-aarch64-raw.json \
        52-edk2-aarch64-verbose-qcow2.json \
        53-edk2-aarch64-verbose-raw.json \
        %{buildroot}%{_datadir}/qemu/firmware

# endif build_aarch64
%endif

%if %{build_riscv64}

install -m 0644 \
        50-edk2-riscv-qcow2.json \
        %{buildroot}%{_datadir}/qemu/firmware

# endif build_riscv64
%endif

%if %{build_loongarch64}

install -m 0644 \
        50-edk2-loongarch64.json \
        %{buildroot}%{_datadir}/qemu/firmware

# endif build_loongarch64
%endif

%if %{defined fedora}

# edk2-tools-python install
cp -R BaseTools/Source/Python %{buildroot}%{_datadir}/%{name}/Python
for i in build BPDG Ecc GenDepex GenFds GenPatchPcdTable PatchPcdValue TargetTool Trim UPT; do
echo '#!/bin/sh
export PYTHONPATH=%{_datadir}/%{name}/Python
exec python3 '%{_datadir}/%{name}/Python/$i/$i.py' "$@"' > %{buildroot}%{_bindir}/$i
  chmod +x %{buildroot}%{_bindir}/$i
done

%if 0%{?py_byte_compile:1}
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python_Appendix/#manual-bytecompilation
%py_byte_compile %{python3} %{buildroot}%{_datadir}/edk2/Python
%endif

%endif
%endif

%check
%ifarch %{build_arches}
for file in %{buildroot}%{_datadir}/%{name}/*/*VARS.secboot.fd; do
    test -f "$file" || continue
    virt-fw-vars --input $file --print | grep "SecureBootEnable.*ON" || exit 1
done
%endif

%global common_files \
  %%license License.txt License.OvmfPkg.txt License-History.txt LICENSE.openssl \
  %%dir %%{_datadir}/%%{name}/ \
  %%dir %%{_datadir}/qemu \
  %%dir %%{_datadir}/qemu/firmware

%ifarch %{build_arches}
%if %{build_ovmf}
%files ovmf
%common_files
%doc OvmfPkg/README
%doc ovmf-whitepaper-c770f8c.txt
%dir %{_datadir}/OVMF/
%{_datadir}/OVMF/OVMF_CODE.fd
%{_datadir}/OVMF/OVMF_CODE.secboot.fd
%{_datadir}/OVMF/OVMF_VARS.fd
%{_datadir}/OVMF/OVMF_VARS.secboot.fd
%{_datadir}/OVMF/UefiShell.iso
%dir %{_datadir}/%{name}/ovmf/
%{_datadir}/%{name}/ovmf/OVMF_CODE.fd
%{_datadir}/%{name}/ovmf/OVMF_CODE.cc.fd
%{_datadir}/%{name}/ovmf/OVMF_CODE.secboot.fd
%{_datadir}/%{name}/ovmf/OVMF_VARS.fd
%{_datadir}/%{name}/ovmf/OVMF_VARS.secboot.fd
%{_datadir}/%{name}/ovmf/OVMF.amdsev.fd
%{_datadir}/%{name}/ovmf/OVMF.inteltdx.fd
%{_datadir}/%{name}/ovmf/OVMF.inteltdx.secboot.fd
%{_datadir}/%{name}/ovmf/UefiShell.iso
%{_datadir}/%{name}/ovmf/EnrollDefaultKeys.efi
%{_datadir}/%{name}/ovmf/DBXUpdate*.bin
%{_datadir}/qemu/firmware/30-edk2-ovmf-4m-qcow2-x64-sb-enrolled.json
%{_datadir}/qemu/firmware/31-edk2-ovmf-2m-raw-x64-sb-enrolled.json
%{_datadir}/qemu/firmware/40-edk2-ovmf-4m-qcow2-x64-sb.json
%{_datadir}/qemu/firmware/41-edk2-ovmf-2m-raw-x64-sb.json
%{_datadir}/qemu/firmware/50-edk2-ovmf-4m-qcow2-x64-nosb.json
%{_datadir}/qemu/firmware/51-edk2-ovmf-2m-raw-x64-nosb.json
%{_datadir}/qemu/firmware/61-edk2-ovmf-x64-amdsev.json
%{_datadir}/qemu/firmware/61-edk2-ovmf-x64-inteltdx.json
%if %{qemuvars}
%{_datadir}/%{name}/ovmf/OVMF.qemuvars.fd
%endif
%if %{defined fedora}
%{_datadir}/%{name}/ovmf/MICROVM.fd
# %{_datadir}/%{name}/ovmf/OVMF.igvm — disabled, no virt-firmware-rs
%{_datadir}/%{name}/ovmf/OVMF.stateless.fd
%{_datadir}/%{name}/ovmf/OVMF.stateless.secboot.fd
%{_datadir}/qemu/firmware/50-edk2-ovmf-x64-microvm.json
%{_datadir}/qemu/firmware/60-edk2-ovmf-x64-stateless.json
%{_datadir}/%{name}/ovmf/OVMF_CODE_4M.qcow2
%{_datadir}/%{name}/ovmf/OVMF_CODE_4M.secboot.qcow2
%{_datadir}/%{name}/ovmf/OVMF_VARS_4M.qcow2
%{_datadir}/%{name}/ovmf/OVMF_VARS_4M.secboot.qcow2
%{_datadir}/%{name}/ovmf/*.pcrlock
%endif
%files shell-x64
%{_datadir}/%{name}/ovmf/Shell.efi
# endif build_ovmf
%endif

%if %{build_aarch64}
%files aarch64
%common_files
%dir %{_datadir}/AAVMF/
%{_datadir}/AAVMF/AAVMF_CODE.verbose.fd
%{_datadir}/AAVMF/AAVMF_CODE.fd
%{_datadir}/AAVMF/AAVMF_VARS.fd
%dir %{_datadir}/%{name}/aarch64/
%{_datadir}/%{name}/aarch64/QEMU_EFI-pflash.*
%{_datadir}/%{name}/aarch64/QEMU_EFI-silent-pflash.*
%{_datadir}/%{name}/aarch64/vars-template-pflash.*
%{_datadir}/%{name}/aarch64/QEMU_EFI.fd
%{_datadir}/%{name}/aarch64/QEMU_EFI.silent.fd
%{_datadir}/%{name}/aarch64/QEMU_VARS.fd
%{_datadir}/%{name}/aarch64/DBXUpdate*.bin
%if %{qemuvars}
%{_datadir}/%{name}/aarch64/QEMU_EFI-qemuvars-pflash.*
%{_datadir}/%{name}/aarch64/QEMU_EFI.qemuvars.fd
%endif
%if %{defined fedora}
%{_datadir}/%{name}/aarch64/QEMU_EFI.kernel.fd
%endif
%{_datadir}/qemu/firmware/50-edk2-aarch64-qcow2.json
%{_datadir}/qemu/firmware/51-edk2-aarch64-raw.json
%{_datadir}/qemu/firmware/52-edk2-aarch64-verbose-qcow2.json
%{_datadir}/qemu/firmware/53-edk2-aarch64-verbose-raw.json
%files shell-aa64
%{_datadir}/%{name}/aarch64/Shell.efi
# endif build_aarch64
%endif

%files tools
%license License.txt
%license License-History.txt
%{_bindir}/DevicePath
%{_bindir}/EfiRom
%{_bindir}/GenCrc32
%{_bindir}/GenFfs
%{_bindir}/GenFv
%{_bindir}/GenFw
%{_bindir}/GenSec
%{_bindir}/LzmaCompress
%{_bindir}/LzmaF86Compress
%{_bindir}/TianoCompress
%{_bindir}/VfrCompile
%{_bindir}/VolInfo
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/BuildEnv
%{_datadir}/%{name}/Conf
%{_datadir}/%{name}/Scripts

%files tools-doc
%doc BaseTools/UserManuals/*.rtf


%if %{defined fedora}
%if %{build_ovmf}
%files experimental
%common_files
%doc README.experimental
%dir %{_datadir}/%{name}/experimental
%{_datadir}/%{name}/experimental/*.fd
%if %{build_aarch64}
%{_datadir}/%{name}/experimental/*.raw
%endif

%files riscv64
%common_files
%dir %{_datadir}/%{name}/riscv
%{_datadir}/%{name}/riscv/*.fd
%{_datadir}/%{name}/riscv/*.qcow2
%{_datadir}/qemu/firmware/50-edk2-riscv-qcow2.json
%endif

%files shell-riscv64
%{_datadir}/%{name}/riscv/Shell.efi

%if %{build_loongarch64}
%files loongarch64
%common_files
%dir %{_datadir}/%{name}/loongarch64
%{_datadir}/%{name}/loongarch64/*.fd
%{_datadir}/qemu/firmware/50-edk2-loongarch64.json
%endif

%files shell-loongarch64
%{_datadir}/%{name}/loongarch64/Shell.efi

%files ext4
%common_files
%dir %{_datadir}/%{name}/drivers
%{_datadir}/%{name}/drivers/ext4*.efi


%files tools-python
%{_bindir}/build
%{_bindir}/BPDG
%{_bindir}/Ecc
%{_bindir}/GenDepex
%{_bindir}/GenFds
%{_bindir}/GenPatchPcdTable
%{_bindir}/PatchPcdValue
%{_bindir}/TargetTool
%{_bindir}/Trim
%{_bindir}/UPT
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/Python

# endif fedora
%endif
%endif


%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 20251119-6
- Latest state for edk2

* Tue Feb 03 2026 Gerd Hoffmann <kraxel@redhat.com> - 20251119-5
- add build dep for openssl Configure perl script

* Tue Feb 03 2026 Gerd Hoffmann <kraxel@redhat.com> - 20251119-4
- switch to vanilla upstream openssl tarballs, update to openssl-3.3.5

* Mon Dec 08 2025 Gerd Hoffmann <kraxel@redhat.com> - 20251119-3
- BaseTools/EfiRom: fix compiler warning

* Thu Dec 04 2025 Gerd Hoffmann <kraxel@redhat.com> - 20251119-2
- OvmfPkg/MemDebugLogLib: use AcquireSpinLockOrFail

* Fri Nov 21 2025 Gerd Hoffmann <kraxel@redhat.com> - 20251119-1
- update to edk2-stable202511

* Mon Nov 03 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250812-24
- add nasm 3.0 build fix

* Mon Nov 03 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250812-23
- update dbx to 20251016 (v1.6.1)

* Mon Nov 03 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250812-22
- dbxupdate: add version tag info

* Thu Oct 16 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250812-21
- backjport iommu fix

* Wed Oct 15 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250812-20
- backport terminal fix

* Tue Oct 14 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250812-19
- switch to standalone efi shell builds

* Mon Oct 06 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250812-18
- add check for 1g page support

* Thu Oct 02 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250812-17
- move build.ovmf.sb.stateless block in edk2-build.fedora

* Tue Sep 30 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250812-16
- json: switch amdsev build to memory

* Tue Sep 30 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250812-15
- move stateless bits to %%fedora sections

* Tue Sep 30 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250812-14
- json: add stateless file, update amdsev + inteltdx files

* Tue Sep 30 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250812-13
- Revert "separate json file for amd-sev"

* Tue Sep 30 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250812-12
- promote stateless ovmf out of experimental

* Tue Sep 30 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250812-11
- Revert "comment out PcdNullPointerDetectionPropertyMask (breaks SEV)"

* Tue Sep 30 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250812-10
- backport sev fixes

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 20250812-9
- Rebuilt for Python 3.14.0rc3 bytecode

* Mon Sep 15 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250812-8
- add fix for aarch64 +tpm2 crash

* Fri Sep 12 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250812-7
- comment out PcdNullPointerDetectionPropertyMask (breaks SEV)

* Wed Sep 10 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250812-6
- drop ia32 support

* Wed Sep 10 2025 Andrea Bolognani <abologna@redhat.com> - 20250812-5
- Add tags to loongarch64 descriptor

* Wed Sep 10 2025 Andrea Bolognani <abologna@redhat.com> - 20250812-4
- Fix horizontal whitespace

* Wed Sep 10 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250812-3
- update page fault handler patch

* Wed Sep 10 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250812-2
- enable DEBUG_TO_MEM

* Wed Sep 10 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250812-1
- update to edk2-stable202508 release

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 20250523-18
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Aug 06 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250523-17
- add vars template to ovmf igvm

* Tue Aug 05 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250523-16
- separate json file for amd-sev

* Mon Aug 04 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250523-15
- add ovmf igvm file

* Mon Aug 04 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250523-14
- move efi shell to new sub-rpms

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20250523-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 17 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250523-12
- copy shell for all archs, add aarch64 dbxupdate

* Wed Jul 09 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250523-11
- add patch: load PlatformDxe in inteltdx build

* Tue Jul 08 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250523-10
- switch non-flash builds to 4M

* Thu Jul 03 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250523-9
- update page fault handler patch

* Mon Jun 23 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250523-8
- add page fault handler patch to fixup + report NX faults

* Mon Jun 23 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250523-7
- turn on EFI_MEMORY_ATTRIBUTE_PROTOCOL in secure boot builds

* Fri Jun 13 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250523-6
- update dbx to 20250610

* Fri Jun 13 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250523-5
- add make-dbxupdate.sh script

* Fri Jun 13 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250523-4
- remove old dbx update files

* Fri Jun 13 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250523-3
- update openssl to version 3.5

* Fri Jun 13 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250523-2
- add qemuvars builds

* Fri Jun 13 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250523-1
- update to edk2-stable2025005 tag

* Tue Mar 11 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250221-8
- fix typo in fwcfg file name

* Mon Mar 10 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250221-7
- add aa64 dbx to src rpm

* Mon Mar 10 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250221-6
- update dbx revocations to 20250224

* Mon Mar 03 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250221-5
- update README.experimental

* Mon Mar 03 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250221-4
- add runtime switch for EFI_MEMORY_ATTRIBUTE_PROTOCOL

* Mon Mar 03 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250221-3
- revert openssl 3.2 adaptions

* Mon Mar 03 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250221-2
- revert openssl 3.4 adaptions

* Mon Mar 03 2025 Gerd Hoffmann <kraxel@redhat.com> - 20250221-1
- [specfile,tarballs,patches] rebase to edk2-stable202502

* Fri Feb 07 2025 Gerd Hoffmann <kraxel@redhat.com> - 20241117-14
- drop downstream patches, add upstream backports

* Fri Feb 07 2025 Gerd Hoffmann <kraxel@redhat.com> - 20241117-13
- split and update rhel9/10 build config

* Fri Feb 07 2025 Gerd Hoffmann <kraxel@redhat.com> - 20241117-12
- drop x64 strictnx build

* Fri Feb 07 2025 Gerd Hoffmann <kraxel@redhat.com> - 20241117-11
- https://fedoraproject.org/wiki/Changes/Edk2Security
- use strictnx config for secure boot builds.
- enable null ptr detection for secure boot builds.

* Mon Jan 20 2025 Gerd Hoffmann <kraxel@redhat.com> - 20241117-10
- minor build script update

* Mon Jan 20 2025 Gerd Hoffmann <kraxel@redhat.com> - 20241117-9
- gcc-15 fixes

* Mon Jan 20 2025 Gerd Hoffmann <kraxel@redhat.com> - 20241117-8
- openssl update

* Mon Jan 20 2025 Gerd Hoffmann <kraxel@redhat.com> - 20241117-7
- add copr build id to release

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20241117-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Nov 27 2024 Gerd Hoffmann <kraxel@redhat.com> - 20241117-5
- xen boot fix

* Wed Nov 27 2024 Gerd Hoffmann <kraxel@redhat.com> - 20241117-4
- enable 5-level paging support

* Wed Nov 27 2024 Gerd Hoffmann <kraxel@redhat.com> - 20241117-3
- drop aarch64 standalone mm image

* Wed Nov 27 2024 Gerd Hoffmann <kraxel@redhat.com> - 20241117-2
- drop 32-bit arm images

* Wed Nov 27 2024 Gerd Hoffmann <kraxel@redhat.com> - 20241117-1
- edk2-stable202411: update tarballs and patches

* Wed Nov 27 2024 Gerd Hoffmann <kraxel@redhat.com> - 20240813-4
- Revert "add openssl fix for CVE-2023-6237"

* Wed Nov 27 2024 Gerd Hoffmann <kraxel@redhat.com> - 20240813-3
- update openssl tarball (to a version including the CVE-2023-6237 fix)

* Fri Oct 11 2024 Paolo Bonzini <pbonzini@redhat.com> - 20240813-2
- add openssl fix for CVE-2023-6237

* Tue Sep 03 2024 Gerd Hoffmann <kraxel@redhat.com> - 20240813-1
- update to edk2-stable202408
- update edk2 and edk2-platform tarballs
- refresh some patches, remove patches merged upstream
- add libfdt tarball (new git submodule in edk2).
- add fix for edk2-platform build
- loongarch moved from edk2-platform to edk2 repo

* Fri Aug 23 2024 Gerd Hoffmann <kraxel@redhat.com> - 20240524-7
- add riscv and loongarch64 directories to file list (rhbz#2302700)

* Fri Aug 23 2024 Gerd Hoffmann <kraxel@redhat.com> - 20240524-6
- allow (dummy) rpm builds on ppc and s390 so the noarch rpms land in the
  ppc/s390 repos

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20240524-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 01 2024 Gerd Hoffmann <kraxel@redhat.com> - 20240524-4
- add 0019-NetworkPkg-DxeNetLib-adjust-PseudoRandom-error-loggi.patch

* Wed Jun 05 2024 Gerd Hoffmann <kraxel@redhat.com> - 20240524-3
- add 0018-NetworkPkg-TcpDxe-Fixed-system-stuck-on-PXE-boot-flo.patch

* Fri May 31 2024 Michal Domonkos <mdomonko@redhat.com> - 20240524-2
- Fix improperly commented out macros in %%%%prep

* Mon May 27 2024 Gerd Hoffmann <kraxel@redhat.com> - 20240524-1
- update to 2024-05 stable tag

* Mon Mar 25 2024 Gerd Hoffmann <kraxel@redhat.com> - 20240214-8
- add a bunch of '%%if %%{build_*}' so partial builds actually work

* Thu Mar 21 2024 Gerd Hoffmann <kraxel@redhat.com> - 20240214-7
- loongarch64: update edk2-platforms tarball, add json firmware description

* Thu Mar 21 2024 Gerd Hoffmann <kraxel@redhat.com> - 20240214-6
- add loongarch64 sub-package

* Thu Mar 21 2024 Gerd Hoffmann <kraxel@redhat.com> - 20240214-5
- loongarch build config update

* Thu Mar 21 2024 Gerd Hoffmann <kraxel@redhat.com> - 20240214-4
- update build config

* Thu Mar 21 2024 Gerd Hoffmann <kraxel@redhat.com> - 20240214-3
- update build script

* Mon Feb 26 2024 Gerd Hoffmann <kraxel@redhat.com> - 20240214-2
- switch pcr predition to systemd-pcrlock format

* Mon Feb 26 2024 Gerd Hoffmann <kraxel@redhat.com> - 20240214-1
- update to edk2-stable202402

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20231122-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20231122-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 22 2023 Gerd Hoffmann <kraxel@redhat.com> - 20231122-14
- set PcdSetNxForStack = TRUE for strict nx builds

* Fri Dec 22 2023 Gerd Hoffmann <kraxel@redhat.com> - 20231122-13
- set PcdImageProtectionPolicy = 0x03 for strict nx builds

* Wed Dec 13 2023 Gerd Hoffmann <kraxel@redhat.com> - 20231122-12
- switch the strictnx build to qcow2 (like all other 4M builds)

* Tue Dec 12 2023 Gerd Hoffmann <kraxel@redhat.com> - 20231122-11
- add PcdUninstallMemAttrProtocol configuration

* Tue Dec 12 2023 Gerd Hoffmann <kraxel@redhat.com> - 20231122-10
- swap MemoryAttributeProtocol patch, again

* Wed Dec 06 2023 Gerd Hoffmann <kraxel@redhat.com> - 20231122-8
- update bundled openssl

* Wed Dec 06 2023 Gerd Hoffmann <kraxel@redhat.com> - 20231122-7
- swap MemoryAttributeProtocol patch

* Wed Dec 06 2023 Gerd Hoffmann <kraxel@redhat.com> - 20231122-6
- fix intel tdx firmware descriptor

* Tue Dec 05 2023 Gerd Hoffmann <kraxel@redhat.com> - 20231122-5
- update build config: 64bit pei, tdx sb

* Tue Dec 05 2023 Gerd Hoffmann <kraxel@redhat.com> - 20231122-4
- update build script

* Mon Nov 27 2023 Gerd Hoffmann <kraxel@redhat.com> - 20231122-3
- silence '... has a LOAD segment with RWX permissions' warning

* Mon Nov 27 2023 Gerd Hoffmann <kraxel@redhat.com> - 20231122-2
- enroll sb keys for tdx image

* Mon Nov 27 2023 Gerd Hoffmann <kraxel@redhat.com> - 20231122-1
- rebase to edk2-stable202311

* Fri Nov 17 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230825-26
- add unversioned virt machine type for riscv64

* Wed Oct 11 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230825-25
- update debug patch, add proper fix for bz2241388

* Tue Oct 10 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230825-24
- test patch for bz2241388

* Wed Sep 27 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230825-23
- add dbxupdate to rpms

* Mon Sep 25 2023 Daniel P. Berrangé <berrange@redhat.com> - 20230825-22
- Add BSD-3-Clause for arm firmware

* Mon Sep 25 2023 Daniel P. Berrangé <berrange@redhat.com> - 20230825-21
- Add BSD-2-Clause OR GPL-2.0-or-later license

* Mon Sep 25 2023 Daniel P. Berrangé <berrange@redhat.com> - 20230825-20
- Add BSD-4-Clause and ISC licenses for arm/x86

* Mon Sep 25 2023 Daniel P. Berrangé <berrange@redhat.com> - 20230825-19
- Add public domain license for Lzma code

* Mon Sep 25 2023 Daniel P. Berrangé <berrange@redhat.com> - 20230825-18
- Alphabetize the SPDX license terms

* Mon Sep 25 2023 Daniel P. Berrangé <berrange@redhat.com> - 20230825-17
- make it simpler to disable silent builds

* Mon Sep 25 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230825-16
- fix 2M secure boot build

* Sun Sep 24 2023 Miroslav Suchý <msuchy@redhat.com> - 20230825-15
- Correct SPDX license formula

* Thu Sep 21 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230825-14
- upgrade libvirt requirement to 9.7.0 or newer, add more subpackages

* Tue Sep 19 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230825-13
- add riscv64 to ExclusiveArch

* Tue Sep 19 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230825-12
- cherry-pick edk2 bugfixes

* Tue Sep 19 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230825-11
- add README.experimental

* Tue Sep 19 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230825-10
- rename subpackage ovmf-experimental to experimental

* Tue Sep 19 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230825-9
- stateless: add --set-fallback-no-reboot

* Tue Sep 19 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230825-8
- add experimental + testonly secure boot build for armvirt

* Tue Sep 19 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230825-7
- update edk2 build script

* Tue Sep 19 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230825-6
- add buildrequires: perl modules for openssl configure

* Tue Sep 19 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230825-5
- openssl licence update (3.0.x uses apache 2.0).

* Tue Sep 19 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230825-4
- add riscv firmware json file

* Tue Sep 19 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230825-3
- split code/vars builds for riscv

* Tue Sep 19 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230825-2
- disable TLS for 2M builds b/c of running out of space.

* Tue Sep 19 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230825-1
- rebase to edk2-stable202308, update patches and openssl tarball

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20230524-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 22 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230524-3
- disable EFI_MEMORY_ATTRIBUTE_PROTO (workaround shim bug)

* Mon Jun 19 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230524-2
- cherry-pick some fixes

* Wed May 31 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230524-1
- drop commit hash from version

* Wed May 31 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230524gitba91d0292e59-1
- update to edk2-stable202305

* Wed May 17 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230301gitf80f052277c8-31
- drop /ovmf-4m/, move 4M builds to /ovmf/ instead

* Wed May 17 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230301gitf80f052277c8-30
- update build script

* Tue May 16 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230301gitf80f052277c8-29
- json descriptors: explicitly set mode = split

* Fri May 12 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230301gitf80f052277c8-28
- switch DBXDATE to 20230509

* Fri May 12 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230301gitf80f052277c8-27
- add 20230509 dbx update files

* Fri May 12 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230301gitf80f052277c8-26
- add json descriptor files for qcow2 images

* Fri May 12 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230301gitf80f052277c8-25
- drop ovmf 4m raw images

* Fri May 12 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230301gitf80f052277c8-24
- add ovmf 4m qcow2 images

* Fri May 12 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230301gitf80f052277c8-23
- require python3-virt-firmware v23.5

* Fri May 12 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230301gitf80f052277c8-22
- update NestedInterruptTplLib patches

* Fri May 05 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230301gitf80f052277c8-21
- drop ASSERT from NestedInterruptTplLib (rhbz#2183336).

* Thu Apr 27 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230301gitf80f052277c8-4
- fix tpm detection.

* Thu Apr 13 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230301gitf80f052277c8-2
- add StandaloneMM and ArmVirtQemuKernel builds.
- add json files for qcow2 images.
- update dbx files to 2023-03.

* Mon Mar 06 2023 Gerd Hoffmann <kraxel@redhat.com> - 20230301gitf80f052277c8-1
- update to edk2-stable202302
- update dbx database to 20220812
- add riscv64 sub-rpm

* Fri Feb 17 2023 Gerd Hoffmann <kraxel@redhat.com> - 20221117gitfff6d81270b5-14
- add sub-package with xen build (resolves: rhbz#2170730)

* Sat Feb 11 2023 Gerd Hoffmann <kraxel@redhat.com> - 20221117gitfff6d81270b5-13
- update openssl (CVE-2023-0286, CVE-2023-0215, CVE-2022-4450, CVE-2022-4304).

* Wed Feb 08 2023 Gerd Hoffmann <kraxel@redhat.com> - 20221117gitfff6d81270b5-12
- cherry-pick aarch64 bugfixes.
- set firmware build release date.
- add ext4 sub-package.

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20221117gitfff6d81270b5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jan 06 2023 Gerd Hoffmann <kraxel@redhat.com> - 20221117gitfff6d81270b5-10
- add experimental builds with strict nx checking.

* Mon Jan 02 2023 Gerd Hoffmann <kraxel@redhat.com> - 20221117gitfff6d81270b5-9
- revert 'make files sparse again' (resolves: rhbz#2155673).
- pick up compiler + linker flags from rpm

* Tue Dec 20 2022 Gerd Hoffmann <kraxel@redhat.com> - 20221117gitfff6d81270b5-8
- make files sparse again

* Thu Dec 15 2022 Gerd Hoffmann <kraxel@redhat.com> - 20221117gitfff6d81270b5-7
- backport https://github.com/tianocore/edk2/pull/3770

* Mon Dec 12 2022 Gerd Hoffmann <kraxel@redhat.com> - 20221117gitfff6d81270b5-6
- fix ovmf platform config (revert broken commit).
- show version information in smbios (backport).

* Mon Dec 05 2022 Gerd Hoffmann <kraxel@redhat.com> - 20221117gitfff6d81270b5-5
- rename *.json files to be more consistent.
- build script update

* Fri Dec 02 2022 Gerd Hoffmann <kraxel@redhat.com> - 20221117gitfff6d81270b5-4
- apply dbx updates

* Tue Nov 29 2022 Gerd Hoffmann <kraxel@redhat.com> - 20221117gitfff6d81270b5-3
- fix build script

* Mon Nov 28 2022 Gerd Hoffmann <kraxel@redhat.com> - 20221117gitfff6d81270b5-2
- add workaround for broken grub

* Tue Sep 20 2022 Gerd Hoffmann <kraxel@redhat.com> - 20220826gitba0e0e4c6a17-1
- update edk2 to 2022-08 stable tag.
- update openssl bundle to rhel-8.7 level.
- add stdvga fix.
- add 4MB firmware builds.

* Thu Aug 18 2022 Gerd Hoffmann <kraxel@redhat.com> - 20220526git16779ede2d36-5
- comment out patch #4 (bug 2116534 workaround)
- comment out patch #12 (bug 2114858 workaround)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20220526git16779ede2d36-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 10 2022 Gerd Hoffmann <kraxel@redhat.com> - 20220526git16779ede2d36-3
- swap stack fix patch.

* Wed Jun 08 2022 Gerd Hoffmann <kraxel@redhat.com> - 20220526git16779ede2d36-2
- fix PcdResizeXterm patch.
- minor specfile cleanup.
- add 0021-OvmfPkg-Sec-fix-stack-switch.patch
- Resolves rhbz#2093745

* Tue May 31 2022 Gerd Hoffmann <kraxel@redhat.com> - 20220526git16779ede2d36-1
- update to new edk2 stable tag (2022-05), refresh patches.
- add amdsev and inteltdx builds
- drop qosb

* Tue Apr 19 2022 Gerd Hoffmann <kraxel@redhat.com> - 20220221gitb24306f15daa-4
- switch to virt-firmware for secure boot key enrollment
- Stop builds on armv7 too (iasl missing).

* Thu Apr 07 2022 Gerd Hoffmann <kraxel@redhat.com> - 20220221gitb24306f15daa-3
- Fix TPM build options.
- Stop builds on i686 (iasl missing).
- Resolves rhbz#2072827

* Wed Mar 23 2022 Gerd Hoffmann <kraxel@redhat.com> - 20220221gitb24306f15daa-1
- Update to edk2-stable202202

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20211126gitbb1bba3d7767-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 6 2021 Gerd Hoffmann <kraxel@redhat.com> - 20211126gitbb1bba3d7767-1
- Update to edk2-stable202111
- Resolves rhbz#1978966
- Resolves rhbz#2026744

* Mon Dec  6 2021 Daniel P. Berrangé <berrange@redhat.com> - 20210527gite1999b264f1f-5
- Drop glibc strcmp workaround

* Mon Nov 29 2021 Daniel P. Berrangé <berrange@redhat.com> - 20210527gite1999b264f1f-4
- Drop customized splash screen boot logo
- Temporary workaround for suspected glibc strcmp bug breaking builds in koji

* Wed Sep  1 2021 Daniel P. Berrangé <berrange@redhat.com> - 20210527gite1999b264f1f-3
- Fix qemu packaging conditionals for ELN builds

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20210527gite1999b264f1f-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 20 2021 Cole Robinson <crobinso@redhat.com> - 20210527gite1999b264f1f-1
- Update to git snapshot
- Sync with c9s packaging

* Mon Jun 14 2021 Jiri Kucera <jkucera@redhat.com> - 20200801stable-5
- Replace genisoimage with xorriso

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20200801stable-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 03 2020 Cole Robinson <aintdiscole@gmail.com> - 20200801stable-3
- Really fix TPM breakage (bz 1897367)

* Tue Nov 24 2020 Cole Robinson <aintdiscole@gmail.com> - 20200801stable-2
- Fix openssl usage, unbreak TPM (bz 1897367)

* Wed Sep 16 2020 Cole Robinson <crobinso@redhat.com> - 20200801stable-1
- Update to edk2 stable 202008

* Sat Sep 12 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 20200201stable-6
- Tweaks for aarch64/ARMv7 builds
- Minor cleanups

* Tue Aug 04 2020 Cole Robinson <aintdiscole@gmail.com> - 20200201stable-5
- Fix build failures on rawhide

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200201stable-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200201stable-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 20200201stable-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Mon Apr 13 2020 Cole Robinson <aintdiscole@gmail.com> - 20200201stable-1
- Update to stable-202002

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20190501stable-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Sep 06 2019 Patrick Uiterwijk <puiterwijk@redhat.com> - 20190501stable-4
- Updated HTTP_BOOT option to new upstream value

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20190501stable-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 15 2019 Cole Robinson <aintdiscole@gmail.com> - 20190501stable-2
- License is now BSD-2-Clause-Patent
- Re-enable secureboot enrollment
- Use qemu-ovmf-secureboot from git

* Thu Jul 11 2019 Cole Robinson <crobinso@redhat.com> - 20190501stable-1
- Update to stable-201905
- Update to openssl-1.1.1b
- Ship VARS file for ovmf-ia32 (bug 1688596)
- Ship Fedora-variant JSON "firmware descriptor files"
- Resolves rhbz#1728652

* Mon Mar 18 2019 Cole Robinson <aintdiscole@gmail.com> - 20190308stable-1
- Use YYYYMMDD versioning to fix upgrade path

* Fri Mar 15 2019 Cole Robinson <aintdiscole@gmail.com> - 201903stable-1
- Update to stable-201903
- Update to openssl-1.1.0j
- Move to python3 deps

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20180815gitcb5f4f45ce-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 14 2018 Patrick Uiterwijk <puiterwijk@redhat.com> - 20180815gitcb5f4f45ce-5
- Add -qosb dependency on python3

* Fri Nov 9 2018 Paolo Bonzini <pbonzini@redhat.com> - 20180815gitcb5f4f45ce-4
- Fix network boot via grub (bz 1648476)

* Wed Sep 12 2018 Paolo Bonzini <pbonzini@redhat.com> - 20180815gitcb5f4f45ce-3
- Explicitly compile the scripts using py_byte_compile

* Fri Aug 31 2018 Cole Robinson <crobinso@redhat.com> - 20180815gitcb5f4f45ce-2
- Fix passing through RPM build flags (bz 1540244)

* Tue Aug 21 2018 Cole Robinson <crobinso@redhat.com> - 20180815gitcb5f4f45ce-1
- Update to edk2 git cb5f4f45ce, edk2-stable201808
- Update to qemu-ovmf-secureboot-1.1.3
- Enable TPM2 support

* Mon Jul 23 2018 Paolo Bonzini <pbonzini@redhat.com> - 20180529gitee3198e672e2-5
- Fixes for AMD SEV on OVMF_CODE.fd
- Add Provides for bundled OpenSSL

* Wed Jul 18 2018 Paolo Bonzini <pbonzini@redhat.com> - 20180529gitee3198e672e2-4
- Enable IPv6

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20180529gitee3198e672e2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 20 2018 Paolo Bonzini <pbonzini@redhat.com> - 20180529gitee3198e672e2-2
- Backport two bug fixes from RHEL: connect again virtio-rng devices, and
  connect consoles unconditionally in OVMF (ARM firmware already did it)

* Tue May 29 2018 Paolo Bonzini <pbonzini@redhat.com> - 20180529gitee3198e672e2-1
- Rebase to ee3198e672e2

* Tue May 01 2018 Cole Robinson <crobinso@redhat.com> - 20171011git92d07e4-7
- Bump release for new build

* Fri Mar 30 2018 Patrick Uiterwijk <puiterwijk@redhat.com> - 20171011git92d07e4-6
- Add qemu-ovmf-secureboot (qosb)
- Generate pre-enrolled Secure Boot OVMF VARS files

* Wed Mar 07 2018 Paolo Bonzini <pbonzini@redhat.com> - 20171011git92d07e4-5
- Fix GCC 8 compilation
- Replace dosfstools and mtools with qemu-img vvfat

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20171011git92d07e4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Paolo Bonzini <pbonzini@redhat.com> - 20170209git296153c5-3
- Add OpenSSL patches from Fedora
- Enable TLS_MODE

* Fri Nov 17 2017 Paolo Bonzini <pbonzini@redhat.com> - 20170209git296153c5-2
- Backport patches 19-21 from RHEL
- Add patches 22-24 to fix SEV slowness
- Add fedora conditionals

* Tue Nov 14 2017 Paolo Bonzini <pbonzini@redhat.com> - 20171011git92d07e4-1
- Import source and patches from RHEL version
- Update OpenSSL to 1.1.0e
- Refresh 0099-Tweak-the-tools_def-to-support-cross-compiling.patch

* Mon Nov 13 2017 Paolo Bonzini <pbonzini@redhat.com> - 20170209git296153c5-6
- Allow non-cross builds
- Install /usr/share/OVMF and /usr/share/AAVMF

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170209git296153c5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170209git296153c5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 15 2017 Cole Robinson <crobinso@redhat.com> - 20170209git296153c5-3
- Ship ovmf-ia32 package (bz 1424722)

* Thu Feb 16 2017 Cole Robinson <crobinso@redhat.com> - 20170209git296153c5-2
- Update EnrollDefaultKeys patch (bz #1398743)

* Mon Feb 13 2017 Paolo Bonzini <pbonzini@redhat.com> - 20170209git296153c5-1
- Rebase to git master
- New patch 0010 fixes failure to build from source.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20161105git3b25ca8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Nov 06 2016 Cole Robinson <crobinso@redhat.com> - 20161105git3b25ca8-1
- Rebase to git master

* Fri Sep  9 2016 Tom Callaway <spot@fedoraproject.org> - 20160418gita8c39ba-5
- replace legally problematic openssl source with "hobbled" tarball

* Thu Jul 21 2016 Gerd Hoffmann <kraxel@redhat.com> - 20160418gita8c39ba-4
- Also build for armv7.

* Tue Jul 19 2016 Gerd Hoffmann <kraxel@redhat.com> 20160418gita8c39ba-3
- Update EnrollDefaultKeys patch.

* Fri Jul 8 2016 Paolo Bonzini <pbonzini@redhat.com> - 20160418gita8c39ba-2
- Distribute edk2-ovmf on aarch64

* Sat May 21 2016 Cole Robinson <crobinso@redhat.com> - 20160418gita8c39ba-1
- Distribute edk2-aarch64 on x86 (bz #1338027)

* Mon Apr 18 2016 Gerd Hoffmann <kraxel@redhat.com> 20160418gita8c39ba-0
- Update to latest git.
- Add firmware builds (FatPkg is free now).

* Mon Feb 15 2016 Cole Robinson <crobinso@redhat.com> 20151127svn18975-3
- Fix FTBFS gcc warning (bz 1307439)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20151127svn18975-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 27 2015 Paolo Bonzini <pbonzini@redhat.com> - 20151127svn18975-1
- Rebase to 20151127svn18975-1
- Linker script renamed to GccBase.lds

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20150519svn17469-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 19 2015 Paolo Bonzini <pbonzini@redhat.com> - 20150519svn17469-1
- Rebase to 20150519svn17469-1
- edk2-remove-tree-check.patch now upstream

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 20140724svn2670-6
- Rebuilt for GCC 5 C++11 ABI change

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20140724svn2670-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 24 2014 Paolo Bonzini <pbonzini@redhat.com> - 20140724svn2670-1
- Rebase to 20140724svn2670-1

* Tue Jun 24 2014 Paolo Bonzini <pbonzini@redhat.com> - 20140624svn2649-1
- Use standalone .tar.xz from buildtools repo

* Tue Jun 24 2014 Paolo Bonzini <pbonzini@redhat.com> - 20140328svn15376-4
- Install BuildTools/BaseEnv

* Mon Jun 23 2014 Paolo Bonzini <pbonzini@redhat.com> - 20140328svn15376-3
- Rebase to get GCC48 configuration
- Package EDK_TOOLS_PATH as /usr/share/edk2
- Package "build" and LzmaF86Compress too, as well as the new
  tools Ecc and TianoCompress.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20131114svn14844-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Nov 14 2013 Paolo Bonzini <pbonzini@redhat.com> - 20131114svn14844-1
- Upgrade to r14844.
- Remove upstreamed parts of patch 1.

* Fri Nov 8 2013 Paolo Bonzini <pbonzini@redhat.com> - 20130515svn14365-7
- Make BaseTools compile on ARM.

* Fri Aug 30 2013 Paolo Bonzini <pbonzini@redhat.com> - 20130515svn14365-6
- Revert previous change; firmware packages should be noarch, and building
  BaseTools twice is simply wrong.

* Mon Aug 19 2013 Kay Sievers <kay@redhat.com> - 20130515svn14365-5
- Add sub-package with EFI shell

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130515svn14365-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 23 2013 Dan Horák <dan[at]danny.cz> 20130515svn14365-3
- set ExclusiveArch

* Thu May 16 2013 Paolo Bonzini <pbonzini@redhat.com> 20130515svn14365-2
- Fix edk2-tools-python Requires

* Wed May 15 2013 Paolo Bonzini <pbonzini@redhat.com> 20130515svn14365-1
- Split edk2-tools-doc and edk2-tools-python
- Fix Python BuildRequires
- Remove FatBinPkg at package creation time.
- Use fully versioned dependency.
- Add comment on how to generate the sources.

* Thu May 2 2013 Paolo Bonzini <pbonzini@redhat.com> 20130502.g732d199-1
- Create.

## END: Generated by rpmautospec
