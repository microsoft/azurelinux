# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define efivar_version 35-2

Name: efibootmgr
Version: 18
Release: 11%{?dist}
Summary: EFI Boot Manager
License: GPL-2.0-or-later
URL: https://github.com/rhboot/%{name}/

BuildRequires: efi-srpm-macros >= 3-2
BuildRequires: efi-filesystem
BuildRequires: git popt-devel
BuildRequires: efivar-libs >= %{efivar_version}
BuildRequires: efivar-devel >= %{efivar_version}
BuildRequires: gcc
BuildRequires: make
Requires: efi-filesystem
ExclusiveArch: %{efi}

Source0: https://github.com/rhboot/%{name}/releases/download/%{name}-%{version}/%{name}-%{version}.tar.bz2
Source1: efibootmgr.patches

%include %{SOURCE1}

%description
%{name} displays and allows the user to edit the Intel Extensible
Firmware Interface (EFI) Boot Manager variables.  Additional
information about EFI can be found at https://uefi.org/.

%prep
%autosetup -S git
git config --local --add efibootmgr.efidir %{efi_vendor}

%build
%make_build CFLAGS='%{optflags}' LDFLAGS='%{build_ldflags}'

%install
%make_install libdir=%{_libdir} \
              bindir=%{_bindir} \
              sbindir=%{_sbindir} \
              mandir=%{_mandir} \
	      localedir=%{_datadir}/locale/ \
              includedir=%{_includedir} \
	      libexecdir=%{_libexecdir} \
              datadir=%{_datadir}

%files
%license COPYING
%{_sbindir}/*
%{_mandir}/*/*.?.gz
%doc README

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 12 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl>
- Rebuilt for the bin-sbin merge (2nd attempt)

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Dec 13 2023 Nicolas Frayer <nfrayer@redhat.com>
- Migrate to SPDX license
- Please refer to https://fedoraproject.org/wiki/Changes/SPDX_Licenses_Phase_2

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 07 2022 Robbie Harwood <rharwood@redhat.com> - 18-1
- New upstream version (18)

* Tue Jul 05 2022 Robbie Harwood <rharwood@redhat.com> - 17-1
- New upstream version (17)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 16-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 16-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 16-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Aug 06 2020 Merlin Mathesius <mmathesi@redhat.com> - 16-9
- FTBFS fixes for Rawhide and ELN

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 16-9
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 16-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri May 04 2018 Peter Jones <pjones@redhat.com> - 16-3
- Rebuild for new efi-rpm-macros, now that it has settled down a bit.

* Wed May 02 2018 Peter Jones <pjones@redhat.com> - 16-2
- Use %%{efi} and similar macros from efi-rpm-macros
- Use '%%autosetup -S git' now that it imports patches without rewriting
  the commit message.
- Fix some URLs maybe.

* Mon Apr 09 2018 Peter Jones <pjones@redhat.com> - 16-1
- efibootmgr 16
- better coverity and clang-analyzer support
- better CI
- minor fixes

* Tue Feb 27 2018 Peter Jones <pjones@redhat.com> - 15-6
- Rebuild against newer efivar.

* Fri Feb 23 2018 Florian Weimer <fweimer@redhat.com> - 15-5
- Use CFLAGS & LDFLAGS from redhat-rpm-config

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 08 2017 Peter Jones <pjones@redhat.com> - 15-1
- Update to efibootmgr 15
- Make efibootmgr use EFIDIR / efibootmgr.efidir like fwupdate does
- make --loader default build-time configurable
- sanitize set_mirror()/get_mirror()
- Add support for parsing loader options as UCS2
- GCC 7 fixes
- Don't use -fshort-wchar since we don't run on EFI machines.
- Also rebuild for efivar-31-1.fc26 to get symbol versioning right.
  Resolves: rhbz#1468841

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Sep 28 2016 Peter Jones <pjones@redhat.com> - 14-3
- Rebuild for efivar-30-3, this time with the right library sonames.

* Wed Sep 28 2016 Peter Jones <pjones@redhat.com> - 14-2
- Rebuild for efivar-30-2

* Tue Sep 27 2016 Peter Jones <pjones@redhat.com> - 14-1
- Update to efibootmgr 14
- Remove "(hex)" from description of --delete-bootnum
- Fix a typo in the popt options
- Add README.md
- make efibootdump install by default
- Man page fixes
- Better compiler detection
- Don't use --default-symver in efibootmgr
- Make -flto part of the overrideable CFLAGS

* Wed Aug 17 2016 Peter Jones <pjones@redhat.com> - 13-2
- Update to efibootmgr 13
- Add support for --sysprep and --driver to support UEFI System Prep
  Applications and UEFI Drivers.
- use efivar's error reporting facility, and show error traces when
  "-v -v" is used.
- Still yet better error codes returned on failures.
- Add -m and -M to support Memory Address Range Mirroring.
- Add efibootdump, to examine Boot* variables found in tarballs in bug
  reports and similar.
- miscellaneous bugfixes.

* Thu Aug 11 2016 Peter Jones <pjones@redhat.com> - 13-1
- Update to version 13
- add efibootdump
- use efivar's error reporting facility
- Add address range mirroring support
- lots of bug fixes

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 28 2015 Peter Jones <pjones@redhat.com> - 0.12-1
- Update to 0.12
- use libefiboot and libefivar to make device paths and load options
- don't depend on -lz or -lpci any more

* Tue Oct 21 2014 Peter Jones <pjones@redhat.com> - 0.11.0-1
- Fix "-n" and friends not being assigned/checked right sometimes from 0.10.0-1
- Generate more archives to avoid people using github's, because they're just
  bad.

* Mon Oct 20 2014 Peter Jones <pjones@redhat.com> - 0.10.0-1
- Make -o parameter validation work better and be more informative
- Better exit values
- Fix a segfault with appending ascii arguments.

* Tue Sep 09 2014 Peter Jones <pjones@redhat.com> - 0.8.0-1
- Release 0.8.0

* Mon Jan 13 2014 Peter Jones <pjones@redhat.com> - 0.6.1-1
- Release 0.6.1

* Mon Jan 13 2014 Jared Dominguez <Jared_Dominguez@dell.com>
- new home https://github.com/vathpela/efibootmgr

* Thu Jan  3 2008 Matt Domsch <Matt_Domsch@dell.com> 0.5.4-1
- split efibootmgr into its own RPM for Fedora/RHEL.

* Tue Aug 24 2004 Matt Domsch <Matt_Domsch@dell.com>
- new home linux.dell.com

* Fri May 18 2001 Matt Domsch <Matt_Domsch@dell.com>
- See doc/ChangeLog
