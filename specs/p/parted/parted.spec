# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: The GNU disk partition manipulation program
Name:    parted
Version: 3.6
Release: 13%{?dist}
License: GPL-3.0-or-later
URL:     http://www.gnu.org/software/parted

Source0: https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
Source1: https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz.sig
Source2: pubkey.phillip.susi
Source3: pubkey.brian.lane

Patch0001: 0001-parted-Print-the-Fixing.-message-to-stderr.patch
Patch0002: 0002-doc-Document-IEC-unit-behavior-in-the-manpage.patch
Patch0003: 0003-libparted-Fail-early-when-detecting-nilfs2.patch
Patch0004: 0004-bug-74444-PATCH-parted-fix-do_version-declaration.patch
Patch0005: 0005-libparted-Fix-sun-disklabel-unhandled-exception.patch
Patch0006: 0006-tests-Add-test-for-SUN-disklabel-handling.patch
Patch0007: 0007-libparted-Fix-dvh-disklabel-unhandled-exception.patch
Patch0008: 0008-tests-Add-test-for-dvh-with-a-bad-checksum.patch
Patch0009: 0009-tests-probing-ext4-without-journal-should-still-indi.patch
Patch0010: 0010-libparted-Do-not-detect-ext4-without-journal-as-ext2.patch
Patch0011: 0011-nilfs2-Fixed-possible-sigsegv-in-case-of-corrupted-s.patch
Patch0012: 0012-doc-Fix-some-groff-mandoc-linting-complaints.patch

BuildRequires: gcc
BuildRequires: e2fsprogs-devel
BuildRequires: readline-devel
BuildRequires: ncurses-devel
BuildRequires: gettext-devel
BuildRequires: texinfo
BuildRequires: device-mapper-devel
BuildRequires: libuuid-devel
BuildRequires: libblkid-devel >= 2.17
BuildRequires: gnupg2
BuildRequires: git
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: e2fsprogs
BuildRequires: xfsprogs
BuildRequires: dosfstools
BuildRequires: perl-Digest-CRC
BuildRequires: bc
BuildRequires: python3
BuildRequires: gperf
BuildRequires: make
BuildRequires: check-devel

# bundled gnulib library exception, as per packaging guidelines
# https://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries
Provides: bundled(gnulib)

%description
The GNU Parted program allows you to create, destroy, resize, move,
and copy hard disk partitions. Parted can be used for creating space
for new operating systems, reorganizing disk usage, and copying data
to new hard disks.


%package devel
Summary:  Files for developing apps which will manipulate disk partitions
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The GNU Parted library is a set of routines for hard disk partition
manipulation. If you want to develop programs that manipulate disk
partitions and filesystems using the routines provided by the GNU
Parted library, you need to install this package.


%prep
%{gpgverify} --keyring='%{SOURCE3}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -S git_am
iconv -f ISO-8859-1 -t UTF8 AUTHORS > tmp; touch -r AUTHORS tmp; mv tmp AUTHORS

%build
autoreconf -fiv
CFLAGS="$RPM_OPT_FLAGS -Wno-unused-but-set-variable"; export CFLAGS
%configure --disable-static --disable-gcc-warnings
# Don't use rpath!
%{__sed} -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
%{__sed} -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build


%install
%{__rm} -rf %{buildroot}
%make_install

# Remove components we do not ship
%{__rm} -rf %{buildroot}%{_libdir}/*.la
%{__rm} -rf %{buildroot}%{_infodir}/dir
%{__rm} -rf %{buildroot}%{_bindir}/label
%{__rm} -rf %{buildroot}%{_bindir}/disk

%find_lang %{name}


%check
export LD_LIBRARY_PATH=$(pwd)/libparted/.libs:$(pwd)/libparted/fs/.libs
make check

%files -f %{name}.lang
%doc AUTHORS NEWS README THANKS
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_sbindir}/parted
%{_sbindir}/partprobe
%{_mandir}/man8/parted.8*
%{_mandir}/man8/partprobe.8*
%{_libdir}/libparted.so.2
%{_libdir}/libparted.so.2.0.5
%{_libdir}/libparted-fs-resize.so.0
%{_libdir}/libparted-fs-resize.so.0.0.5
%{_infodir}/parted.info*

%files devel
%doc TODO doc/API doc/FAT
%{_includedir}/parted
%{_libdir}/libparted.so
%{_libdir}/libparted-fs-resize.so
%{_libdir}/pkgconfig/libparted.pc
%{_libdir}/pkgconfig/libparted-fs-resize.pc


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri May 30 2025 Brian C. Lane <bcl@redhat.com> - 3.6-12
- doc: Fix some groff/mandoc linting complaints (bcl)
- nilfs2: Fixed possible sigsegv in case of corrupted superblock (abutenko)
- libparted: Do not detect ext4 without journal as ext2 (pascal)
- tests: probing ext4 without journal should still indicate ext4 (bcl)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 15 2025 Brian C. Lane <bcl@redhat.com> - 3.6-10
- tests: Add test for dvh with a bad checksum (bcl)
- libparted: Fix dvh disklabel unhandled exception (bcl)
- tests: Add test for SUN disklabel handling (bcl)
- libparted: Fix sun disklabel unhandled exception (bcl)

* Wed Nov 20 2024 Brian C. Lane <bcl@redhat.com> - 3.6-9
- parted: Fix do_version declaration (rudi)

* Thu Oct 17 2024 Brian C. Lane <bcl@redhat.com> - 3.6-8
- libparted: Fail early when detecting nilfs2 (oldium.pro)

* Fri Aug 23 2024 Brian C. Lane <bcl@redhat.com> - 3.6-7
- tests: Move to tmt tests and switch to a functional test (bcl)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Brian C. Lane <bcl@redhat.com> - 3.6-5
- doc: Document IEC unit behavior in the manpage (bcl)
- parted: Print the Fixing... message to stderr (bcl)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Apr 10 2023 Brian C. Lane <bcl@redhat.com> - 3.6-1
- Upstream 3.6 stable release
- Dropping pre-3.5 changelog entries

* Mon Mar 27 2023 Brian C. Lane <bcl@redhat.com> - 3.5.28-1
- Upstream 3.5.28 Alpha release
- Dropped all patches included in new upstream release
- Bumped minor version on libparted.so and libparted-fs-resize.so

* Fri Mar 17 2023 Brian C. Lane <bcl@redhat.com> - 3.5-11
- parted: Fix ending sector location when using kibi IEC suffix (bcl)
- tests: Fix formatting and snprintf warnings in tests. (bcl)
- ui: Add checks for prompt being NULL (bcl)
- strlist: Handle realloc error in wchar_to_str (bcl)
- libparted: Fix potential NULL dereference in ped_disk_next_partition (bcl)
- filesys: Check for null from close_fn (bcl)

* Tue Feb 07 2023 Brian C. Lane <bcl@redhat.com> - 3.5-10
- libparted: Fix problem with creating 1s partitions
- tests: Fixing libparted test framework usage

* Mon Jan 30 2023 Brian C. Lane <bcl@redhat.com> - 3.5-9
- SPDX migration

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec 14 2022 Brian C. Lane <bcl@redhat.com> - 3.5-7
- libparted: Fix handling of msdos partition types
- tests: Add a libparted test for ped_partition_set_system on msdos
- parted: Add display of GPT UUIDs in JSON output
- Add no_automount flag support
- increase xfs size to 300M

* Mon Aug 08 2022 Brian C. Lane <bcl@redhat.com> - 3.5-6
- Fix ped_partition_set_system handling of existing flags

* Thu Aug 04 2022 Brian C. Lane <bcl@redhat.com> - 3.5-5
- Update enum patch description for upstream

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 20 2022 Adam Williamson <awilliam@redhat.com> - 3.5-3
- Set _FIRST_ and _LAST_ macro values directly

* Tue May 17 2022 Brian C. Lane <bcl@redhat.com> - 3.5-2
- tests: t3200-type-change now passes (bcl)
- parted: Reset the filesystem type when changing the id/uuid (bcl)
- libparted: add swap flag for DASD label (aschnell)
- parted: add type command (aschnell)
- maint: post-release administrivia (bcl)

* Mon Apr 18 2022 Brian C. Lane <bcl@redhat.com> - 3.5-1
- Upstream 3.5 stable release
