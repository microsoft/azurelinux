# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: DWARF optimization and duplicate removal tool
Name: dwz
Version: 0.16
Release: 2%{?dist}
License: GPL-3.0-or-later AND (GPL-3.0-or-later WITH GCC-exception-3.1) AND GPL-2.0-or-later AND (GPL-2.0-or-later WITH GCC-exception-2.0) AND LGPL-2.0-or-later
URL: https://sourceware.org/dwz/
Source: https://sourceware.org/ftp/dwz/releases/%{name}-%{version}.tar.xz
BuildRequires: gcc, gcc-c++, gdb, elfutils-libelf-devel, dejagnu
# dwz builds with XXH_INLINE_ALL, so depend on (virtual) xxhash-static
BuildRequires: make elfutils xxhash-devel xxhash-static

# Patches

%description
The dwz package contains a program that attempts to optimize DWARF
debugging information contained in ELF shared libraries and ELF executables
for size, by replacing DWARF information representation with equivalent
smaller representation where possible and by reducing the amount of
duplication using techniques from DWARF standard appendix E - creating
DW_TAG_partial_unit compilation units (CUs) for duplicated information
and using DW_TAG_imported_unit to import it into each CU that needs it.

%prep
%autosetup -p1 -n dwz

%build
%make_build CFLAGS='%{optflags}' LDFLAGS='%{build_ldflags}' \
  prefix=%{_prefix} mandir=%{_mandir} bindir=%{_bindir}

%install
rm -rf %{buildroot}
%make_install prefix=%{_prefix} mandir=%{_mandir} bindir=%{_bindir}

%check
CFLAGS="" LDFLAGS="" srcdir=$(pwd) make check

%files
%license COPYING COPYING3 COPYING.RUNTIME
%{_bindir}/dwz
%{_mandir}/man1/dwz.1*

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 10 2025 Mark Wielaard <mjw@fedoraproject.org> - 0.16-1
- Update to upstream dwz 0.16
- Drop dwz-0.15-index9.patch
- Add srcdir=$(pwd) for make check

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Oct 7 2024 Mark Wielaard <mjw@fedoraproject.org> - 0.15-8
- Add dwz-0.15-index9.patch

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Feb  1 2024 Siddhesh Poyarekar <siddhesh@redhat.com> - 0.15-6
- Bump release for SPDX change.

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Nov   3 2022 Mark Wielaard <mjw@fedoraproject.org> 0.15-1
- update to a new upstream release

* Tue Oct  25 2022 Mark Wielaard <mjw@fedoraproject.org> 0.14-9
- Add dwz-0.14-grep-E.patch

* Tue Oct  25 2022 William Cohen <wcohen@redhat.com> 0.14-8
- Added URL and complete path to source tarball to dwz.spec.

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul  1 2022 Mark Wielaard <mjw@fedoraproject.org> 0.14-6
- Add dwz-0.14-gdb-add-index.patch

* Wed Jun 29 2022 Mark Wielaard <mjw@fedoraproject.org> 0.14-5
- Add dwz-0.14-binutils-readelf-alt.patch
- BuildRequires elfutils (for tests)

* Sun Jun 26 2022 Mark Wielaard <mjw@fedoraproject.org> 0.14-4
- Add dwz-0.14-binutils-Wn.patch

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 09 2021 Jakub Jelinek <jakub@redhat.com> 0.14-1
- update to a new upstream release

* Fri Jan 22 2021 Mark Wielaard <mjw@fedoraproject.org> 0.13-7
- Don't crash on DWARF5 .debug_line table with zero files (#1919243)

* Thu Jan 21 2021 Jakub Jelinek <jakub@redhat.com> 0.13-6
- DW_FORM_implicit_const handling fixes (sw#27212, sw#27213)
- temporarily build odr tests with -gdwarf-4 as they are incompatible with
  DWARF 5

* Mon Jan 18 2021 Jakub Jelinek <jakub@redhat.com> 0.13-5
- update to latest git snapshot
  - DWARF5 support

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 0.13-3
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Dec 11 2019 Jakub Jelinek <jakub@redhat.com> 0.13-1
- update to a new upstream release
- add make check

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 19 2018 Marek Polacek <polacek@redhat.com> 0.12-9
- remove %{?_isa} from BuildRequires (#1545173)
- add gcc to BuildRequires

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 23 2018 Florian Weimer <fweimer@redhat.com> - 0.12-7
- Use LDFLAGS from redhat-rpm-config

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Feb 01 2017 Stephen Gallagher <sgallagh@redhat.com> - 0.12-3
- Add missing %%license macro

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jul 13 2015 Jakub Jelinek <jakub@redhat.com> 0.12-1
- fix up alignment of moved non-allocated sections and section header table

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.11-5
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul  2 2013 Jakub Jelinek <jakub@redhat.com> 0.11-1
- handle .gdb_index version 8 (#969454)

* Mon Mar 11 2013 Jakub Jelinek <jakub@redhat.com> 0.10-1
- when creating DW_AT_stmt_list, use DW_FORM_sec_offset for dwarf4
  and DW_FORM_data4 for dwarf[23] rather than vice versa (#919755)

* Mon Feb  4 2013 Jakub Jelinek <jakub@redhat.com> 0.9-1
- fix up handling of DIE equality if more than one DIE in the same
  CU compare equal (#889283)
- check DW_FORM_ref_addr properly during fi_multifile phase

* Thu Nov 29 2012 Jakub Jelinek <jakub@redhat.com> 0.8-1
- fix recompute_abbrevs (#880634)
- optimize DW_FORM_data[48] DW_AT_high_pc that GCC 4.8 produces

* Fri Aug 10 2012 Jakub Jelinek <jakub@redhat.com> 0.7-1
- fix iterative hasing on big-endian targets (#846685)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Jakub Jelinek <jakub@redhat.com> 0.6-1
- add --version/-v option support (Matt Newsome)
- fix building on RHEL 5

* Wed Jul  4 2012 Jakub Jelinek <jakub@redhat.com> 0.5-1
- handle .gdb_index version 7

* Fri Jun 22 2012 Jakub Jelinek <jakub@redhat.com> 0.4-1
- fix up DIE counting in low-mem mode for testing the -L limit

* Fri Jun 15 2012 Jakub Jelinek <jakub@redhat.com> 0.3-1
- update to dwz-0.3 (#830863)

* Mon Jun 11 2012 Jakub Jelinek <jakub@redhat.com> 0.2-1
- new package
