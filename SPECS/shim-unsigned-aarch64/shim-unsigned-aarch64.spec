%global debug_package %{nil}
Summary:        First stage UEFI bootloader
Name:           shim-unsigned-aarch64
Version:        15.4
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/rhboot/shim
Source0:        https://github.com/rhboot/shim/releases/download/%{version}/shim-%{version}.tar.bz2
Source1:        sbat.csv.in
Source100:      cbl-mariner-ca-20210127.der
BuildRequires:  dos2unix
BuildRequires:  vim-extra
ExclusiveArch:  aarch64

%description
shim is a trivial EFI application that, when run, attempts to open and
execute another application.
On systems with a TPM chip enabled and supported by the system firmware,
shim will extend various PCRs with the digests of the targets it is
loading.

%prep
%autosetup -n shim-%{version} -p1
# shim Makefile expects vendor SBATs to be in data/sbat.<vendor>.csv
sed -e "s,@@VERSION_RELEASE@@,%{version}-%{release},g" %{SOURCE1} > ./data/sbat.microsoft.csv
cat ./data/sbat.microsoft.csv

%build
cp %{SOURCE100} cert.der
make shimaa64.efi VENDOR_CERT_FILE=cert.der

%install
install -vdm 755 %{buildroot}%{_datadir}/%{name}
install -vm 644 shimaa64.efi %{buildroot}%{_datadir}/%{name}/shimaa64.efi

%check
make VENDOR_CERT_FILE=cert.der test

%files
%defattr(-,root,root)
%license COPYRIGHT
%{_datadir}/%{name}/shimaa64.efi

%changelog
* Tue Mar 30 2021 Chris Co <chrco@microsoft.com> - 15.4-1
- Update to 15.4
- Remove extra patches. These are incorporated into latest version
- License verified

* Tue Aug 25 2020 Chris Co <chrco@microsoft.com> - 15-4
- Apply patch files (from CentOS: shim-15-8.el7)

* Thu Jul 30 2020 Chris Co <chrco@microsoft.com> - 15-3
- Update binary path

* Wed Jul 29 2020 Chris Co <chrco@microsoft.com> - 15-2
- Update built-in cert

* Wed Jun 24 2020 Chris Co <chrco@microsoft.com> - 15-1
- Original version for CBL-Mariner.
