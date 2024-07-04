%global debug_package %{nil}
%define release_number %(echo "%{release}" | cut -d. -f1)
Summary:        First stage UEFI bootloader
Name:           shim
Version:        15.8
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/rhboot/shim
# The below source URL will point to the backing shim source code version used
# to build the shim binary which has been signed with the MS UEFI CA. This is
# needed for component governance.
# The Source0 that gets used is actually the signed shim binary, whose filename
# is annotated after the '#'. The signed shim binary is named with the following
# schema to avoid name collisions:
#   signed-shim<arch>-<version>-<release>.<dist tag>.efi
Source0:        https://github.com/rhboot/shim/releases/download/%{version}/shim-%{version}.tar.bz2#/signed-shimx64-%{version}-%{release}.efi
# Currently, the tarball only contains a UEFI CA signed x86_64 shim binary.
# Upstream aarch64 shim 15.4 builds are in a bad state. They will break using
# binutils versions before 2.35, and even after that they may give
# unpredictable results. Due to this, aarch64 shims are not being accepted
# for shim signing at this time.
#
# Once upstream aarch64 shim builds stabilize and are being accepted for
# review/signing, we should update this spec to also include UEFI CA signed
# aarch64 shim binaries
ExclusiveArch:  x86_64

%description
Initial UEFI bootloader that handles chaining to a trusted full bootloader
under secure boot environments.

%prep
%autosetup -n signed-%{name}-%{version}-%{release_number}

%install
install -d %{buildroot}/boot/efi/EFI/BOOT
install -m644 %{SOURCE0} %{buildroot}/boot/efi/EFI/BOOT/bootx64.efi

%files
%defattr(-,root,root)
/boot/efi/EFI/BOOT/bootx64.efi

%changelog
* Mon Jul 01 2024 Chris Co <chrco@microsoft.com> - 15.8-1
- Update shim binary to newer version associated with the 15.8-1 unsigned build.

* Tue Feb 08 2022 Chris Co <chrco@microsoft.com> - 15.4-2
- Update signed shim binary to newer one associated with 15.4-2 unsigned build.
- License verified

* Fri Apr 16 2021 Chris Co <chrco@microsoft.com> - 15.4-1
- Original version for CBL-Mariner.
