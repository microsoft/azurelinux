# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global run_testsuite 1
%global mingw_build_ucrt64 1
%define enable_new_dtags 0

Name:           mingw-binutils
Version:        2.45.1
Release: 2%{?dist}
Summary:        Cross-compiled version of binutils for Win32 and Win64 environments

License:        GPL-3.0-or-later AND (GPL-3.0-or-later WITH Bison-exception-2.2) AND (LGPL-2.0-or-later WITH GCC-exception-2.0) AND BSD-3-Clause AND GFDL-1.3-or-later AND GPL-2.0-or-later AND LGPL-2.1-or-later AND LGPL-2.0-or-later

URL:            http://www.gnu.org/software/binutils/
Source0:        https://ftp.gnu.org/gnu/binutils/binutils-%{version}.tar.xz

### Patches from native package
# Purpose:  Use /lib64 and /usr/lib64 instead of /lib and /usr/lib in the
#           default library search path of 64-bit targets.
# Lifetime: Permanent, but it should not be.  This is a bug in the libtool
#           sources used in both binutils and gcc, (specifically the
#           libtool.m4 file).  These are based on a version released in 2009
#           (2.2.6?) rather than the latest version.  (Definitely fixed in
#           libtool version 2.4.6).
# Not needed, mingw does not have lib64
# Patch01: binutils-libtool-lib64.patch

# Purpose:  Appends a RHEL or Fedora release string to the generic binutils
#           version string.
# Lifetime: Permanent.  This is a RHEL/Fedora specific patch.
Patch02: binutils-version.patch

# Purpose:  Exports the demangle.h header file (associated with the libiberty
#           sources) with the binutils-devel rpm.
# Lifetime: Permanent.  This is a RHEL/Fedora specific patch.
Patch03: binutils-export-demangle.h.patch

# Purpose:  Disables the check in the BFD library's bfd.h header file that
#           config.h has been included before the bfd.h header.  See BZ
#           #845084 for more details.
# Lifetime: Permanent - but it should not be.  The bfd.h header defines
#           various types that are dependent upon configuration options, so
#           the order of inclusion is important.
# FIXME:    It would be better if the packages using the bfd.h header were
#           fixed so that they do include the header files in the correct
#           order.
Patch04: binutils-no-config-h-check.patch

# Purpose:  Disable an x86/x86_64 optimization that moves functions from the
#           PLT into the GOTPLT for faster access.  This optimization is
#           problematic for tools that want to intercept PLT entries, such
#           as ltrace and LD_AUDIT.  See BZs 1452111 and 1333481.
# Lifetime: Permanent.  But it should not be.
# FIXME:    Replace with a configure time option.
Patch05: binutils-revert-PLT-elision.patch

# Purpose:  Do not create PLT entries for AARCH64 IFUNC symbols referenced in
#           debug sections.
# Lifetime: Permanent.
# FIXME:    Find related bug.  Decide on permanency.
Patch06: binutils-2.27-aarch64-ifunc.patch

# Purpose:  Stop the binutils from statically linking with libstdc++.
# Lifetime: Permanent.
Patch07: binutils-do-not-link-with-static-libstdc++.patch

# Purpose:  Stop gold from aborting when input sections with the same name
#            have different flags.
# Lifetime: Fixed in 2.43 (maybe)
# Patch08: binutils-gold-mismatched-section-flags.patch

# Purpose:  Change the gold configuration script to only warn about
#            unsupported targets.  This allows the binutils to be built with
#            BPF support enabled.
# Lifetime: Permanent.
# Patch09: binutils-gold-warn-unsupported.patch

# Purpose:  Enable the creation of .note.gnu.property sections by the GOLD
#            linker for x86 binaries.
# Lifetime: Permanent.
# Patch10: binutils-gold-i386-gnu-property-notes.patch

# Purpose:  Allow the binutils to be configured with any (recent) version of
#            autoconf.
# Lifetime: Fixed in 2.44 (maybe ?)
Patch11: binutils-autoconf-version.patch

# Purpose:  Stop libtool from inserting useless runpaths into binaries.
# Lifetime: Who knows.
Patch12: binutils-libtool-no-rpath.patch

# Purpose:  Stop an abort when using dwp to process a file with no dwo links.
# Lifetime: Fixed in 2.44 (maybe)
# Patch13: binutils-gold-empty-dwp.patch

# Purpose:  Fix binutils testsuite failures.
# Lifetime: Permanent, but varies with each rebase.
Patch14: binutils-testsuite-fixes.patch

# Purpose:  Fix binutils testsuite failures for the RISCV-64 target.
# Lifetime: Permanent, but varies with each rebase.
Patch15: binutils-riscv-testsuite-fixes.patch

# Purpose:  Make the GOLD linker ignore the "-z pack-relative-relocs" command line option.
# Lifetime: Fixed in 2.44 (maybe)
# Patch16: binutils-gold-pack-relative-relocs.patch

# Purpose:  Let the gold lihnker ignore --error-execstack and --error-rwx-segments.
# Lifetime: Fixed in 2.44 (maybe)
# Patch17: binutils-gold-ignore-execstack-error.patch

# Purpose:  Fix the ar test of non-deterministic archives.
# Lifetime: Fixed in 2.44
Patch18: binutils-fix-ar-test.patch

# Purpose:  Fix a seg fault in the AArch64 linker when building u-boot.
# Lifetime: Fixed in 2.45
Patch19: binutils-aarch64-small-plt0.patch

# Backport fix for CVE-2025-11494
# https://sourceware.org/cgit/binutils-gdb/patch/?id=b6ac5a8a5b82f0ae6a4642c8d7149b325f4cc60a
Patch20:         CVE-2025-11494.patch
# Backport fix for CVE-2025-11495
# https://sourceware.org/cgit/binutils-gdb/patch/?id=6b21c8b2ecfef5c95142cbc2c32f185cb1c26ab0
Patch21:         CVE-2025-11495.patch
# Backport fix for CVE-2025-11082
# https://sourceware.org/cgit/binutils-gdb/patch/?id=ea1a0737c7692737a644af0486b71e4a392cbca8
Patch22:         CVE-2025-11082.patch
# Backport fix CVE-2025-11081
# https://sourceware.org/cgit/binutils-gdb/patch/?id=f87a66db645caf8cc0e6fc87b0c28c78a38af59b
Patch23:         CVE-2025-11081.patch
# Backport fix for CVE-2025-11083
# https://sourceware.org/cgit/binutils-gdb/patch/?id=9ca499644a21ceb3f946d1c179c38a83be084490
Patch24:         CVE-2025-11083.patch


BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  texinfo
BuildRequires:  zlib-devel
BuildRequires:  mingw32-filesystem
BuildRequires:  mingw64-filesystem
BuildRequires:  ucrt64-filesystem
%if %{run_testsuite}
BuildRequires:  dejagnu
BuildRequires:  sharutils
%endif
Provides:       bundled(libiberty)


%description
Cross compiled binutils (utilities like 'strip', 'as', 'ld') which
understand Windows executables and DLLs.

%package -n mingw-binutils-generic
Summary:        Utilities which are needed for both the Win32 and Win64 toolchains

%description -n mingw-binutils-generic
Utilities (like strip and objdump) which are needed for
both the Win32 and Win64 toolchains

%package -n mingw32-binutils
Summary:        Cross-compiled version of binutils for the Win32 environment
Requires:       mingw-binutils-generic = %{version}-%{release}

# NB: This must be left in.
Requires:       mingw32-filesystem >= 95

%description -n mingw32-binutils
Cross compiled binutils (utilities like 'strip', 'as', 'ld') which
understand Windows executables and DLLs.

%package -n mingw64-binutils
Summary:        Cross-compiled version of binutils for the Win64 environment
Requires:       mingw-binutils-generic = %{version}-%{release}

# NB: This must be left in.
Requires:       mingw64-filesystem >= 95

%description -n mingw64-binutils
Cross compiled binutils (utilities like 'strip', 'as', 'ld') which
understand Windows executables and DLLs.

%package -n ucrt64-binutils
Summary:        Cross-compiled version of binutils for the Win64 environment
Requires:       mingw-binutils-generic = %{version}-%{release}

# NB: This must be left in.
Requires:       ucrt64-filesystem >= 133

%description -n ucrt64-binutils
Cross compiled binutils (utilities like 'strip', 'as', 'ld') which
understand Windows executables and DLLs.


%prep
%autosetup -p1 -n binutils-%{version}

# See Patch02
sed -i -e 's/%''{release}/%{release}/g' bfd/Makefile{.am,.in}


%build
# We call configure directly rather than via macros, thus if
# we are using LTO, we have to manually fix the broken configure
# scripts
[ %{_lto_cflags}x != x ] && %{_fix_broken_configure_for_lto}


mkdir build_win32
pushd build_win32
CFLAGS="%{optflags}" \
../configure \
  --build=%_build --host=%_host \
  --target=%{mingw32_target} \
  --disable-nls \
  --with-sysroot=%{mingw32_sysroot} \
  --prefix=%{_prefix} \
  --bindir=%{_bindir} \
  --includedir=%{_includedir} \
  --libdir=%{_libdir} \
  --mandir=%{_mandir} \
  --infodir=%{_infodir}

%make_build
popd

mkdir build_win64
pushd build_win64
CFLAGS="%{optflags}" \
../configure \
  --build=%_build --host=%_host \
  --target=%{mingw64_target} \
  --disable-nls \
  --with-sysroot=%{mingw64_sysroot} \
  --prefix=%{_prefix} \
  --bindir=%{_bindir} \
  --includedir=%{_includedir} \
  --libdir=%{_libdir} \
  --mandir=%{_mandir} \
  --infodir=%{_infodir}

%make_build
popd

mkdir build_ucrt64
pushd build_ucrt64
CFLAGS="%{optflags}" \
../configure \
  --build=%_build --host=%_host \
  --target=%{ucrt64_target} \
  --disable-nls \
  --with-sysroot=%{ucrt64_sysroot} \
  --prefix=%{_prefix} \
  --bindir=%{_bindir} \
  --includedir=%{_includedir} \
  --libdir=%{_libdir} \
  --mandir=%{_mandir} \
  --infodir=%{_infodir}

%make_build
popd

# Create multilib versions for the tools strip, objdump nm, and objcopy
mkdir build_multilib
pushd build_multilib
CFLAGS="%{optflags}" \
../configure \
  --build=%_build --host=%_host \
  --target=%{mingw64_target} \
  --enable-targets=%{mingw64_target},%{mingw32_target},%{ucrt64_target} \
  --disable-nls \
  --with-sysroot=%{mingw64_sysroot} \
  --prefix=%{_prefix} \
  --bindir=%{_bindir} \
  --includedir=%{_includedir} \
  --libdir=%{_libdir} \
  --mandir=%{_mandir} \
  --infodir=%{_infodir}

%make_build
popd


%check
%if !%{run_testsuite}
echo ====================TESTSUITE DISABLED=========================
%else
pushd build_win32
  make -k check < /dev/null || :
  echo ====================TESTING WIN32 =========================
  cat {gas/testsuite/gas,ld/ld,binutils/binutils}.sum
  echo ====================TESTING WIN32 END=====================
  for file in {gas/testsuite/gas,ld/ld,binutils/binutils}.{sum,log}
  do
    ln $file binutils-%{mingw32_target}-$(basename $file) || :
  done
  tar cjf binutils-%{mingw32_target}.tar.bz2 binutils-%{mingw32_target}-*.{sum,log}
  uuencode binutils-%{mingw32_target}.tar.bz2 binutils-%{mingw32_target}.tar.bz2
  rm -f binutils-%{mingw32_target}.tar.bz2 binutils-%{mingw32_target}-*.{sum,log}
popd

pushd build_win64
  make -k check < /dev/null || :
  echo ====================TESTING WIN64 =========================
  cat {gas/testsuite/gas,ld/ld,binutils/binutils}.sum
  echo ====================TESTING WIN64 END=====================
  for file in {gas/testsuite/gas,ld/ld,binutils/binutils}.{sum,log}
  do
    ln $file binutils-%{mingw64_target}-$(basename $file) || :
  done
  tar cjf binutils-%{mingw64_target}.tar.bz2 binutils-%{mingw64_target}-*.{sum,log}
  uuencode binutils-%{mingw64_target}.tar.bz2 binutils-%{mingw64_target}.tar.bz2
  rm -f binutils-%{mingw64_target}.tar.bz2 binutils-%{mingw64_target}-*.{sum,log}
popd

pushd build_ucrt64
  make -k check < /dev/null || :
  echo ====================TESTING UCRT64 =========================
  cat {gas/testsuite/gas,ld/ld,binutils/binutils}.sum
  echo ====================TESTING UCRT64 END=====================
  for file in {gas/testsuite/gas,ld/ld,binutils/binutils}.{sum,log}
  do
    ln $file binutils-%{ucrt64_target}-$(basename $file) || :
  done
  tar cjf binutils-%{ucrt64_target}.tar.bz2 binutils-%{ucrt64_target}-*.{sum,log}
  uuencode binutils-%{ucrt64_target}.tar.bz2 binutils-%{ucrt64_target}.tar.bz2
  rm -f binutils-%{ucrt64_target}.tar.bz2 binutils-%{ucrt64_target}-*.{sum,log}
popd
%endif


%install
%mingw_make_install
make -C build_multilib DESTDIR=%{buildroot}/multilib install

# These files conflict with ordinary binutils.
rm -rf %{buildroot}%{_infodir}
rm -f %{buildroot}%{_libdir}/libiberty*
rm -f %{buildroot}%{_libdir}/bfd-plugins/libdep.so

# Keep the multilib versions of the strip, objdump and objcopy commands
# We need these for the RPM integration as these tools must be able to
# both process win32 and win64 binaries
mv %{buildroot}/multilib%{_bindir}/%{mingw64_strip} %{buildroot}%{_bindir}/%{mingw_strip}
mv %{buildroot}/multilib%{_bindir}/%{mingw64_objdump} %{buildroot}%{_bindir}/%{mingw_objdump}
mv %{buildroot}/multilib%{_bindir}/%{mingw64_objcopy} %{buildroot}%{_bindir}/%{mingw_objcopy}
mv %{buildroot}/multilib%{_bindir}/%{mingw64_nm} %{buildroot}%{_bindir}/%{mingw_nm}
rm -rf %{buildroot}/multilib

# Drop man pages, they are a duplicate of those of the native tools
rm -rf %{buildroot}%{_mandir}/man1/*


%files -n mingw-binutils-generic
%license COPYING
%{_bindir}/%{mingw_strip}
%{_bindir}/%{mingw_objdump}
%{_bindir}/%{mingw_objcopy}
%{_bindir}/%{mingw_nm}

%files -n mingw32-binutils
%{_bindir}/%{mingw32_target}-addr2line
%{_bindir}/%{mingw32_target}-ar
%{_bindir}/%{mingw32_target}-as
%{_bindir}/%{mingw32_target}-c++filt
%{_bindir}/%{mingw32_target}-dlltool
%{_bindir}/%{mingw32_target}-dllwrap
%{_bindir}/%{mingw32_target}-elfedit
%{_bindir}/%{mingw32_target}-gprof
%{_bindir}/%{mingw32_target}-ld
%{_bindir}/%{mingw32_target}-ld.bfd
%{_bindir}/%{mingw32_target}-nm
%{_bindir}/%{mingw32_target}-objcopy
%{_bindir}/%{mingw32_target}-objdump
%{_bindir}/%{mingw32_target}-ranlib
%{_bindir}/%{mingw32_target}-readelf
%{_bindir}/%{mingw32_target}-size
%{_bindir}/%{mingw32_target}-strings
%{_bindir}/%{mingw32_target}-strip
%{_bindir}/%{mingw32_target}-windmc
%{_bindir}/%{mingw32_target}-windres
%{_prefix}/%{mingw32_target}/bin/ar
%{_prefix}/%{mingw32_target}/bin/as
%{_prefix}/%{mingw32_target}/bin/dlltool
%{_prefix}/%{mingw32_target}/bin/ld
%{_prefix}/%{mingw32_target}/bin/ld.bfd
%{_prefix}/%{mingw32_target}/bin/nm
%{_prefix}/%{mingw32_target}/bin/objcopy
%{_prefix}/%{mingw32_target}/bin/objdump
%{_prefix}/%{mingw32_target}/bin/ranlib
%{_prefix}/%{mingw32_target}/bin/readelf
%{_prefix}/%{mingw32_target}/bin/strip
%{_prefix}/%{mingw32_target}/lib/ldscripts

%files -n mingw64-binutils
%{_bindir}/%{mingw64_target}-addr2line
%{_bindir}/%{mingw64_target}-ar
%{_bindir}/%{mingw64_target}-as
%{_bindir}/%{mingw64_target}-c++filt
%{_bindir}/%{mingw64_target}-dlltool
%{_bindir}/%{mingw64_target}-dllwrap
%{_bindir}/%{mingw64_target}-elfedit
%{_bindir}/%{mingw64_target}-gprof
%{_bindir}/%{mingw64_target}-ld
%{_bindir}/%{mingw64_target}-ld.bfd
%{_bindir}/%{mingw64_target}-nm
%{_bindir}/%{mingw64_target}-objcopy
%{_bindir}/%{mingw64_target}-objdump
%{_bindir}/%{mingw64_target}-ranlib
%{_bindir}/%{mingw64_target}-readelf
%{_bindir}/%{mingw64_target}-size
%{_bindir}/%{mingw64_target}-strings
%{_bindir}/%{mingw64_target}-strip
%{_bindir}/%{mingw64_target}-windmc
%{_bindir}/%{mingw64_target}-windres
%{_prefix}/%{mingw64_target}/bin/ar
%{_prefix}/%{mingw64_target}/bin/as
%{_prefix}/%{mingw64_target}/bin/dlltool
%{_prefix}/%{mingw64_target}/bin/ld
%{_prefix}/%{mingw64_target}/bin/ld.bfd
%{_prefix}/%{mingw64_target}/bin/nm
%{_prefix}/%{mingw64_target}/bin/objcopy
%{_prefix}/%{mingw64_target}/bin/objdump
%{_prefix}/%{mingw64_target}/bin/ranlib
%{_prefix}/%{mingw64_target}/bin/readelf
%{_prefix}/%{mingw64_target}/bin/strip
%{_prefix}/%{mingw64_target}/lib/ldscripts

%files -n ucrt64-binutils
%{_bindir}/%{ucrt64_target}-addr2line
%{_bindir}/%{ucrt64_target}-ar
%{_bindir}/%{ucrt64_target}-as
%{_bindir}/%{ucrt64_target}-c++filt
%{_bindir}/%{ucrt64_target}-dlltool
%{_bindir}/%{ucrt64_target}-dllwrap
%{_bindir}/%{ucrt64_target}-elfedit
%{_bindir}/%{ucrt64_target}-gprof
%{_bindir}/%{ucrt64_target}-ld
%{_bindir}/%{ucrt64_target}-ld.bfd
%{_bindir}/%{ucrt64_target}-nm
%{_bindir}/%{ucrt64_target}-objcopy
%{_bindir}/%{ucrt64_target}-objdump
%{_bindir}/%{ucrt64_target}-ranlib
%{_bindir}/%{ucrt64_target}-readelf
%{_bindir}/%{ucrt64_target}-size
%{_bindir}/%{ucrt64_target}-strings
%{_bindir}/%{ucrt64_target}-strip
%{_bindir}/%{ucrt64_target}-windmc
%{_bindir}/%{ucrt64_target}-windres
%{_prefix}/%{ucrt64_target}/bin/ar
%{_prefix}/%{ucrt64_target}/bin/as
%{_prefix}/%{ucrt64_target}/bin/dlltool
%{_prefix}/%{ucrt64_target}/bin/ld
%{_prefix}/%{ucrt64_target}/bin/ld.bfd
%{_prefix}/%{ucrt64_target}/bin/nm
%{_prefix}/%{ucrt64_target}/bin/objcopy
%{_prefix}/%{ucrt64_target}/bin/objdump
%{_prefix}/%{ucrt64_target}/bin/ranlib
%{_prefix}/%{ucrt64_target}/bin/readelf
%{_prefix}/%{ucrt64_target}/bin/strip
%{_prefix}/%{ucrt64_target}/lib/ldscripts


%changelog
* Tue Dec 30 2025 Sandro Mani <manisandro@gmail.com> - 2.45.1-1
- Update to 2.45.1

* Fri Oct 10 2025 Sandro Mani <manisandro@gmail.com>
- Backport fixes for CVE-2025-11494, CVE-2025-11495, CVE-2025-11082,
  CVE-2025-11081, CVE-2025-11083

* Thu Oct 09 2025 Sandro Mani <manisandro@gmail.com> - 2.45-1
- Update to 2.45

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.44-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 18 2025 Sandro Mani <manisandro@gmail.com> - 2.44-2
- Backport fixes for CVE-2025-7545 and CVE-2025-7546

* Sun Feb 16 2025 Sandro Mani <manisandro@gmail.com> - 2.44-1
- Update to 2.44

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.43.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Oct 02 2024 Davide Cavalca <dcavalca@fedoraproject.org> - 2.43.1-2
- Fix invalid SPDX expression in license tag

* Tue Aug 20 2024 Sandro Mani <manisandro@gmail.com> - 2.43.1-1
- Update to 2.43.1

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 18 2024 Sandro Mani <manisandro@gmail.com> - 2.42-1
- Update to 2.42

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.41-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Oct 17 2023 Sandro Mani <manisandro@gmail.com> - 2.41-1
- Update to 2.41

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.40-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Sandro Mani <manisandro@gmail.com> - 2.40-3
- Backport fix for Backport fix for
  https://sourceware.org/bugzilla/show_bug.cgi?id=30079

* Fri Apr 14 2023 Sandro Mani <manisandro@gmail.com> - 2.40-2
- Backport fix for CVE-2023-1972

* Thu Mar 09 2023 Sandro Mani <manisandro@gmail.com> - 2.40-1
- Update to 2.40

* Tue Mar 07 2023 Sandro Mani <manisandro@gmail.com> - 2.39-5
- Backport patch for CVE-2023-25587

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.39-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 03 2023 Sandro Mani <manisandro@gmail.com> - 2.39-3
- Backport patch for CVE-2022-4285

* Sun Oct 30 2022 Sandro Mani <manisandro@gmail.com> - 2.39-2
- Backport patch for CVE-2022-38533

* Tue Aug 16 2022 Sandro Mani <manisandro@gmail.com> - 2.39-1
- Update to 2.39

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.38-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Apr 26 2022 Sandro Mani <manisandro@gmail.com> - 2.38-2
- Backport proposed fix for binutils #29006

* Fri Mar 11 2022 Sandro Mani <manisandro@gmail.com> - 2.38-1
- Update to 2.38

* Wed Feb 23 2022 Marc-André Lureau <marcandre.lureau@redhat.com> - 2.37-5
- Add ucrt64 target. Related to rhbz#2055254.

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.37-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Dec 18 2021 Sandro Mani <manisandro@gmail.com> - 2.37-3
- Backport fix for CVE-2021-45078

* Thu Aug 12 2021 Sandro Mani <manisandro@gmail.com> - 2.37-2
- Drop man pages

* Sat Jul 24 2021 Sandro Mani <manisandro@gmail.com> - 2.37-1
- Update to 2.37

* Sat Jul 24 2021 Sandro Mani <manisandro@gmail.com> - 2.36.1-3
- Backport fix for "relocation truncated to fit" errors

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.36.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Feb 13 2021 Sandro Mani <manisandro@gmail.com> - 2.36.1-1
- Update to 2.36.1

* Thu Jan 28 2021 Richard W.M. Jones <rjones@redhat.com> - 2.34-7
- Backport fixes for CVE-2021-20197.
- Bump and rebuild for s390.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.34-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec 18 2020 Sandro Mani <manisandro@gmail.com> - 2.34-4
- Backport patches for CVE-2020-16592, CVE-2020-16598

* Wed Jul 29 2020 Sandro Mani <manisandro@gmail.com> - 2.34-3
- Fix ld --version output

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Jeff Law <law@redhat.com> - 2.34.0-2
- Fix configure tests compromised by LTO

* Fri Jun 19 2020 Sandro Mani <manisandro@gmail.com> - 2.34.0-1
- Update to 2.34.0
- Modernize spec

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.32-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 19 2019 Sandro Mani <manisandro@gmail.com> - 2.32-6
- Add binutils_24267.patch
- Drop non-relevant patches from native binutils package

* Tue Aug 13 2019 Fabiano Fidêncio <fidencio@redhat.com> - 3.32-5
- Backport all patches from native binutils package, rhbz#1740709

* Wed Aug 07 2019 Sandro Mani <manisandro@gmail.com> - 2.32-4
- Backport patch to fix "too many open files" when linking libLLVM.dll

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 07 2019 Sandro Mani <manisandro@gmail.com> - 2.32-1
- Update to 2.32

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.30-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Aug 22 2018 Sandro Mani <manisandro@gmail.com> - 2.30-5
- Refresh patch for binutils bug #23061

* Wed Aug 08 2018 Sandro Mani <manisandro@gmail.com> - 2.30-4
- Backport patch for binutils bug #23061

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 14 2018 Sandro Mani <manisandro@gmail.com> - 2.30-2
- Backport patch for binutils bug #22762

* Thu Jun 14 2018 Sandro Mani <manisandro@gmail.com> - 2.30-1
- Update to 2.30

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.29.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Oct 08 2017 Kalev Lember <klember@redhat.com> - 2.29.1-1
- Update to 2.29.1

* Tue Sep 19 2017 Sandro Mani <manisandro@gmail.com> - 2.29-4
- Rebuild for mingw-filesystem (for %%mingw_nm macro)

* Fri Aug 25 2017 Sandro Mani <manisandro@gmail.com> - 2.29-3
- Also build multilib version of nm

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Kalev Lember <klember@redhat.com> - 2.29-1
- Update to 2.29

* Mon Mar 06 2017 Kalev Lember <klember@redhat.com> - 2.28-1
- Update to 2.28

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Aug 10 2016 Kalev Lember <klember@redhat.com> - 2.27-1
- Update to 2.27

* Tue May 10 2016 Kalev Lember <klember@redhat.com> - 2.26-1
- Update to 2.26

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Dec 23 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.25-1
- Update to 2.25

* Tue Dec 23 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.24-5
- Fix CVE-2014-8501 (RHBZ #1162578 #1162583)
- Fix CVE-2014-8502 (RHBZ #1162602)
- Fix CVE-2014-8503 (RHBZ #1162612)
- Fix CVE-2014-8504 (RHBZ #1162626)
- Fix CVE-2014-8737 (RHBZ #1162660)
- Fix CVE-2014-8738 (RHBZ #1162673)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.24-2
- Fix FTBFS against gcc 4.9

* Sat Jan 11 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.24-1
- Update to 2.24

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.23.52.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr  3 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.23.52.0.1-1
- Update to 2.23.52.0.1
- Fixes FTBFS against latest texinfo
- Resolve build failure on PPC

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.23.51.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.23.51.0.5-3
- Backported patch to fix 'unexpected version string length' error in windres (RHBZ #902960)

* Tue Nov 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.23.51.0.5-2
- Added BR: zlib-devel to enable support for compressed debug sections

* Wed Nov 21 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.23.51.0.5-1
- Update to 2.23.51.0.5 release

* Mon Oct 15 2012 Jon Ciesla <limburgher@gmail.com> - 2.22.52.0.4-2
- Provides: bundled(libiberty)

* Wed Jul 18 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.22.52.0.4-1
- Update to 2.22.52.0.4 release

* Sat Jun  2 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.22.52.0.3-1
- Update to 2.22.52.0.3 release

* Sun Apr  8 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.22.52-4
- Cleaned up unneeded %%global tags

* Tue Mar  6 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.22.52-3
- Made the package compliant with the new MinGW packaging guidelines
- Added win64 support
- Added a mingw-binutils-generic package containing toolchain
  utilities which can be used by both the win32 and win64 toolchains
- Enable the testsuite
- Package the license
- Fix source URL

* Tue Mar  6 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.22.52-2
- Renamed the source package to mingw-binutils (RHBZ #673786)
- Use mingw macros without leading underscore

* Sat Feb 25 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.22.52-1
- Update to 2.22.52 20120225 snapshot
- Bump the BR/R: mingw32-filesystem to >= 95
- Rebuild using the i686-w64-mingw32 triplet
- Dropped some obsolete configure arguments
- Temporary provide mingw-strip, mingw-objdump and mingw-objcopy
  in preparation for win32+win64 support

* Tue Jan 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.22-1
- Update to 2.22
- Dropped unneeded RPM tags
- Use parallel make

* Tue May 10 2011 Kalev Lember <kalev@smartlink.ee> - 2.21-2
- Default to runtime pseudo reloc v2 now that mingw32-runtime 3.18 is in

* Thu Mar 17 2011 Kalev Lember <kalev@smartlink.ee> - 2.21-1
- Update to 2.21
- Added a patch to use runtime pseudo reloc v1 by default as the version of
  mingw32-runtime we have does not support v2.
- Don't own the /usr/i686-pc-mingw32/bin/ directory

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20.51.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep  7 2010 Richard W.M. Jones <rjones@redhat.com> - 2.20.51.0.10-1
- Synchronize with Fedora native version (2.20.51.0.10).
- Note however that we are not using any Fedora patches.

* Thu May 13 2010 Kalev Lember <kalev@smartlink.ee> - 2.20.1-1
- Update to 2.20.1

* Wed Sep 16 2009 Kalev Lember <kalev@smartlink.ee> - 2.19.51.0.14-1
- Update to 2.19.51.0.14

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 10 2009 Richard W.M. Jones <rjones@redhat.com> - 2.19.1-4
- Switch to using upstream (GNU) binutils 2.19.1.  It's exactly the
  same as the MinGW version now.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 2.19.1-2
- Rebuild for mingw32-gcc 4.4

* Tue Feb 10 2009 Richard W.M. Jones <rjones@redhat.com> - 2.19.1-1
- New upstream version 2.19.1.

* Mon Dec 15 2008 Richard W.M. Jones <rjones@redhat.com> - 2.19-1
- New upstream version 2.19.

* Sat Nov 29 2008 Richard W.M. Jones <rjones@redhat.com> - 2.18.50_20080109_2-10
- Must runtime-require mingw32-filesystem.

* Fri Nov 21 2008 Levente Farkas <lfarkas@lfarkas.org> - 2.18.50_20080109_2-9
- BR mingw32-filesystem >= 38

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 2.18.50_20080109_2-8
- Rename mingw -> mingw32.
- BR mingw32-filesystem >= 26.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 2.18.50_20080109_2-7
- Use mingw-filesystem.

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 2.18.50_20080109_2-5
- Initial RPM release, largely based on earlier work from several sources.
