# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           efivar
Version:        39
Release: 11%{?dist}
Summary:        Tools to manage UEFI variables
License:        LGPL-2.1-only
URL:            https://github.com/rhboot/efivar
Requires:       %{name}-libs = %{version}-%{release}
ExclusiveArch:  %{efi}

BuildRequires:  gcc
BuildRequires:  efi-srpm-macros git glibc-static libabigail
BuildRequires:  make
BuildRequires:  mandoc
BuildRequires:  git
# please don't fix this to reflect github's incomprehensible url that goes
# to a different tarball.
Source0:        https://github.com/rhboot/efivar/releases/download/%{version}/efivar-%{version}.tar.bz2
Source1:        efivar.patches

# include patches
%include %{SOURCE1}

%description
efivar provides a simple command line interface to the UEFI variable facility.

%package libs
Summary: Library to manage UEFI variables

%description libs
Library to allow for the simple manipulation of UEFI variables.

%package devel
Summary: Development headers for libefivar
Requires: %{name}-libs = %{version}-%{release}

%description devel
development headers required to use libefivar.

%prep
%setup -q -n %{name}-%{version}
git init
git config user.email "%{name}-owner@fedoraproject.org"
git config user.name "Fedora Ninjas"
git add .
git commit -a -q -m "%{version} baseline."
git am %{patches} </dev/null
git config --unset user.email
git config --unset user.name

%build
# This package implements symbol versioning with toplevel ASM statments which is
# incompatible with LTO.  Disable LTO
%define _lto_cflags %{nil}

make LIBDIR=%{_libdir} BINDIR=%{_bindir} CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS"

%install
%makeinstall CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS"
install -m 0644 src/abignore %{buildroot}%{_includedir}/efivar/.abignore

%check
%ifarch x86_64
make abicheck CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS"
%endif

%ldconfig_scriptlets libs

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README.md
%{_bindir}/efivar
%{_bindir}/efisecdb
%{_mandir}/man1/*

%files devel
%{_mandir}/man3/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files libs
%license COPYING
%{_libdir}/*.so.*

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 39-9
- Update ABI XML for glibc-2.42

* Tue Jan 28 2025 Nicolas Frayer <nfrayer@redhat.com> - 39-8
- ABI: Update abixml to match glibc changes
- Resolves: #2340115

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jul 11 2024 Peter Jones <pjones@redhat.com> - 39-5
- Bump release here to keep rawhide ahead of f40

* Thu Jul 11 2024 Peter Jones <pjones@redhat.com> - 39-3
- Update our abixml files for newer libabigail

* Thu Jul 11 2024 Nicolas Frayer <nfrayer@redhat.com> - 39-2
- license: Add COPYING to efivar-lib
- Resolves: #2295838

* Wed Jan 31 2024 Peter Jones <pjones@redhat.com> - 39-1
- Update to efivar-39

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 10 2023 Robbie Harwood <rharwood@redhat.com> - 38-6
- Fix inheritance of buildflags

* Thu Jul 28 2022 Robbie Harwood <rharwood@redhat.com> - 38-5
- Fix build with glibc-2.36

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Apr 08 2022 Robbie Harwood <rharwood@redhat.com> - 38-3
- Apply fix for risxv64 (wefu)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 14 2022 Robbie Harwood <rharwood@redhat.com> - 38-1
- New upstream release (38)

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 17 2021 Javier Martinez Canillas <javierm@redhat.com> - 37-16
- Enable Intel Control-flow Enforcement Technology (CET)
  Resolves: rhbz#1808811

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Oct 27 2020 Petr Pisar <ppisar@redhat.com> - 37-14
- Fix XML ABI dumps that were generated with a faulty GCC and missed the
  variadic arguments when building without LTO (bug #1863475)

* Thu Aug 06 2020 Jeff Law <law@redhat.com>
- Remove explicit LTO bits from flags

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org>
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Jeff Law <law@redhat.com> - 37-11
- Disable LTO

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Javier Martinez Canillas <javierm@redhat.com> - 37-9
- Change License field to LGPL-2.1 to prevent rpminspect test to fail

* Wed Apr 22 2020 Hans de Goede <hdegoede@redhat.com> - 37-8
- Add a patch to fix eMMC sysfs path parsing
  Resolves: rhbz#1826864

* Mon Feb 24 2020 Peter Jones <pjones@redhat.com> - 37-7
- Package our abignore file to try to shut taskotron up some.

* Mon Feb 24 2020 Peter Jones <pjones@redhat.com> - 37-6
- Pull in a bunch of patches from upstream.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 37-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 12 2019 Peter Jones <pjones@redhat.com> - 37-4
- Update for some compiler warning fixes.
  Resolves: rhbz#1735168

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 05 2018 Peter Jones <pjones@redhat.com> - 37-1
- Update to efivar 37:
  - Minor coverity fixes
  - Improve ACPI device path formatting
  - Add support for SOC devices that use FDT as their PCI root node
  - Make devices we can't parse the "device" sysfs link for use DEV_ABBREV_ONLY
  - Handle SCSI port numbers better
  - Don't require an EUI for NVMe
  - Fix the accidental requirement on ACPI UID nodes existing
  - Add support for EMMC devices
  - Add support for PCI root nodes without a device link in sysfs
  - Add support for partitioned MD devices
  - Fix partition number detection when the number isn't provided
  - Add support for ACPI Generic Container and Embedded Controller root nodes
  - Add limited support for SAS/SATA port expanders

* Mon Sep 17 2018 Peter Jones <pjones@redhat.com> - 36-1
- Update to efivar 36
- Add NVDIMM support
- Re-written linux interface parser to handle how devices are
  partitioned better, and for cleaner code, with one file per device
  type.
- lots of verbosity updates
- better CI
- analysis with clang's analyzer as well as coverity
- Better handling of immutable bits in sysfs
- LIBEFIVAR_OPS=help
- lots of code cleanups.

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 35-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri May 04 2018 Peter Jones <pjones@redhat.com> - 35-3
- Rebuild for new efi-rpm-macros, now that it has settled down a bit.

* Tue May 01 2018 Peter Jones <pjones@redhat.com> - 35-2
- Use efi-rpm-macros instead of defining efi-related macros ourselves

* Mon Apr 09 2018 Peter Jones <pjones@redhat.com> - 35-1
- Update to efivar 35
- fixes for older compilers
- efi_get_variable_exists()
- Lots of stuff to make CI work.
- use usleep() to avoid hitting the kernel rate limiter on efivarfs
- better EFI_GUID macro
- add efi_guid_fwupdate (0abba7dc-e516-4167-bbf5-4d9d1c739416)

* Tue Feb 27 2018 Peter Jones <pjones@redhat.com> - 34-1
- Update to efivar 34, and include a patch to avoid upstream rate limiting.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Peter Robinson <pbrobinson@fedoraproject.org> 33-2
- Enable ARMv7, minor spec cleanups

* Tue Jan 23 2018 Peter Jones <pjones@redhat.com> - 33-1
- Add NVDIMM support
- Bump version to 33

* Tue Sep 12 2017 Peter Jones <pjones@redhat.com> - 32-2
- Make efi_guid_ux_capsule actually get exported right.

* Tue Sep 12 2017 Peter Jones <pjones@redhat.com> - 32-1
- efivar 32
- lots of coverity fixes; mostly leaked memory and fds and the like
- fix sysfs pci path formats
- handle device paths for dns, nfit, bluetooth, wifi, emmc, btle.
- improved abi checking on releases
- Fix failures on EDIT_WRITE in edit_variable() when the variable doesn't exist
- Add efi_guid_ux_capsule_guid to our guids
- Now with %%check

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 06 2017 Peter Jones <pjones@redhat.com> - 31-1
- Update to efivar 31
- Work around NVMe EUI sysfs change
- Provide some oldish version strings we should have kept.
- lots of overflow checking on our pointer math in dp parsing
- fix major/minor device number handling in the linux code
- Do better formatting checks for MBR partitions
- Fixes for gcc 7

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 30-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Oct 17 2016 Peter Jones <pjones@redhat.com> - 30-4
- Handle NVMe device attributes paths moving around in sysfs.

* Wed Sep 28 2016 Peter Jones <pjones@redhat.com> - 30-3
- Maybe even provide the *right* old linker deps.

* Tue Sep 27 2016 Peter Jones <pjones@redhat.com> - 30-2
- Try not to screw up SONAME stuff quite so badly.

* Tue Sep 27 2016 Peter Jones <pjones@redhat.com> - 30-1
- Fix efidp_*() functions with __pure__ that break with some optimizations
- Fix NVMe EUI parsing.

* Tue Sep 27 2016 Peter Jones <pjones@redhat.com> - 29-1
- Use -pie not -PIE in our linker config
- Fix some overflow checks for gcc < 5.x
- Make variable class probes other than the first one actually work
- Move -flto to CFLAGS
- Pack all of the efi device path headers
- Fix redundant decl of efi_guid_zero()

* Wed Aug 17 2016 Peter Jones <pjones@redhat.com> - 28-1
- Make our sonames always lib$FOO.1 , not lib$FOO.$VERSION .

* Tue Aug 16 2016 Peter Jones <pjones@redhat.com> - 27-1
- Bug fix for 086eeb17 in efivar 26.

* Wed Aug 10 2016 Peter Jones <pjones@redhat.com> - 26-1
- Update to efivar-26 .

* Thu Jun 30 2016 Peter Jones <pjones@redhat.com> - 0.24-1
- Update to 0.24

* Mon Feb 15 2016 Peter Jones <pjones@redhat.com> - 0.23-1
- Update to 0.23

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 02 2015 Peter Jones <pjones@redhat.com> - 0.21-2
- Bump the release here so f22->f23->f24 updates work.

* Mon Jul 13 2015 Peter Jones <pjones@redhat.com> - 0.21-1
- Rename "make test" so packagers don't think it's a good idea to run it
  during builds.
- Error check sizes in vars_get_variable()
- Fix some file size comparisons
- make SONAME reflect the correct values.
- Fix some uses of "const"
- Compile with -O2 by default
- Fix some strict-aliasing violations
- Fix some of the .pc files and how we do linking to work better.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 02 2015 Peter Jones <pjones@redhat.com> - 0.20-1
- Update to 0.20
- Make sure tester is build with the right link order for libraries.
- Adjust linker order for pkg-config
- Work around LocateDevicePath() not grokking PcieRoot() devices properly.
- Rectify some missing changelog entries

* Thu May 28 2015 Peter Jones <pjones@redhat.com> - 0.19-1
- Update to 0.19
- add API from efibootmgr so fwupdate and other tools can use it.

* Wed Oct 15 2014 Peter Jones <pjones@redhat.com> - 0.15-1
- Update to 0.15
- Make 32-bit builds set variables' DataSize correctly.

* Wed Oct 08 2014 Peter Jones <pjones@redhat.com> - 0.14-1
- Update to 0.14
- add efi_id_guid_to_guid() and efi_guid_to_id_guid(), which support {ID GUID}
  as a concept.
- Add some vendor specific guids to our guid list.
- Call "empty" "zero" now, as many other places do.  References to
  efi_guid_is_empty() and efi_guid_empty still exist for ABI compatibility.
- add "efivar -L" to the man page.

* Tue Oct 07 2014 Peter Jones <pjones@redhat.com> - 0.13-1
- Update to 0.13:
- add efi_symbol_to_guid()
- efi_name_to_guid() will now fall back on efi_symbol_to_guid() as a last
  resort
- "efivar -L" to list all the guids we know about
- better namespacing on libefivar.so (rename well_known_* -> efi_well_known_*)

* Thu Sep 25 2014 Peter Jones <pjones@redhat.com> - 0.12-1
- Update to 0.12

* Wed Aug 20 2014 Peter Jones <pjones@redhat.com> - 0.11-1
- Update to 0.11

* Fri May 02 2014 Peter Jones <pjones@redhat.com> - 0.10-1
- Update package to 0.10.
- Fixes a build error due to different cflags in the builders vs updstream
  makefile.

* Fri May 02 2014 Peter Jones <pjones@redhat.com> - 0.9-0.1
- Update package to 0.9.

* Tue Apr 01 2014 Peter Jones <pjones@redhat.com> - 0.8-0.1
- Update package to 0.8 as well.

* Fri Oct 25 2013 Peter Jones <pjones@redhat.com> - 0.7-1
- Update package to 0.7
- adds --append support to the binary.

* Fri Sep 06 2013 Peter Jones <pjones@redhat.com> - 0.6-1
- Update package to 0.6
- fixes to documentation from lersek
- more validation of uefi guids
- use .xz for archives

* Thu Sep 05 2013 Peter Jones <pjones@redhat.com> - 0.5-0.1
- Update to 0.5

* Mon Jun 17 2013 Peter Jones <pjones@redhat.com> - 0.4-0.2
- Fix ldconfig invocation

* Mon Jun 17 2013 Peter Jones <pjones@redhat.com> - 0.4-0.1
- Initial spec file
