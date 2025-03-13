%global debug_package %{nil}
Summary:        Firmware update EFI binaries
Name:           fwupd-efi
Version:        1.6
Release:        2%{?dist}
License:        LGPL-2.1-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/fwupd/fwupd-efi
Source0:        https://github.com/fwupd/fwupd-efi/releases/download/%{version}/%{name}-%{version}.tar.xz
# Tolerate a slightly older version of gnu-efi
Patch1:         azure_linux_compat.patch
BuildRequires:  gcc
BuildRequires:  gnu-efi-devel
BuildRequires:  meson
BuildRequires:  pesign
BuildRequires:  python3-pefile
BuildRequires:  python3-uswid
BuildRequires:  python3-cbor2
BuildRequires:  python3-lxml

# these are the only architectures supporting UEFI UpdateCapsule
ExclusiveArch:  x86_64 aarch64

%description
fwupd is a project to allow updating device firmware, and this package provides
the EFI binary that is used for updating using UpdateCapsule.

%prep
%autosetup -p1

%build

%meson \
    -Defi_sbat_distro_id="azurelinux" \
    -Defi_sbat_distro_summary="Microsoft" \
    -Defi_sbat_distro_pkgname="%{name}" \
    -Defi_sbat_distro_version="%{version}-%{release}" \
    -Defi_sbat_distro_url="https://github.com/microsoft/azurelinux"

%meson_build

%install
%meson_install

# sign fwupd.efi loader
%ifarch x86_64
%global efiarch x64
%endif
%ifarch aarch64
%global efiarch aa64
%endif
%global fwup_efi_fn %{buildroot}%{_libexecdir}/fwupd/efi/fwupd%{efiarch}.efi
%pesign -s -i %{fwup_efi_fn} -o %{fwup_efi_fn}.tmp
%define __pesign_client_cert fwupd-signer
%pesign -s -i %{fwup_efi_fn}.tmp -o %{fwup_efi_fn}.signed
rm -vf %{fwup_efi_fn}.tmp

%files
%doc README.md AUTHORS
%license COPYING
%{_libexecdir}/fwupd/efi/*.efi
%{_libexecdir}/fwupd/efi/*.efi.signed
%{_libdir}/pkgconfig/fwupd-efi.pc

%changelog
* Mon Oct 28 2024 Jocelyn Berrendonner <jocelynb@microsoft.com> - 1.6-2
- Integrating the spec into Azure Linux
- Initial CBL-Mariner import from Fedora 42 (license: MIT).
- License verified.

* Mon Apr 15 2024 Richard Hughes <richard@hughsie.com> - 1.6-1
- New upstream release

* Fri Mar 22 2024 Richard Hughes <richard@hughsie.com> - 1.5-3
- Build against the new gnu-efi

* Mon Mar 18 2024 Richard Hughes <richard@hughsie.com> - 1.5-2
- Revert a patch to fix firmware updates

* Mon Mar 18 2024 Richard Hughes <richard@hughsie.com> - 1.5-1
- New upstream release

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.4-3
- Fix build with latest gnu-efi

* Wed Feb 22 2023 Richard Hughes <richard@hughsie.com> - 1.4-2
- migrated to SPDX license

* Fri Jan 27 2023 Richard Hughes <richard@hughsie.com> - 1.4-1
- New upstream release

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Apr 14 2022 Richard Hughes <richard@hughsie.com> - 1.3-1
- New package version

* Sun Jan 23 2022 Richard Hughes <richard@hughsie.com> - 1.2-1
- New package version

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jun 19 2021 Richard Hughes <richard@hughsie.com> - 1.1-1
- New package version

* Mon May 17 2021 Richard Hughes <richard@hughsie.com> - 1.0-2
- Rebuilt to use the HSM signers

* Wed Apr 28 2021 Richard Hughes <richard@hughsie.com> - 1.0-1
- Initial import (#1953508).
