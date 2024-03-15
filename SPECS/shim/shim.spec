
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
Name:           shim-%{efiarch}
# Note - version and release *must* match shim-unsigned
Version:        15.8
Release:        3%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/rhboot/shim

ExclusiveArch:  x86_64 aarch64

Provides:       shim = %{version}-%{release}
Provides:       shim-signed = %{version}-%{release}
Provides:       shim-signed-%{efiarch} = %{version}-%{release}

BuildRequires:  shim-unsigned-%{efiarch} = %{version}-%{release}

# This is the signed shim which has been reviewed upstream by
# https://github.com/rhboot/shim-review and then signed by the
# Microsoft UEFI signing key
Source0:        shim%{efiarch}.efi

%description
Initial UEFI bootloader that handles chaining to a trusted full bootloader
under secure boot environments. This package contains the shim EFI image
signed for secure boot. The package is specifically created for installing
on %{_arch} systems.

%prep
rm -rf %{_builddir}/%{name}-%{version}
mkdir -p %{_builddir}/%{name}-%{version}

%build
mkdir -p BOOT
cp -av %{SOURCE0} BOOT/boot%{efiarch}.efi
cp -av %{shimdir}/fb%{efiarch}.efi BOOT

mkdir -p %{efidir}
cp -av %{SOURCE0} %{efidir}/shim%{efiarch}.efi
cp -av %{shimdir}/mm%{efiarch}.efi %{efidir}

# Start with the UTF-16LE BOM magic number
echo -ne "\xff\xfe" > utf16le.bom

for csv in %{shimdir}/*.CSV; do
    cat utf16le.bom $csv >> %{efidir}/$(basename $csv)
done

%install
mkdir -p %{buildroot}%{_sysconfdir}/dnf/protected.d
echo "%{name}" > %{buildroot}%{_sysconfdir}/dnf/protected.d/%{name}.conf

mkdir -p %{buildroot}/boot/efi/EFI
mv -v BOOT %{buildroot}/boot/efi/EFI
mv -v %{efidir} %{buildroot}/boot/efi/EFI

%files
%defattr(-,root,root)
%{_sysconfdir}/dnf/protected.d/%{name}.conf
/boot/efi/EFI/BOOT/*
/boot/efi/EFI/%{efidir}/*

%changelog
* Wed Mar 13 2024 Dan Streetman <ddstreet@microsoft.com> - 15.8-3
- update to 15.8
- include mm and fb
- protect from dnf removal

* Tue Feb 08 2022 Chris Co <chrco@microsoft.com> - 15.4-2
- Update signed shim binary to newer one associated with 15.4-2 unsigned build.
- License verified

* Fri Apr 16 2021 Chris Co <chrco@microsoft.com> - 15.4-1
- Original version for CBL-Mariner.
