# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: Common RPM Macros for building EFI-related packages
Name: efi-rpm-macros
Version: 6
Release: 5%{?dist}
License: GPL-3.0-or-later
URL: https://github.com/rhboot/%{name}/
BuildRequires: git sed
BuildRequires: make
BuildArch: noarch

Source0: https://github.com/rhboot/%{name}/releases/download/%{version}/%{name}-6.tar.bz2
# Not upstream, but trivial and posted upstream as a PR:
# https://github.com/rhboot/efi-rpm-macros/pull/3
Patch0001: 0001-add-riscv64-support.patch
Patch0002: 0002-Re-enable-ia32-as-an-alt-for-x86_64.patch

%global debug_package %{nil}
%global _efi_vendor_ %(eval echo $(sed -n -e 's/rhel/redhat/' -e 's/^ID=//p' /etc/os-release))

%description
%{name} provides a set of RPM macros for use in EFI-related packages.

%package -n efi-srpm-macros
Summary: Common SRPM Macros for building EFI-related packages
BuildArch: noarch
Requires: rpm

%description -n efi-srpm-macros
efi-srpm-macros provides a set of SRPM macros for use in EFI-related packages.

%package -n efi-filesystem
Summary: The basic directory layout for EFI machines
BuildArch: noarch
Requires: filesystem

%description -n efi-filesystem
The efi-filesystem package contains the basic directory layout for EFI
machine bootloaders and tools.

%prep
%autosetup -S git_am -n %{name}-6
git config --local --add efi.vendor "%{_efi_vendor_}"
git config --local --add efi.esp-root /boot/efi
git config --local --add efi.arches "x86_64 aarch64 %{arm} %{ix86} riscv64"

%build
%make_build clean all

%install
%make_install

#%%files
#%%{!?_licensedir:%%global license %%%%doc}
#%%license LICENSE
#%%doc README
#%%{_rpmmacrodir}/macros.efi

%files -n efi-srpm-macros
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README
%{_rpmmacrodir}/macros.efi-srpm
%{_rpmconfigdir}/brp-boot-efi-times

%files -n efi-filesystem
%defattr(0700,root,root,-)
%dir /boot/efi
%dir /boot/efi/EFI
%dir /boot/efi/EFI/BOOT
%dir /boot/efi/EFI/%{_efi_vendor_}

%changelog
* Mon Oct 27 2025 Peter Jones <pjones@redhat.com> - 6-5
- Re-add ia32 as per https://bodhi.fedoraproject.org/updates/FEDORA-2025-6a839fa19e

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Mar 14 2025 Kashyap Chamarthy <kchamart@redhat.com> - 6-3
- Re-add risc64 support; remove upstreamed patches.

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 10 2024 Nicolas Frayer <nfrayer@redhat.com> - 6-1
- Update to efi-rpm-macros version 6

* Fri Jul 19 2024 David Abdurachmanov <davidlt@rivosinc.com> - 5-13
- Add riscv64

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Dec 13 2023 Nicolas Frayer <nfrayer@redhat.com>
- Migrate to SPDX license
- Please refer to https://fedoraproject.org/wiki/Changes/SPDX_Licenses_Phase_2

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 09 2023 Sandro Bonazzola <sbonazzo@redhat.com> - 5-8
- Fixes permissions on /boot/efi/EFI
- Resolves: rhbz#2144459

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Sep 02 2021 Robbie Harwood <rharwood@redhat.com> - 5-4
- Remove arm as an alt for aarch64 (would require cross compiler)

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Apr 06 2021 Peter Jones <pjones@redhat.com> - 5-2
- There's always a typo.

* Tue Apr 06 2021 Peter Jones <pjones@redhat.com> - 5-1
- Add arm as an alt for aarch64

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Sep 26 2018 Peter Jones <pjones@redhat.com> - 4-1
- Provide %%{efi_build_requires} and brp-boot-efi-times

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri May 04 2018 Peter Jones <pjones@redhat.com> - 3-2
- Always provide macros for efi_arch and efi_alt_arch (and their _upper
  variants), and make efi_has_arch and efi_has_alt_arch 0 when they will be
  wrong.  This ensures everything can always expand when we're on a non-efi
  architecture.

* Fri May 04 2018 Peter Jones <pjones@redhat.com> - 3-1
- Update to version 3 to try and un-break rawhide composes due to
  ExclusiveArch constraints.

* Thu May 03 2018 Peter Jones <pjones@redhat.com> - 2-6
- Rework the macros for better srpm use.

* Wed May 02 2018 Peter Jones <pjones@redhat.com> - 2-5
- Add efi-filesystem subpackage

* Wed May 02 2018 Peter Jones <pjones@redhat.com> - 2-4
- Add %%{efi_has_alt_arch}

* Tue May 01 2018 Peter Jones <pjones@redhat.com> - 2-3
- Make an efi-srpm-macros subpackage to pull in so %%{efi} works in
  ExclusiveArch in koji.

* Tue May 01 2018 Peter Jones <pjones@redhat.com> - 2-2
- Fix the non-efi and non-efi-alt-arch cases, hopefully.
- Make efi-*-macros packages not be ExclusiveArch, because they need to work
  in non-efi-arch packages.

* Tue May 01 2018 Peter Jones <pjones@redhat.com> - 2-1
- Lots of rpmlint fixups and the like.

* Mon Apr 30 2018 Peter Jones <pjones@redhat.com> - 1-1
- First shot at building it.
