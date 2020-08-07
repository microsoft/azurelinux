%global debug_package %{nil}
Summary:        First stage UEFI bootloader
Name:           shim-unsigned-x64
Version:        15
Release:        5%{?dist}
URL:            https://github.com/rhboot/shim
License:        BSD
Vendor:         Microsoft
Distribution:   Mariner
Source0:        https://github.com/rhboot/shim/releases/download/%{version}/shim-%{version}.tar.bz2
Source1:        cbl-mariner-ca.der
ExclusiveArch:  x86_64

BuildRequires:  gnu-efi
BuildRequires:  gnu-efi-devel

%description
shim is a trivial EFI application that, when run, attempts to open and
execute another application.
On systems with a TPM chip enabled and supported by the system firmware,
shim will extend various PCRs with the digests of the targets it is
loading.

%prep
%setup -q -n shim-%{version}

%build
cp %{SOURCE1} cert.der
make shimx64.efi VENDOR_CERT_FILE=cert.der EFI_PATH=/usr/lib/gnuefi

%install
install -vdm 755 %{buildroot}/usr/share/%{name}
install -vm 644 shimx64.efi %{buildroot}/usr/share/%{name}/shimx64.efi

%files
%defattr(-,root,root)
%license COPYRIGHT
/usr/share/%{name}/shimx64.efi

%changelog
* Wed Jul 29 2020 Chris Co <chrco@microsoft.com> 15-5
- Update built-in cert
* Mon Jun 22 2020 Chris Co <chrco@microsoft.com> 15-4
- Update install path
* Thu May 14 2020 Chris Co <chrco@microsoft.com> 15-3
- Update test key
* Mon May 04 2020 Emre Girgin <mrgirgin@microsoft.com> 15-2
- Replace BuildArch with ExclusiveArch
* Wed Apr 29 2020 Chris Co <chrco@microsoft.com> 15-1
- Original version for CBL-Mariner.