# RPM doesn't detect that code in /usr/share is python3, this forces it
# https://fedoraproject.org/wiki/Changes/Avoid_usr_bin_python_in_RPM_Build#Python_bytecompilation
%global __python python3
%global edk2_stable_date 202008
%global edk2_stable_str  edk2-stable%{edk2_stable_date}
%global openssl_version  1.1.1g
%global qosb_version     20190521-gitf158f12
%global softfloat_version 20180726-gitb64af41

%define qosb_testing 0
%define cross 0

%ifarch %{ix86} x86_64
%define build_ovmf_ia32 1
%ifarch x86_64
%define build_ovmf_x64 1
%endif
%endif

%ifarch aarch64
%define build_aavmf_aarch64 1
%endif

%ifarch %{arm}
%define build_aavmf_arm 1
%endif

%if 0%{?cross}
%define build_ovmf_x64 1
%define build_ovmf_ia32 1
%define build_aavmf_aarch64 1
%define build_aavmf_arm 1
%endif

# Enable this to skip secureboot enrollment, if problems pop up
%if %{with_check}
# keep enroll for testing (non containeried build env)
%global skip_enroll 0
%else
# skip enroll when building that blocks containerized build
%global skip_enroll 1
%endif

%ifarch x86_64
%if %{with_check}
%define qosb_testing 1
%endif
%endif

Summary:        EFI Development Kit II
Name:           edk2
# Even though edk2 stable releases are YYYYMM, we need
# to use YYYMMDD to avoid needing to bump package epoch
# due to previous 'git' Version:
Version:        %{edk2_stable_date}01stable
Release:        4%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/tianocore/tianocore.github.io/wiki/EDK-II/
# Needed due to a dependency on "nasm", which doesn't officially support the ARM64 architecture.
# See here: https://github.com/netwide-assembler/nasm/pull/3
ExclusiveArch:  x86_64

Source0:        https://github.com/tianocore/edk2/archive/%{edk2_stable_str}.tar.gz#/%{edk2_stable_str}.tar.gz
Source1:        openssl-%{openssl_version}-hobbled.tar.xz
Source2:        ovmf-whitepaper-c770f8c.txt
#Source3:        https://github.com/puiterwijk/qemu-ovmf-secureboot/archive/v{qosb_version}/qemu-ovmf-secureboot-{qosb_version}.tar.gz
Source3:        qemu-ovmf-secureboot-%{qosb_version}.tar.xz
Source4:        softfloat-%{softfloat_version}.tar.xz
Source5:        RedHatSecureBootPkKek1.pem
Source10:       hobble-openssl
Source11:       build-iso.sh
Source12:       update-tarball.sh
Source13:       openssl-patch-to-tarball.sh
# Fedora-specific JSON "descriptor files"
Source14:       40-edk2-ovmf-x64-sb-enrolled.json
Source15:       50-edk2-ovmf-x64-sb.json
Source16:       60-edk2-ovmf-x64.json
Source17:       40-edk2-ovmf-ia32-sb-enrolled.json
Source18:       50-edk2-ovmf-ia32-sb.json
Source19:       60-edk2-ovmf-ia32.json
Source20:       70-edk2-aarch64-verbose.json
Source21:       70-edk2-arm-verbose.json

# non-upstream patches
Patch0001:      0001-OvmfPkg-silence-EFI_D_VERBOSE-0x00400000-in-NvmExpre.patch
Patch0002:      0002-OvmfPkg-silence-EFI_D_VERBOSE-0x00400000-in-the-DXE-.patch
Patch0003:      0003-OvmfPkg-enable-DEBUG_VERBOSE.patch
Patch0004:      0004-OvmfPkg-increase-max-debug-message-length-to-512.patch
Patch0005:      0005-advertise-OpenSSL-on-TianoCore-splash-screen-boot-lo.patch
Patch0006:      0006-OvmfPkg-QemuVideoDxe-enable-debug-messages-in-VbeShi.patch
Patch0007:      0007-MdeModulePkg-TerminalDxe-add-other-text-resolutions.patch
Patch0008:      0008-MdeModulePkg-TerminalDxe-set-xterm-resolution-on-mod.patch
Patch0009:      0009-OvmfPkg-take-PcdResizeXterm-from-the-QEMU-command-li.patch
Patch0010:      0010-ArmVirtPkg-take-PcdResizeXterm-from-the-QEMU-command.patch
Patch0011:      0011-OvmfPkg-allow-exclusion-of-the-shell-from-the-firmwa.patch
Patch0012:      0012-ArmPlatformPkg-introduce-fixed-PCD-for-early-hello-m.patch
Patch0013:      0013-ArmPlatformPkg-PrePeiCore-write-early-hello-message-.patch
Patch0014:      0014-ArmVirtPkg-set-early-hello-message-RH-only.patch
Patch0015:      0015-Tweak-the-tools_def-to-support-cross-compiling.patch
Patch0016:      0016-BaseTools-do-not-build-BrotliCompress-RH-only.patch

BuildRequires:  bc
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  genisoimage
BuildRequires:  iasl
BuildRequires:  libuuid-devel
BuildRequires:  nasm
BuildRequires:  python3
BuildRequires:  python3-devel
# These are for QOSB
BuildRequires:  python3-requests
BuildRequires:  qemu-img
BuildRequires:  qemu-kvm
BuildRequires:  sed

%if 0%{?cross}
BuildRequires:  gcc-aarch64-linux-gnu
BuildRequires:  gcc-arm-linux-gnu
BuildRequires:  gcc-x86_64-linux-gnu
%endif

%if %{?qosb_testing}
# This is used for testing the enrollment: builds are run in a chroot, lacking
# a kernel. The testing is only performed on x86_64 for now, but we can't make
# the BuildRequires only on a specific arch, as that'd come through in the SRPM
# NOTE: The actual enrollment needs to happen in all builds for all architectures,
# because OVMF is built as noarch, which means that koji enforces that the build
# results don't actually differ per arch, and then it picks a random arches' build
# for the actual RPM.
BuildRequires:  kernel-core
%endif

%description
EDK II is a development code base for creating UEFI drivers, applications
and firmware images.

%package tools
Summary:        EFI Development Kit II Tools
License:        BSD

%description tools
This package provides tools that are needed to
build EFI executables and ROMs using the GNU tools.

%package tools-python
Summary:        EFI Development Kit II Tools
License:        BSD
Requires:       python3
BuildArch:      noarch

%description tools-python
This package provides tools that are needed to build EFI executables
and ROMs using the GNU tools.  You do not need to install this package;
you probably want to install edk2-tools only.

%package tools-doc
Summary:        Documentation for EFI Development Kit II Tools
License:        BSD
BuildArch:      noarch

%description tools-doc
This package documents the tools that are needed to
build EFI executables and ROMs using the GNU tools.

%package qosb
Summary:        Tool to enroll secureboot
License:        BSD
Requires:       python3
BuildArch:      noarch

%description qosb
This package contains QOSB (QEMU OVMF Secure Boot), which can enroll OVMF
variable files to enforce Secure Boot.

%if 0%{?build_ovmf_x64:1}
%package ovmf
Summary:        Open Virtual Machine Firmware
# OVMF includes the Secure Boot and IPv6 features; it has a builtin OpenSSL
# library.
License:        BSD AND OpenSSL
BuildArch:      noarch

Provides:       bundled(openssl)

Provides:       OVMF = %{version}-%{release}
Obsoletes:      OVMF < %{version}-%{release}

%description ovmf
EFI Development Kit II
Open Virtual Machine Firmware (x64)
%endif

%if 0%{?build_ovmf_ia32:1}
%package ovmf-ia32
Summary:        Open Virtual Machine Firmware
# OVMF includes the Secure Boot and IPv6 features; it has a builtin OpenSSL
# library.
License:        BSD AND OpenSSL
BuildArch:      noarch

Provides:       bundled(openssl)

%description ovmf-ia32
EFI Development Kit II
Open Virtual Machine Firmware (ia32)
%endif

%if 0%{?build_aavmf_aarch64:1}
%package aarch64
Summary:        AARCH64 Virtual Machine Firmware
# No Secure Boot for AAVMF yet, but we include OpenSSL for the IPv6/HTTP boot stack.
License:        BSD AND OpenSSL
BuildArch:      noarch

Provides:       AAVMF = %{version}-%{release}
Obsoletes:      AAVMF < %{version}-%{release}

Provides:       bundled(openssl)

%description aarch64
EFI Development Kit II
AARCH64 UEFI Firmware
%endif

%if 0%{?build_aavmf_arm:1}
%package arm
Summary:        ARM Virtual Machine Firmware
# No Secure Boot for ARMv7, but we include OpenSSL for the IPv6/HTTP boot stack.
License:        BSD AND OpenSSL
BuildArch:      noarch

%description arm
EFI Development Kit II
ARMv7 UEFI Firmware
%endif


%prep
%setup -q -n edk2-%{edk2_stable_str}

# Ensure old shell and binary packages are not used
rm -rf EdkShellBinPkg
rm -rf EdkShellPkg
rm -rf FatBinPkg
rm -rf ShellBinPkg

# copy whitepaper into place
cp -a -- %{SOURCE2} .
# extract openssl into place
tar -xf %{SOURCE1} --strip-components=1 --directory CryptoPkg/Library/OpensslLib/openssl
# extract softfloat into place
tar -xf %{SOURCE4} --strip-components=1 --directory ArmPkg/Library/ArmSoftFloatLib/berkeley-softfloat-3/

# Extract QOSB
tar -xf %{SOURCE3}
mv qemu-ovmf-secureboot-%{qosb_version}/README.md README.qosb
mv qemu-ovmf-secureboot-%{qosb_version}/LICENSE LICENSE.qosb

%autopatch -p1
base64 --decode < MdeModulePkg/Logo/Logo-OpenSSL.bmp.b64 > MdeModulePkg/Logo/Logo-OpenSSL.bmp

# Extract OEM string from the RH cert, as described here
# https://bugzilla.tianocore.org/show_bug.cgi?id=1747#c2
sed \
  -e 's/^-----BEGIN CERTIFICATE-----$/4e32566d-8e9e-4f52-81d3-5bb9715f9727:/' \
  -e '/^-----END CERTIFICATE-----$/d' \
  %{_sourcedir}/RedHatSecureBootPkKek1.pem \
| tr -d '\n' \
> PkKek1.oemstr


%build
export PYTHON_COMMAND=python3
source ./edksetup.sh

# compiler
CC_FLAGS="-t GCC5"

# parallel builds
JOBS="%{?_smp_mflags}"
JOBS="${JOBS#-j}"
if test "$JOBS" != ""; then
        CC_FLAGS="${CC_FLAGS} -n $JOBS"
fi

# common features
CC_FLAGS="$CC_FLAGS --cmd-len=65536 -b DEBUG --hash"
CC_FLAGS="$CC_FLAGS -D NETWORK_IP6_ENABLE"
CC_FLAGS="$CC_FLAGS -D NETWORK_TLS_ENABLE"
CC_FLAGS="$CC_FLAGS -D NETWORK_HTTP_BOOT_ENABLE"
CC_FLAGS="$CC_FLAGS -D TPM2_ENABLE"

# ovmf features
OVMF_FLAGS="${CC_FLAGS}"
OVMF_FLAGS="${OVMF_FLAGS} -D FD_SIZE_2MB"

# ovmf + secure boot features
OVMF_SB_FLAGS="${OVMF_FLAGS}"
OVMF_SB_FLAGS="${OVMF_SB_FLAGS} -D SECURE_BOOT_ENABLE"
OVMF_SB_FLAGS="${OVMF_SB_FLAGS} -D SMM_REQUIRE"
OVMF_SB_FLAGS="${OVMF_SB_FLAGS} -D EXCLUDE_SHELL_FROM_FD"

# arm firmware features
ARM_FLAGS="${CC_FLAGS}"

unset MAKEFLAGS
%make_build -C BaseTools \
  EXTRA_OPTFLAGS="%{optflags}" \
  EXTRA_LDFLAGS="%{__global_ldflags}"
sed -i -e 's/-Werror//' Conf/tools_def.txt


%if 0%{?cross}
export GCC5_IA32_PREFIX="x86_64-linux-gnu-"
export GCC5_X64_PREFIX="x86_64-linux-gnu-"
export GCC5_AARCH64_PREFIX="aarch64-linux-gnu-"
export GCC5_ARM_PREFIX="arm-linux-gnu-"
%endif

# build ovmf (x64)
%if 0%{?build_ovmf_x64:1}
mkdir -p ovmf
build ${OVMF_FLAGS} -a X64 -p OvmfPkg/OvmfPkgX64.dsc
cp Build/OvmfX64/*/FV/OVMF_*.fd ovmf/
rm -rf Build/OvmfX64

# build ovmf (x64) with secure boot
build ${OVMF_SB_FLAGS} -a IA32 -a X64 -p OvmfPkg/OvmfPkgIa32X64.dsc
cp Build/Ovmf3264/*/FV/OVMF_CODE.fd ovmf/OVMF_CODE.secboot.fd

# build ovmf (x64) shell iso with EnrollDefaultKeys
cp Build/Ovmf3264/*/X64/Shell.efi ovmf/
cp Build/Ovmf3264/*/X64/EnrollDefaultKeys.efi ovmf
sh %{_sourcedir}/build-iso.sh ovmf/

%if !%{skip_enroll}
python3 qemu-ovmf-secureboot-%{qosb_version}/ovmf-vars-generator \
    --qemu-binary %{_bindir}/qemu-system-x86_64 \
    --ovmf-binary ovmf/OVMF_CODE.secboot.fd \
    --ovmf-template-vars ovmf/OVMF_VARS.fd \
    --uefi-shell-iso ovmf/UefiShell.iso \
    --oem-string "$(< PkKek1.oemstr)" \
    --skip-testing \
    ovmf/OVMF_VARS.secboot.fd
%else
# This isn't going to actually give secureboot, but makes json files happy
# if we need to test disabling ovmf-vars-generator
cp ovmf/OVMF_VARS.fd ovmf/OVMF_VARS.secboot.fd
%endif
%endif


# build ovmf-ia32
%if 0%{?build_ovmf_ia32:1}
mkdir -p ovmf-ia32
build ${OVMF_FLAGS} -a IA32 -p OvmfPkg/OvmfPkgIa32.dsc
cp Build/OvmfIa32/*/FV/OVMF_CODE*.fd ovmf-ia32/
# cp VARS files from from ovmf/, which are all we need
cp ovmf/OVMF_VARS*.fd ovmf-ia32/
rm -rf Build/OvmfIa32

# build ovmf-ia32 with secure boot
build ${OVMF_SB_FLAGS} -a IA32 -p OvmfPkg/OvmfPkgIa32.dsc
cp Build/OvmfIa32/*/FV/OVMF_CODE.fd ovmf-ia32/OVMF_CODE.secboot.fd

# build ovmf-ia32 shell iso with EnrollDefaultKeys
cp Build/OvmfIa32/*/IA32/Shell.efi ovmf-ia32/Shell.efi
cp Build/OvmfIa32/*/IA32/EnrollDefaultKeys.efi ovmf-ia32/EnrollDefaultKeys.efi
sh %{_sourcedir}/build-iso.sh ovmf-ia32/
%endif


# build aarch64 firmware
%if 0%{?build_aavmf_aarch64:1}
mkdir -p aarch64
build $ARM_FLAGS -a AARCH64 -p ArmVirtPkg/ArmVirtQemu.dsc
cp Build/ArmVirtQemu-AARCH64/DEBUG_*/FV/*.fd aarch64
dd of="aarch64/QEMU_EFI-pflash.raw" if="/dev/zero" bs=1M count=64
dd of="aarch64/QEMU_EFI-pflash.raw" if="aarch64/QEMU_EFI.fd" conv=notrunc
dd of="aarch64/vars-template-pflash.raw" if="/dev/zero" bs=1M count=64
%endif


# build ARMv7 firmware
%if 0%{?build_aavmf_arm:1}
mkdir -p arm
build $ARM_FLAGS -a ARM -p ArmVirtPkg/ArmVirtQemu.dsc
cp Build/ArmVirtQemu-ARM/DEBUG_*/FV/*.fd arm
dd of="arm/QEMU_EFI-pflash.raw" if="/dev/zero" bs=1M count=64
dd of="arm/QEMU_EFI-pflash.raw" if="arm/QEMU_EFI.fd" conv=notrunc
dd of="arm/vars-template-pflash.raw" if="/dev/zero" bs=1M count=64
%endif



%check
%if 0%{?build_ovmf_x64:1}
%if 0%{?qosb_testing}
%if !%{skip_enroll}
python3 qemu-ovmf-secureboot-%{qosb_version}/ovmf-vars-generator \
    --qemu-binary %{_bindir}/qemu-system-x86_64 \
    --ovmf-binary ovmf/OVMF_CODE.secboot.fd \
    --ovmf-template-vars ovmf/OVMF_VARS.fd \
    --uefi-shell-iso ovmf/UefiShell.iso \
    --skip-enrollment \
    --print-output \
    --no-download \
    --kernel-path `rpm -ql kernel-core | grep "\/vmlinuz$" -m 1` \
    ovmf/OVMF_VARS.secboot.fd
%endif
%endif
%endif



%install
cp CryptoPkg/Library/OpensslLib/openssl/LICENSE LICENSE.openssl
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

cp -R BaseTools/Source/Python %{buildroot}%{_datadir}/%{name}/Python
for i in build BPDG Ecc GenDepex GenFds GenPatchPcdTable PatchPcdValue TargetTool Trim UPT; do
echo '#!/bin/sh
export PYTHONPATH=%{_datadir}/%{name}/Python
exec python3 '%{_datadir}/%{name}/Python/$i/$i.py' "$@"' > %{buildroot}%{_bindir}/$i
  chmod +x %{buildroot}%{_bindir}/$i
done

# For distro-provided firmware packages, the specification
# (https://git.qemu.org/?p=qemu.git;a=blob;f=docs/interop/firmware.json)
# says the JSON "descriptor files" to be searched in this directory:
# `/usr/share/firmware/`.  Create it.
mkdir -p %{buildroot}/%{_datadir}/qemu/firmware

mkdir -p %{buildroot}%{_datadir}/%{name}
%if 0%{?build_ovmf_x64:1}
cp -a ovmf %{buildroot}%{_datadir}/%{name}
# Libvirt hardcodes this directory name
mkdir %{buildroot}%{_datadir}/OVMF
ln -sf ../%{name}/ovmf/OVMF_CODE.fd                %{buildroot}%{_datadir}/OVMF
ln -sf ../%{name}/ovmf/OVMF_CODE.secboot.fd        %{buildroot}%{_datadir}/OVMF
ln -sf ../%{name}/ovmf/OVMF_VARS.fd                %{buildroot}%{_datadir}/OVMF
ln -sf ../%{name}/ovmf/OVMF_VARS.secboot.fd        %{buildroot}%{_datadir}/OVMF
ln -sf ../%{name}/ovmf/UefiShell.iso               %{buildroot}%{_datadir}/OVMF

for f in %{_sourcedir}/*edk2-ovmf-x64*.json; do
    install -pm 644 $f %{buildroot}/%{_datadir}/qemu/firmware
done
%endif


%if 0%{?build_ovmf_ia32:1}
cp -a ovmf-ia32 %{buildroot}%{_datadir}/%{name}

for f in %{_sourcedir}/*edk2-ovmf-ia32*.json; do
    install -pm 644 $f %{buildroot}/%{_datadir}/qemu/firmware
done
%endif


%if 0%{?build_aavmf_aarch64:1}
cp -a aarch64 %{buildroot}%{_datadir}/%{name}
# Libvirt hardcodes this directory name
mkdir %{buildroot}%{_datadir}/AAVMF
ln -sf ../%{name}/aarch64/QEMU_EFI-pflash.raw      %{buildroot}%{_datadir}/AAVMF/AAVMF_CODE.fd
ln -sf ../%{name}/aarch64/vars-template-pflash.raw %{buildroot}%{_datadir}/AAVMF/AAVMF_VARS.fd

for f in %{_sourcedir}/*edk2-aarch64*.json; do
    install -pm 644 $f %{buildroot}/%{_datadir}/qemu/firmware
done
%endif


%if 0%{?build_aavmf_arm:1}
cp -a arm %{buildroot}%{_datadir}/%{name}
ln -sf ../%{name}/arm/QEMU_EFI-pflash.raw          %{buildroot}%{_datadir}/AAVMF/AAVMF32_CODE.fd

for f in %{_sourcedir}/*edk2-arm*.json; do
    install -pm 644 $f %{buildroot}/%{_datadir}/qemu/firmware
done
%endif

%if 0%{?py_byte_compile:1}
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python_Appendix/#manual-bytecompilation
%py_byte_compile %{python3} %{buildroot}%{_datadir}/edk2/Python
%endif


install qemu-ovmf-secureboot-%{qosb_version}/ovmf-vars-generator %{buildroot}%{_bindir}


%files tools
%license LICENSE.openssl License.txt
%{_bindir}/DevicePath
%{_bindir}/EfiRom
%{_bindir}/GenCrc32
%{_bindir}/GenFfs
%{_bindir}/GenFv
%{_bindir}/GenFw
%{_bindir}/GenSec
%{_bindir}/LzmaCompress
%{_bindir}/LzmaF86Compress
%{_bindir}/Split
%{_bindir}/TianoCompress
%{_bindir}/VfrCompile
%{_bindir}/VolInfo
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/BuildEnv
%{_datadir}/%{name}/Conf
%{_datadir}/%{name}/Scripts

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

%files tools-doc
%doc BaseTools/UserManuals/*.rtf

%files qosb
%license LICENSE.qosb
%doc README.qosb
%{_bindir}/ovmf-vars-generator

%if 0%{?build_ovmf_x64:1}
%files ovmf
%license LICENSE.openssl OvmfPkg/License.txt
%doc OvmfPkg/README
%doc ovmf-whitepaper-c770f8c.txt
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/ovmf
%dir %{_datadir}/qemu/firmware
%{_datadir}/%{name}/ovmf/OVMF*.fd
%{_datadir}/%{name}/ovmf/*.efi
%{_datadir}/%{name}/ovmf/*.iso
%{_datadir}/qemu/firmware/*edk2-ovmf-x64*.json
%{_datadir}/OVMF
%endif

%if 0%{?build_ovmf_ia32:1}
%files ovmf-ia32
%license LICENSE.openssl OvmfPkg/License.txt
%doc OvmfPkg/README
%doc ovmf-whitepaper-c770f8c.txt
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/ovmf-ia32
%dir %{_datadir}/qemu/firmware
%{_datadir}/%{name}/ovmf-ia32/OVMF*.fd
%{_datadir}/%{name}/ovmf-ia32/*.efi
%{_datadir}/%{name}/ovmf-ia32/*.iso
%{_datadir}/qemu/firmware/*edk2-ovmf-ia32*.json
%endif

%if 0%{?build_aavmf_aarch64:1}
%files aarch64
%license LICENSE.openssl OvmfPkg/License.txt
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/aarch64
%dir %{_datadir}/qemu/firmware
%{_datadir}/%{name}/aarch64/QEMU*.fd
%{_datadir}/%{name}/aarch64/*.raw
%{_datadir}/qemu/firmware/*edk2-aarch64*.json
%{_datadir}/AAVMF/AAVMF_*
%endif

%if 0%{?build_aavmf_arm:1}
%files arm
%license LICENSE.openssl OvmfPkg/License.txt
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/arm
%dir %{_datadir}/qemu/firmware
%{_datadir}/%{name}/arm/QEMU*.fd
%{_datadir}/%{name}/arm/*.raw
%{_datadir}/qemu/firmware/*edk2-arm*.json
%{_datadir}/AAVMF/AAVMF32_*
%endif

%changelog
* Thu Jun 02 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200801stable-4
- Switching to building exclusively for AMD64 due to dependency on "nasm".

* Thu Apr 07 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 20200801stable-3
- Skip enroll that blocks building from containerized environment.
- License verified.

* Tue Jul 06 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200801stable-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- Turn off cross-compilation.
- Replace BR 'qemu-system-x86' with Mariner's 'qemu-kvm'.
- Hiding test-only BRs behind the 'with_check' macro.

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
