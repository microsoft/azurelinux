
%ifarch x86_64
%global efiarch x64
%endif
%ifarch aarch64
%global efiarch aa64
%endif

# From shim-unsigned-%%{efiarch}
%global efidir azurelinux
%global shimrootdir %{_datadir}/shim/
%global shimversiondir %{shimrootdir}/%{version}-%{release}
%global shimdir %{shimversiondir}/%{efiarch}

Summary:        First stage UEFI bootloader
Name:           shim-signed-%{efiarch}
Version:        15.8
Release:        3%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/rhboot/shim
# This package's "version" and "release" must reflect the unsigned version that
# was signed.
# An important consequence is that when making a change to this package, the
# unsigned version/release must be increased to keep the two versions consistent.
# Ideally though, this spec will not change much or at all, so the version will
# just track the unsigned package's version/release.
#
# To populate these sources:
#   1. Build the unsigned packages as normal
#   2. Sign the desired binary
#   3. Place the unsigned package and signed binary in this spec's folder
#   4. Build this spec
Source0:        shim-%{efiarch}-%{version}-%{release}.%{_arch}.rpm
Source1:        mm%{efiarch}.efi
Source2:        fb%{efiarch}.efi

# Only x86-64 for now...no aarch64 yet
ExclusiveArch:  x86_64

Provides:       shim = %{version}-%{release}
Provides:       shim-signed = %{version}-%{release}
Provides:       shim-signed-%{efiarch} = %{version}-%{release}

BuildRequires:  shim-unsigned-%{efiarch}

%description
Initial UEFI bootloader that handles chaining to a trusted full bootloader
under secure boot environments. This package contains the shim EFI image
signed for secure boot. The package is specifically created for installing
on %{_arch} systems.

%install
rpm --nodb --notriggers --noscripts --nodeps -r %{buildroot} -i %{SOURCE0}

cp -vf %{SOURCE1} %{buildroot}/boot/efi/EFI/%{efidir}

cp -vf %{SOURCE2} %{buildroot}/boot/efi/EFI/BOOT

%files
%defattr(-,root,root)
%{_sysconfdir}/dnf/protected.d/shim-%{efiarch}.conf
/boot/efi/EFI/BOOT/*
/boot/efi/EFI/%{efidir}/*
# If rpm created its DB, just ignore it
%exclude /var/lib/rpm

%changelog
* Wed Mar 13 2024 Dan Streetman <ddstreet@microsoft.com> - 15.8-3
- Original version for Azure Linux.
- License verified
