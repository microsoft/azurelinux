%global debug_package %{nil}
%global _efi_vendor_ %(eval echo $(sed -n -e 's/rhel/redhat/' -e 's/^ID=//p' %{_sysconfdir}/os-release))

Summary:        Common RPM Macros for building EFI-related packages
Name:           efi-rpm-macros
Version:        4
Release:        6%{?dist}
License:        GPLv3
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/rhboot/%{name}/
Source0:        https://github.com/rhboot/%{name}/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  %{_sysconfdir}/os-release
BuildRequires:  bash
BuildRequires:  git
BuildRequires:  sed

%description
%{name} provides a set of RPM macros for use in EFI-related packages.

%package -n efi-srpm-macros
Summary:        Common SRPM Macros for building EFI-related packages

Requires:       rpm

%description -n efi-srpm-macros
efi-srpm-macros provides a set of SRPM macros for use in EFI-related packages.

%package -n efi-filesystem
Summary:        The basic directory layout for EFI machines

Requires:       filesystem

%description -n efi-filesystem
The efi-filesystem package contains the basic directory layout for EFI
machine bootloaders and tools.

%prep
%autosetup -S git
git config --local --add efi.vendor "%{_efi_vendor_}"
git config --local --add efi.esp-root /boot/efi
git config --local --add efi.arches "x86_64 aarch64 %{arm} %{ix86}"

%build
%make_build SHELL=/bin/bash clean all

%install
%make_install SHELL=/bin/bash

%files -n efi-srpm-macros
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
* Wed May 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 4-6
- Fixing package build by adding an explicit BR on '/etc/os-release'.
- License verified.

* Mon Jun 07 2021 Olivia Crain <oliviacrain@microsoft.com> - 4-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Set shell to bash during make invocations, since the Makefile uses bash built-in commands 

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
