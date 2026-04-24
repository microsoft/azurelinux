# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: debugedit
Version: 5.2
Release: 4%{?dist}
Summary: Tools and scripts for creating debuginfo and source file distributions, collect build-ids and rewrite source paths in DWARF data for debugging, tracing and profiling.
License: GPL-3.0-or-later AND GPL-2.0-or-later AND LGPL-2.0-or-later
URL: https://sourceware.org/debugedit/
Source0: https://sourceware.org/pub/debugedit/%{version}/%{name}-%{version}.tar.xz
Source1: https://sourceware.org/pub/debugedit/%{version}/%{name}-%{version}.tar.xz.sig
Source2: gpgkey-5C1D1AA44BE649DE760A.gpg

BuildRequires: make gcc
BuildRequires: pkgconfig(libelf)
BuildRequires: pkgconfig(libdw)
BuildRequires: help2man
BuildRequires: gnupg2

# For configure checking -j support
BuildRequires: dwz

# For debugedit build-id recomputation
BuildRequires: xxhash-devel
# debugedit builds with XXH_INLINE_ALL, so depend on (virtual) xxhash-static
BuildRequires: xxhash-static

# For the testsuite.
BuildRequires: autoconf
BuildRequires: automake

# The find-debuginfo.sh script has a couple of tools it needs at runtime.
# For strip_to_debug, eu-strip
Requires: elfutils
# For ar, add_minidebug, readelf, awk, nm, sort, comm, objcopy, xz
Requires: binutils, gawk, coreutils, xz
# For find and xargs
Requires: findutils
# For do_file, gdb_add_index
# We only need gdb-add-index, so suggest gdb-minimal (full gdb is also ok)
Requires: /usr/bin/gdb-add-index
Suggests: gdb-minimal
# For run_job, sed
Requires: sed
# For dwz
Requires: dwz
# For append_uniq, grep
Requires: grep

%global _hardened_build 1

Patch1: 0001-Add-debugedit-classify-ar-and-use-it-before-running-.patch

%description
The debugedit project provides programs and scripts for creating
debuginfo and source file distributions, collect build-ids and rewrite
source paths in DWARF data for debugging, tracing and profiling.

It is based on code originally from the rpm project plus libiberty and
binutils.  It depends on the elfutils libelf and libdw libraries to
read and write ELF files, DWARF data and build-ids.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1

%build
autoreconf -f -v -i
%configure
%make_build

%install
%make_install
# Temp symlink to make sure things don't break.
cd %{buildroot}%{_bindir}
ln -s find-debuginfo find-debuginfo.sh

%check
# The testsuite should be zero fail.
make check %{?_smp_mflags}

%files
%license COPYING COPYING3 COPYING.LIB
%doc README
%{_bindir}/debugedit
%{_bindir}/sepdebugcrcfix
%{_bindir}/debugedit-classify-ar
%{_bindir}/find-debuginfo
%{_bindir}/find-debuginfo.sh
%{_mandir}/man1/debugedit.1*
%{_mandir}/man1/sepdebugcrcfix.1*
%{_mandir}/man1/debugedit-classify-ar.1*
%{_mandir}/man1/find-debuginfo.1*

%changelog
* Fri Aug 29 2025 Mark Wielaard <mjw@fedoraproject.org> - 5.2-3
- Add 0001-Add-debugedit-classify-ar-and-use-it-before-running-.patch
- Install debugedit-classify-ar and man page

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul  7 2025 Mark Wielaard <mjw@fedoraproject.org> - 5.2-1
- New upstream 5.2 release
- Drop all local patches

* Fri Jun 20 2025 Mark Wielaard <mjw@fedoraproject.org> - 5.1-7
- Add 0001-Add-basic-find-debuginfo-script-tests.patch

* Tue Apr  8 2025 Mark Wielaard <mjw@fedoraproject.org> - 5.1-6
- Add 0001-debugedit-Handle-unused-.debug_str_offsets-entries.patch

* Wed Feb 26 2025 Mark Wielaard <mjw@fedoraproject.org> - 5.1-5
- Add debugedit-5.1-binutils-tools-override.patch

* Thu Jan 16 2025 Mark Wielaard <mjw@fedoraproject.org> - 5.1-4
- 0001-find-debuginfo-Make-return-from-do_file-explicit.patch

* Thu Jan 16 2025 Mark Wielaard <mjw@fedoraproject.org> - 5.1-3
- Add 0001-find-debuginfo-Fix-skip_mini-.gnu_debugdata-handling.patch

* Thu Nov 28 2024 Mark Wielaard <mjw@fedoraproject.org> - 5.1-2
- Add 0001-find-debuginfo-Check-files-are-writable-before-modif.patch

* Tue Oct 29 2024 Mark Wielaard <mjw@fedoraproject.org> - 5.1-1
- New upstream 5.1 release
- Drop all local patches

* Mon Oct 7 2024 Mark Wielaard <mjw@fedoraproject.org> - 5.0-18
- Add debugedit-5.0-DW_UT_type.patch

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun May 19 2024 Mark Wielaard <mjw@fedoraproject.org> - 5.0-16
- Add relocation, debug_str_offsets and macro fixes:
  0001-Make-relocation-reading-explicit.patch
  0002-Simplify-update_rela_data-by-checking-rel_updated.patch
  0003-debug_str_offsets-header-version-and-padding-are-2-b.patch
  0004-debugedit-Track-active-CU.patch
  0005-debugedit-Handle-DW_MACRO_-define-undef-_strx.patch

* Mon Apr 29 2024 Mark Wielaard <mjw@fedoraproject.org> - 5.0-15
- Add debugedit-5.0-do_read_32_binary-search.patch

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec  4 2023 Mark Wielaard <mjw@fedoraproject.org> - 5.0-12
- Add 0001-debugedit-Add-support-for-.debug_str_offsets-DW_FORM.patch

* Fri Nov 17 2023 Mark Wirlaard <mjw@fedoraproject.org> - 5.0-11
- migrated to SPDX license

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 30 2023 Mark Wielaard <mjw@fedoraproject.org> - 5.0-9
- Add 0001-find-debuginfo-Add-v-verbose-for-per-file-messages.patch

* Fri Jun 30 2023 Mark Wielaard <mjw@fedoraproject.org> - 5.0-8
- Add 0001-find-debuginfo-Prefix-install_dir-to-PATH.patch

* Fri Jan 27 2023 Mark Wielaard <mjw@fedoraproject.org> - 5.0-7
- Refresh 0001-tests-Handle-zero-directory-entry-in-.debug_line-DWA.patch
- Add new upstream patches:
  0001-use-READELF-not-readelf.patch
  0001-find-debuginfo-Pass-j-down-to-dwz.patch
  0002-configure.ac-Use-AC_LINK_IFELSE-for-gz-none-check.patch
  0003-configure.ac-Use-AC_LANG_PROGRAM-for-AC_LINK_IFELSE-.patch
  0004-scripts-find-debuginfo.in-Add-q-quiet.patch

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 10 2022 Romanos Skiadas <rom.skiad@gmail.com> - 5.0-4
- Remove CFLAGS/LDFLAGS sed as they are already set to "" by debugedit

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 30 2021 Mark Wielaard <mjw@fedoraproject.org> - 5.0-2
- Add testsuite fix for GCC 11.2.1

* Mon Jul 26 2021 Mark Wielaard <mjw@fedoraproject.org> - 5.0-1
- Upgrade to upstream 5.0 release.

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 17 2021 Mark Wielaard <mjw@fedoraproject.org> - 0.3-1
- Update to upstream 0.3 pre-release. Removes find-debuginfo .sh suffix.
  - This release still has a find-debuginfo.sh -> find-debuginfo symlink.

* Wed May  5 2021 Mark Wielaard <mjw@fedoraproject.org> - 0.2-1
- Update to upstream 0.2 pre-release. Adds documentation.

* Wed Apr 28 2021 Mark Wielaard <mjw@fedoraproject.org> - 0.1-5
- Add dist to Release. Use file dependency for /usr/bin/gdb-add-index.

* Tue Apr 27 2021 Mark Wielaard <mjw@fedoraproject.org> - 0.1-4
- Use numbered Sources and https.

* Mon Apr 26 2021 Mark Wielaard <mjw@fedoraproject.org> - 0.1-3
- Fix some rpmlint issues, add comments, add license and doc,
  gpg verification, use pkgconfig BuildRequires, enable _hardened_build

* Mon Mar 29 2021 Panu Matilainen <pmatilai@redhat.com>
- Add pile of missing runtime utility dependencies

* Tue Mar 23 2021 Panu Matilainen <pmatilai@redhat.com>
- Initial packaging
