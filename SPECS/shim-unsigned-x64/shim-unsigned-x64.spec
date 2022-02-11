%global debug_package %{nil}
Summary:        First stage UEFI bootloader
Name:           shim-unsigned-x64
Version:        15.4
Release:        2%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/rhboot/shim
Source0:        https://github.com/rhboot/shim/releases/download/%{version}/shim-%{version}.tar.bz2
Source1:        sbat.csv.in
Source100:      cbl-mariner-ca-20211013.der
Patch0:         Don-t-call-QueryVariableInfo-on-EFI-1.10-machines.patch
Patch1:         Fix-handling-of-ignore_db-and-user_insecure_mode.patch
Patch2:         Fix-a-broken-file-header-on-ia32.patch
Patch3:         mok-allocate-MOK-config-table-as-BootServicesData.patch
Patch4:         shim-another-attempt-to-fix-load-options-handling.patch
Patch5:         Relax-the-check-for-import_mok_state.patch
BuildRequires:  dos2unix
BuildRequires:  vim-extra
ExclusiveArch:  x86_64

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
make shimx64.efi VENDOR_CERT_FILE=cert.der

%install
install -vdm 755 %{buildroot}%{_datadir}/%{name}
install -vm 644 shimx64.efi %{buildroot}%{_datadir}/%{name}/shimx64.efi

%check
make VENDOR_CERT_FILE=cert.der test

%files
%defattr(-,root,root)
%license COPYRIGHT
%{_datadir}/%{name}/shimx64.efi

%changelog
* Wed Jan 05 2022 Chris Co <chrco@microsoft.com> - 15.4-2
- Update key
- License verified

* Tue Mar 30 2021 Chris Co <chrco@microsoft.com> - 15.4-1
- Update to 15.4
- Remove extra patches. These are incorporated into latest version

* Tue Aug 25 2020 Chris Co <chrco@microsoft.com> - 15-6
- Apply patch files (from CentOS: shim-15-8.el7)

* Wed Jul 29 2020 Chris Co <chrco@microsoft.com> - 15-5
- Update built-in cert

* Mon Jun 22 2020 Chris Co <chrco@microsoft.com> - 15-4
- Update install path

* Thu May 14 2020 Chris Co <chrco@microsoft.com> - 15-3
- Update test key

* Mon May 04 2020 Emre Girgin <mrgirgin@microsoft.com> - 15-2
- Replace BuildArch with ExclusiveArch

* Wed Apr 29 2020 Chris Co <chrco@microsoft.com> - 15-1
- Original version for CBL-Mariner.
