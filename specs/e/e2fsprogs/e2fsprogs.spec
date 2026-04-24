# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: Utilities for managing ext2, ext3, and ext4 file systems
Name: e2fsprogs
Version: 1.47.3
Release: 3%{?dist}

# License tags based on COPYING file distinctions for various components
# Automatically converted from old format: GPLv2 - review is highly recommended.
License: GPL-2.0-only
Source0: https://www.kernel.org/pub/linux/kernel/people/tytso/%{name}/v%{version}/%{name}-%{version}.tar.xz
Source1: https://www.kernel.org/pub/linux/kernel/people/tytso/%{name}/v%{version}/%{name}-%{version}.tar.sign
# GPG key fetched from https://thunk.org/tytso/tytso-key.asc
# which was linked from https://thunk.org/tytso/
# Also verified fingerprint matches on https://www.kernel.org/doc/wot/tytso.html
# note that the GPG key linked off his MIT page is likely old, and is *not* the
# same as the above key ( http://web.mit.edu/tytso/www/home.html )
Source2: tytso-key.asc

Url: http://e2fsprogs.sourceforge.net/
Requires: e2fsprogs-libs%{?_isa} = %{version}-%{release}
Requires: libcom_err%{?_isa} = %{version}-%{release}
Requires: libss = %{version}-%{release}

# e4fsprogs was a parallel ext4-capable package in RHEL5.x
%if 0%{?rhel} > 0
Obsoletes: e4fsprogs < %{version}-%{release}
Provides: e4fsprogs = %{version}-%{release}
%endif

%if "%{_sbindir}" == "%{_bindir}"
# We rely on filesystem to create the compat symlinks for us
Requires: filesystem(unmerged-sbin-symlinks)
Provides: /usr/sbin/mke2fs
Provides: /usr/sbin/fsck.ext2
Provides: /usr/sbin/fsck.ext3
Provides: /usr/sbin/fsck.ext4
Provides: /usr/sbin/mkfs.ext2
Provides: /usr/sbin/mkfs.ext3
Provides: /usr/sbin/mkfs.ext4
%endif

BuildRequires: pkgconfig, texinfo, libselinux-devel, gcc
BuildRequires: fuse3-devel
BuildRequires: libsepol-devel
BuildRequires: libblkid-devel
BuildRequires: libuuid-devel
BuildRequires: gettext
BuildRequires: multilib-rpm-config
BuildRequires: systemd
BuildRequires: make

# For gpg verifying the source tarball
BuildRequires: gnupg2 xz

Patch 0:	0001-remove-local-PATH.patch

%description
The e2fsprogs package contains a number of utilities for creating,
checking, modifying, and correcting any inconsistencies in second,
third and fourth extended (ext2/ext3/ext4) file systems. E2fsprogs
contains e2fsck (used to repair file system inconsistencies after an
unclean shutdown), mke2fs (used to initialize a partition to contain
an empty ext2 file system), debugfs (used to examine the internal
structure of a file system, to manually repair a corrupted
file system, or to create test cases for e2fsck), tune2fs (used to
modify file system parameters), and most of the other core ext2fs
file system utilities.

You should install the e2fsprogs package if you need to manage the
performance of an ext2, ext3, or ext4 file system.

%package libs
Summary: Ext2/3/4 file system specific shared libraries
License: GPLv2 and LGPLv2
Requires: libcom_err%{?_isa} = %{version}-%{release}

%description libs
E2fsprogs-libs contains libe2p and libext2fs, the libraries of the
e2fsprogs package.

These libraries are used to directly access ext2/3/4 file systems
from user space.

%package static
Summary: Ext2/3/4 file system specific static libraries
License: GPLv2 and LGPLv2

%description static
E2fsprogs-static contains all static libraries built from e2fsprogs,
including libext2fs, libcom_err, libe2p, and libss.

These libraries are used to directly access ext2/3/4 file systems
from user space, and perform other useful functions.

%package devel
Summary: Ext2/3/4 file system specific libraries and headers
License: GPLv2 and LGPLv2
Requires: e2fsprogs-libs%{?_isa} = %{version}-%{release}
Requires: libcom_err-devel%{?_isa} = %{version}-%{release}
Requires: gawk
Requires: pkgconfig

%description devel
E2fsprogs-devel contains the libraries and header files needed to
develop second, third and fourth extended (ext2/ext3/ext4)
file system specific programs.

You should install e2fsprogs-devel if you want to develop ext2/3/4
file system specific programs. If you install e2fsprogs-devel, you'll
also want to install e2fsprogs.

%package -n libcom_err
Summary: Common error description library
License: MIT

%description -n libcom_err
This is the common error description library, part of e2fsprogs.

libcom_err is an attempt to present a common error-handling mechanism.

%package -n libcom_err-devel
Summary: Common error description library
License: MIT
Requires: libcom_err%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description -n libcom_err-devel
This is the common error description development library and headers,
part of e2fsprogs.  It contains the compile_et command, used
to convert a table listing error-code names and associated messages
messages into a C source file suitable for use with the library.

libcom_err is an attempt to present a common error-handling mechanism.

%package -n libss
Summary: Command line interface parsing library
License: MIT
Requires: libcom_err%{?_isa} = %{version}-%{release}

%description -n libss
This is libss, a command line interface parsing library, part of e2fsprogs.

This package includes a tool that parses a command table to generate
a simple command-line interface parser, the include files needed to
compile and use it.

It was originally inspired by the Multics SubSystem library.

%package -n libss-devel
Summary: Command line interface parsing library
License: MIT
Requires: libss%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description -n libss-devel
This is the command line interface parsing (libss) development library
and headers, part of e2fsprogs.  It contains the mk_cmds command, which
parses a command table to generate a simple command-line interface parser.

It was originally inspired by the Multics SubSystem library.

%package -n e2scrub
Summary: Online Ext4 metadata consistency checking tool and service
License: GPLv2 and LGPLv2
Recommends: /usr/sbin/sendmail
Requires: systemd
Requires: util-linux
Requires: lvm2
Requires: e2fsprogs%{?_isa} = %{version}-%{release}

%description -n e2scrub
This package includes e2scrub script that can check ext[234] file system
metadata consistency while the file system is online. It also containes a
systemd service that can be enabled to do consistency check periodically.

The file system consistency check can be performed online and does not
require the file system to be unmounted. It uses lvm snapshots to do this
which means that it can only be done on file systems that are on a lvm
managed device with some free space available in respective volume group.

%prep
xzcat '%{SOURCE0}' | %{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data=-
%setup -q

%patch -P0 -p1
# Remove flawed tests
rm -rf tests/m_rootdir_acl

%global _udevdir %{_prefix}/lib/udev/rules.d

%build
%configure CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" \
	   --enable-elf-shlibs --enable-nls --disable-uuidd --disable-fsck \
	   --disable-e2initrd-helper --disable-libblkid --disable-libuuid \
	   --enable-quota --with-root-prefix=/usr --with-crond-dir=no
%make_build

%install
rm -rf %{buildroot}
export PATH=/sbin:$PATH
%make_install install-libs \
	root_sbindir=%{_sbindir} root_libdir=%{_libdir}

# Replace arch-dependent header file with arch-independent stub (when needed).
%multilib_fix_c_header --file %{_includedir}/ext2fs/ext2_types.h

# Hack for now, otherwise strip fails.
chmod +w %{buildroot}%{_libdir}/*.a

%find_lang %{name}

%check
make PRINT_FAILED=yes fullcheck

%ldconfig_scriptlets libs

%ldconfig_scriptlets -n libcom_err

%ldconfig_scriptlets -n libss

%files -f %{name}.lang
%doc README
%{!?_licensedir:%global license %%doc}

%config(noreplace) %{_sysconfdir}/mke2fs.conf

%{_sbindir}/badblocks
%{_sbindir}/debugfs
%{_sbindir}/dumpe2fs
%{_sbindir}/e2fsck
%{_sbindir}/e2image
%{_sbindir}/e2label
%{_sbindir}/e2mmpstatus
%{_sbindir}/e2undo
%{_sbindir}/e4crypt
%{_sbindir}/fsck.ext2
%{_sbindir}/fsck.ext3
%{_sbindir}/fsck.ext4
%{_sbindir}/logsave
%{_sbindir}/mke2fs
%{_sbindir}/mkfs.ext2
%{_sbindir}/mkfs.ext3
%{_sbindir}/mkfs.ext4
%{_sbindir}/resize2fs
%{_sbindir}/tune2fs
%{_sbindir}/filefrag
%{_sbindir}/e2freefrag
%{_sbindir}/e4defrag
%{_sbindir}/mklost+found

%{_bindir}/chattr
%{_bindir}/lsattr
%{_bindir}/fuse2fs
%{_mandir}/man1/chattr.1*
%{_mandir}/man1/fuse2fs.1*
%{_mandir}/man1/lsattr.1*

%{_mandir}/man5/ext2.5*
%{_mandir}/man5/ext3.5*
%{_mandir}/man5/ext4.5*
%{_mandir}/man5/e2fsck.conf.5*
%{_mandir}/man5/mke2fs.conf.5*

%{_mandir}/man8/badblocks.8*
%{_mandir}/man8/debugfs.8*
%{_mandir}/man8/dumpe2fs.8*
%{_mandir}/man8/e2fsck.8*
%{_mandir}/man8/e4crypt.8*
%{_mandir}/man8/filefrag.8*
%{_mandir}/man8/e2freefrag.8*
%{_mandir}/man8/e4defrag.8*
%{_mandir}/man8/fsck.ext2.8*
%{_mandir}/man8/fsck.ext3.8*
%{_mandir}/man8/fsck.ext4.8*
%{_mandir}/man8/e2image.8*
%{_mandir}/man8/e2label.8*
%{_mandir}/man8/e2mmpstatus.8*
%{_mandir}/man8/e2undo.8*
%{_mandir}/man8/logsave.8*
%{_mandir}/man8/mke2fs.8*
%{_mandir}/man8/mkfs.ext2.8*
%{_mandir}/man8/mkfs.ext3.8*
%{_mandir}/man8/mkfs.ext4.8*
%{_mandir}/man8/mklost+found.8*
%{_mandir}/man8/resize2fs.8*
%{_mandir}/man8/tune2fs.8*

%{_udevrulesdir}/64-ext4.rules

%files libs
%{!?_licensedir:%global license %%doc}
%license NOTICE
%{_libdir}/libe2p.so.*
%{_libdir}/libext2fs.so.*

%files static
%{!?_licensedir:%global license %%doc}
%license NOTICE
%{_libdir}/*.a

%files devel
%{_infodir}/libext2fs.info*
%{_libdir}/libe2p.so
%{_libdir}/libext2fs.so
%{_libdir}/pkgconfig/e2p.pc
%{_libdir}/pkgconfig/ext2fs.pc

%{_includedir}/e2p
%{_includedir}/ext2fs

%files -n libcom_err
%{!?_licensedir:%global license %%doc}
%license NOTICE
%{_libdir}/libcom_err.so.*

%files -n libcom_err-devel
%{_bindir}/compile_et
%{_libdir}/libcom_err.so
%{_datadir}/et
%{_includedir}/et
%{_includedir}/com_err.h
%{_mandir}/man1/compile_et.1*
%{_mandir}/man3/com_err.3*
%{_libdir}/pkgconfig/com_err.pc

%files -n libss
%{!?_licensedir:%global license %%doc}
%license NOTICE
%{_libdir}/libss.so.*

%files -n libss-devel
%{_bindir}/mk_cmds
%{_libdir}/libss.so
%{_datadir}/ss
%{_includedir}/ss
%{_mandir}/man1/mk_cmds.1*
%{_libdir}/pkgconfig/ss.pc

%files -n e2scrub
%config(noreplace) %{_sysconfdir}/e2scrub.conf
%{_sbindir}/e2scrub
%{_sbindir}/e2scrub_all
%{_mandir}/man8/e2scrub.8*
%{_mandir}/man8/e2scrub_all.8*
%{_libexecdir}/e2fsprogs/e2scrub_fail
%{_unitdir}/e2scrub@.service
%{_unitdir}/e2scrub_all.service
%{_unitdir}/e2scrub_all.timer
%{_unitdir}/e2scrub_fail@.service
%{_unitdir}/e2scrub_reap.service
%{_udevdir}/96-e2scrub.rules

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.47.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 10 2025 Pavel Reichl <preichl@redhat.com> - 1.47.3-1
- Update to the v1.47.3

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.47.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 12 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.47.2-2
- Rebuilt for the bin-sbin merge (2nd attempt)

* Mon Jan 06 2025 Pavel Reichl <preichl@redhat.com> - 1.47.2-1
- Update to the latest upstream version
- Drop patch added in 1.47.1-6 release because it is already in 1.47.2

* Mon Oct 21 2024 Eric Sandeen <sandeen@redhat.com> - 1.47.1-6
- Actually apply the new patch to handle orphan inode file
  (RHBZ#2318710)

* Sat Oct 19 2024 Eric Sandeen <sandeen@redhat.com> - 1.47.1-5
- e2fsck: don't skip checks if the orphan file is present in the filesystem
  (RHBZ#2318710)

* Mon Jul 29 2024 Miroslav Suchý <msuchy@redhat.com> - 1.47.1-4
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.47.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.47.1-2
- Rebuilt for the bin-sbin merge

* Tue Jun 25 2024 Eric Sandeen <sandeen@sandeen.net> - 1.47.1-1
- New upstream version (#2282078)
- Build against fuse3 rather than fuse(2) (#1940259)
- New udev rule to prohibit auto-mounting, from upstreamg

* Fri Feb 09 2024 Brian J. Murrell <brian@interlinx.bc.ca> - 1.47.0-5
- Recommends: /usr/sbin/sendmail rather than sendmail as many packages
  can provide a /usr/sbin/sendmail command

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.47.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.47.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.47.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed May 24 2023 Eric Sandeen <sandeen@redhat.com> - 1.47.0-1
- New upstream release

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.46.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.46.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.46.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 3 2022 Lukas Czerner <lczerner@redhat.com> - 1.46.5-1
- New upstream release

* Wed Jul 28 2021 Lukas Czerner <lczerner@redhat.com> - 1.46.3-1
- New upstream release

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.46.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Mar 1 2021 Lukas Czerner <lczerner@redhat.com> - 1.46.2
- New upstream release

* Fri Feb 12 2021 Lukas Czerner <lczerner@redhat.com> - 1.46.1
- New upstream release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.45.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.45.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 1.45.6-3
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Wed Mar 25 2020 Eric Sandeen <sandeen@redhat.com> - 1.45.6-2
- Remove local/ elements from e2scrub PATH

* Tue Mar 24 2020 Eric Sandeen <sandeen@redhat.com> - 1.45.6-1
- New upstream release

* Thu Jan 30 2020 Lukas Czerner <lczerner@redhat.com> - 1.45.5-3
- Fix build errors with gcc 10

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.45.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 8 2020 Lukas Czerner <lczerner@redhat.com> - 1.45.5-1
- New upstream release

* Thu Oct 3 2019 Lukas Czerner <lczerner@redhat.com> - 1.45.4-1
- New upstream release

* Thu Jul 25 2019 Lukas Czerner <lczerner@redhat.com> - 1.45.3-1
- New upstream release

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.45.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 29 2019 Lukas Czerner <lczerner@redhat.com> - 1.45.2-1
- New upstream release

* Tue Mar 12 2019 Lukas Czerner <lczerner@redhat.com> - 1.45.0-1
- New upstream release

* Thu Mar  7 2019 Tim Landscheidt <tim@tim-landscheidt.de> - 1.44.6-2
- Remove obsolete requirements for %%post/%%preun scriptlets

* Wed Mar 6 2019 Lukas Czerner <lczerner@redhat.com> 1.44.6-1
- New upstream release

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.44.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 8 2019 Lukas Czerner <lczerner@redhat.com> 1.44.5-1
- New upstream release

* Mon Aug 20 2018 Lukas Czerner <lczerner@redhat.com> 1.44.4-1
- New upstream release

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.44.3-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Lukas Czerner <lczerner@redhat.com> 1.44.3-0
- New upstream release
- Remove multiarch wrappers
- Remove needless use of %%defattr marco

* Wed Apr 04 2018 Lukas Czerner <lczerner@redhat.com> 1.44.1-1
- New upstream release
- tests: use mke2fs and debugfs from the build tree
- remove custom patch to ignose sb feature differences
- e2fsprogs: fix metadata image handling on big endian systems
- fix spelling errors in spec file
- remove custom e2fsck.conf

* Mon Mar 12 2018 Lukas Czerner <lczerner@redhat.com> 1.44.0-2
- e2fsck: fix endianness problem when reading htree nodes
- use make fullcheck in %%check section to run all the tests

* Thu Mar 08 2018 Lukas Czerner <lczerner@redhat.com> 1.44.0-1
- New upstream release
- Add gcc to the BuildRequires to comply with packaging guidelines

* Mon Mar 05 2018 Lukas Czerner <lczerner@redhat.com> 1.43.9-1
- New upstream release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.43.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 9 2018 Lukas Czerner <lczerner@redhat.com> 1.43.8-1
- New upstream release
- Fix build failure swapfs.c on big-endian

* Wed Oct 18 2017 Eric Sandeen <sandeen@redhat.com> 1.43.7-1
- New upstream release

* Wed Aug 30 2017 Eric Sandeen <sandeen@redhat.com> 1.43.6-1
- New upstream release

* Fri Aug 11 2017 Kalev Lember <klember@redhat.com> 1.43.5-2
- Bump and rebuild for an rpm signing issue

* Tue Aug 08 2017 Eric Sandeen <sandeen@redhat.com> 1.43.5-1
- New upstream release

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.43.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.43.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Feb 01 2017 Stephen Gallagher <sgallagh@redhat.com> - 1.43.4-2
- Add missing %%license macro

* Tue Jan 31 2017 Eric Sandeen <sandeen@redhat.com> 1.43.4-1
- New upstream release

* Mon Sep 05 2016 Eric Sandeen <sandeen@redhat.com> 1.43.3-1
- New upstream release

* Mon Sep 05 2016 Eric Sandeen <sandeen@redhat.com> 1.43.2-1
- New upstream release (broken on i686, not built)

* Thu Jun 16 2016 Eric Sandeen <sandeen@redhat.com> 1.43.1-2
- Fix e2undo endian issues (#1344636)

* Wed Jun 08 2016 Eric Sandeen <sandeen@redhat.com> 1.43.1-1
- New upstream release

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.42.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.42.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Eric Sandeen <sandeen@redhat.com> 1.42.13-2
- Add -fno-strict-aliasing (#1211582)

* Mon May 18 2015 Eric Sandeen <sandeen@redhat.com> 1.42.13-1
- New upstream release

* Thu Apr 30 2015 Eric Sandeen <sandeen@redhat.com> 1.42.12-5
- Don't trigger full check within time fudge window (#1202024)

* Tue Feb 24 2015 Eric Sandeen <sandeen@redhat.com> 1.42.12-4
- Fix potential buffer overflow in closefs (#1193947, CVE-2015-1572)
- Fix dumpe2fs segfault with no arguments (#1194063)
- Don't require fsck prior to resize2fs -P (#1170803)

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.42.12-3
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Tue Feb 17 2015 Eric Sandeen <sandeen@redhat.com> 1.42.12-2
- Fix use after free (#1192861)
- Fix time-based fsck if set in superblock (e2fsck.conf, #963283)

* Fri Aug 29 2014 Eric Sandeen <sandeen@redhat.com> 1.42.12-1
- New upstream release

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.42.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Tom Callaway <spot@fedoraproject.org> 1.42.11-2
- fix license handling

* Fri Jul 11 2014 Eric Sandeen <sandeen@redhat.com> 1.42.11-1
- New upstream release

* Tue Jul 01 2014 Dan Horák <dan@danny.cz> - 1.42.10-5
- Rebuilt for buggy rpm 4.12 alpha -
  https://lists.fedoraproject.org/pipermail/devel/2014-June/200633.html

* Mon Jun 30 2014 Dan Horák <dan[at]danny.cz> - 1.42.10-4
- Add missing dependency info for quota.c - fixes build on s390(x)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.42.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Eric Sandeen <sandeen@redhat.com> 1.42.10-2
- Fix large file handling on 32-bit builds

* Mon May 19 2014 Eric Sandeen <sandeen@redhat.com> 1.42.10-1
- New upstream release
- Enable userspace quota

* Mon Jan 20 2014 Eric Sandeen <sandeen@redhat.com> 1.42.9-2
- Fix up Source0 URL

* Thu Jan 02 2014 Eric Sandeen <sandeen@redhat.com> 1.42.9-1
- New upstream release
- Re-enable disabled tests for now

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.42.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Eric Sandeen <sandeen@redhat.com> 1.42.8-2
- Interpackage dependencies should be for same arch
- Remove newly added but failing resize2fs tests for now

* Wed Jun 26 2013 Eric Sandeen <sandeen@redhat.com> 1.42.8-1
- New upstream release

* Tue Jan 29 2013 Eric Sandeen <sandeen@redhat.com> 1.42.7-2
- Tighten up inter-package dependencies

* Tue Jan 22 2013 Eric Sandeen <sandeen@redhat.com> 1.42.7-1
- New upstream release

* Tue Oct 02 2012 Eric Sandeen <sandeen@redhat.com> 1.42.6-2
- Switch back to gzipped tarball to make sf.net source URL correct

* Tue Oct 02 2012 Eric Sandeen <sandeen@redhat.com> 1.42.6-1
- New upstream release

* Thu Aug 16 2012 Eric Sandeen <sandeen@redhat.com> 1.42.5-2
- Add explicit library deps to e2fsprogs (#848805)

* Mon Jul 30 2012 Eric Sandeen <sandeen@redhat.com> 1.42.5-1
- New upstream release

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.42.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Eric Sandeen <sandeen@redhat.com> 1.42.4-1
- New upstream release

* Thu May 31 2012 Eric Sandeen <sandeen@redhat.com> 1.42.3-2
- Fixes for > 16T filesystems

* Mon May 14 2012 Eric Sandeen <sandeen@redhat.com> 1.42.3-1
- New upstream release

* Sun Apr 22 2012 Eric Sandeen <sandeen@@redhat.com> 1.42.2-6
- Add missing [options] tag to e2fsck.conf

* Fri Apr 20 2012 Eric Sandeen <sandeen@@redhat.com> 1.42.2-5
- Add broken system clock config to e2fsck.conf to let boot
  continue even if system clock very wrong.

* Mon Apr 09 2012 Eric Sandeen <sandeen@@redhat.com> 1.42.2-4
- Handle 32-bit bitmaps in new find_first_zero functions

* Fri Mar 30 2012 Richard W.M. Jones <rjones@redhat.com> 1.42.2-3
- Rebuild against new RPM (RHBZ#808250).

* Wed Mar 28 2012 Eric Sandeen <sandeen@redhat.com> 1.42.2-2
- Move files out of /sbin and /lib into /usr/...

* Tue Mar 27 2012 Eric Sandeen <sandeen@redhat.com> 1.42.2-1
- New upstream release

* Mon Feb 20 2012 Eric Sandeen <sandeen@redhat.com> 1.42.1-1
- New upstream release

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Eric Sandeen <sandeen@redhat.com> 1.42-1
- New upstream point release

* Mon Nov 21 2011 Eric Sandeen <sandeen@redhat.com> 1.42-0.9.WIP.1120
- Build the right tarball for 1.42-WIP-1120

* Mon Nov 21 2011 Eric Sandeen <sandeen@redhat.com> 1.42-0.8.WIP.1120
- New upstream snapshot release

* Thu Nov 10 2011 Eric Sandeen <sandeen@redhat.com> 1.42-0.7.WIP.1016
- Several mmp-related fixes

* Tue Nov 08 2011 Eric Sandeen <sandeen@redhat.com> 1.42-0.6.WIP.1016
- Fix e2fsck / make check on big endian arch

* Mon Oct 17 2011 Eric Sandeen <sandeen@redhat.com> 1.42-0.5.WIP.1016
- New upstream snapshot release

* Mon Oct 10 2011 Eric Sandeen <sandeen@redhat.com> 1.42-0.4.WIP.2011.1009
- New upstream snapshot release

* Mon Sep 26 2011 Eric Sandeen <sandeen@redhat.com> 1.42-0.3.WIP.0925
- New upstream snapshot release

* Tue Aug 09 2011 Eric Sandeen <sandeen@redhat.com> 1.42-0.2.WIP.0702
- Fix use of uninitialized memory via ext2fs_copy_generic_bmap()

* Tue Aug 09 2011 Eric Sandeen <sandeen@redhat.com> 1.42-0.1.WIP.0702
- Test release for >16T support 

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.41.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Eric Sandeen <sandeen@redhat.com> 1.41.14-1
- New upstream release

* Wed Dec 22 2010 Dan Horák <dan[at]danny.cz> 1.41.13-2
- Add upstream fix for big-endian machines

* Mon Dec 20 2010 Eric Sandeen <sandeen@redhat.com> 1.41.13-1
- New upstream release

* Tue Dec 07 2010 Eric Sandeen <sandeen@redhat.com> 1.41.12-7
- Fix up UTF-8 formatting in e2fsck output (#655227)

* Wed Oct 06 2010 Eric Sandeen <sandeen@redhat.com> 1.41.12-6
- Install e4defrag for testing

* Tue Jul 13 2010 Eric Sandeen <sandeen@redhat.com> 1.41.12-5
- Relax fsck requirements for resize2fs -P

* Mon Jul 12 2010 Eric Sandeen <sandeen@redhat.com> 1.41.12-4
- Add COPYING file to the static subpackage

* Wed Jun 02 2010 Eric Sandeen <sandeen@redhat.com> 1.41.12-3
- Reinstate static libs in dedicated package (#596377)

* Wed May 19 2010 Eric Sandeen <sandeen@redhat.com> 1.41.12-2
- Fix fsck thinko in 1.41.12 release

* Mon May 17 2010 Eric Sandeen <sandeen@redhat.com> 1.41.12-1
- New upstream version

* Mon Mar 15 2010 Eric Sandeen <sandeen@redhat.com> 1.41.11-1
- New upstream version

* Mon Mar 01 2010 Eric Sandeen <sandeen@redhat.com> 1.41.10-5
- Don't ask for confirmation of misaligned mkfs with -F (#569021)

* Tue Feb 23 2010 Eric Sandeen <sandeen@redhat.com> 1.41.10-4
- Fix for e2fsck -fD corruption

* Fri Feb 12 2010 Eric Sandeen <sandeen@redhat.com> 1.41.10-3
- And drop virtual provides for static libs

* Fri Feb 12 2010 Eric Sandeen <sandeen@redhat.com> 1.41.10-2
- Drop static libs (#545144)

* Wed Feb 10 2010 Eric Sandeen <sandeen@redhat.com> 1.41.10-1
- New upstream version

* Sun Feb 07 2010 Eric Sandeen <sandeen@redhat.com> 1.41.9-10
- Upstream version of resize2fs array fix, original was wrong

* Sat Jan 23 2010 Eric Sandeen <sandeen@redhat.com> 1.41.9-9
- Fix up stray output & re-enable make check
- Fix dlopen issues for newer libreadline
- Fix access beyond end of array in resize2fs

* Tue Nov 10 2009 Eric Sandeen <sandeen@redhat.com> 1.41.9-8
- Fix up topology patch to build w/ new util-linux-ng
- Fix endian swapping of backup journal blocks in sb

* Tue Nov 10 2009 Eric Sandeen <sandeen@redhat.com> 1.41.9-7
- Re-enable "make check" during build

* Wed Oct 28 2009 Eric Sandeen <sandeen@redhat.com> 1.41.9-6
- Add support for block discard (TRIM) at mkfs time
- Add support for new blkid topology awareness

* Mon Oct 19 2009 Eric Sandeen <sandeen@redhat.com> 1.41.9-5
- Allow superblock timestamp differences up to 24h (#522969)

* Tue Oct 06 2009 Eric Sandeen <sandeen@redhat.com> 1.41.9-4
- Fix install with --excludedocs (#515987)

* Mon Sep 14 2009 Eric Sandeen <sandeen@redhat.com> 1.41.9-3
- Drop defrag bits for now, not ready yet.

* Thu Sep 10 2009 Josef Bacik <josef@toxicpanda.com> 1.41.9-2
- Fix resize -m bug with flexbg (#519131)

* Sun Aug 23 2009 Eric Sandeen <sandeen@redhat.com> 1.41.9-1
- New upstream release

* Thu Aug 06 2009 Eric Sandeen <sandeen@redhat.com> 1.41.8-6
- Fix filefrag in fallback case
- Add e2freefrag & e4defrag (experimental)

* Sun Jul 26 2009 Karel Zak <kzak@redhat.com> 1.41.8-5
- disable fsck (replaced by util-linux-ng)

* Sat Jul 25 2009 Karel Zak <kzak@redhat.com> 1.41.8-4
- disable libuuid and uuidd (replaced by util-linux-ng)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.41.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17  2009 Eric Sandeen <sandeen@redhat.com> 1.41.8-2
- Address some package review concerns (#225714)

* Sun Jul 12 2009 Eric Sandeen <sandeen@redhat.com> 1.41.8-1
- New upstream version, several resize fixes.

* Tue Jun 30 2009 Eric Sandeen <sandeen@redhat.com> 1.41.7-1
- New upstream version

* Fri Jun 26 2009 Eric Sandeen <sandeen@redhat.com> 1.41.6-6
- Split out sub-libraries (#225406)
- Don't start uuidd by default

* Thu Jun 18 2009 Eric Sandeen <sandeen@redhat.com> 1.41.6-5
- Update journal backup blocks in sb after resize (#505339)
- Fix memory leak in extent handling functions
- Fix bug in inode writing in extent code, clobbered i_extra_isize etc

* Mon Jun  8 2009 Karel Zak <kzak@redhat.com> 1.41.6-4
- set BuildRequires: libblkid-devel (from util-linux-ng)

* Mon Jun  8 2009 Karel Zak <kzak@redhat.com> 1.41.6-3
- temporary use BuildRequires: e2fsprogs-devel (we cannot install 
  new util-linux-ng with libblkid to buildroots without new e2fsprogs 
  without libblkid). 

* Thu Jun  4 2009 Karel Zak <kzak@redhat.com> 1.41.6-2
- disable libblkid (replaced by libblkid from util-linux-ng)

* Sat May 30 2009 Eric Sandeen <sandeen@redhat.com> 1.41.6-1
- New upstream version

* Fri Apr 24 2009 Eric Sandeen <sandeen@redhat.com> 1.41.5-1
- New upstream version

* Wed Apr 22 2009 Eric Sandeen <sandeen@redhat.com> 1.41.4-8
- Fix support for external journals

* Wed Apr 22 2009 Eric Sandeen <sandeen@redhat.com> 1.41.4-7
- Fix ext4 resize issues (#496982)

* Sat Apr 11 2009 Eric Sandeen <sandeen@redhat.com> 1.41.4-6
- ignore differing NEEDS_RECOVERY flag on fsck post-resize (#471925)

* Thu Feb 26 2009 Eric Sandeen <sandeen@redhat.com> 1.41.4-5
- fix a couple missed descriptions; obsolete e4fsprogs

* Thu Feb 26 2009 Eric Sandeen <sandeen@redhat.com> 1.41.4-4
- Edit summary & description to include ext4 (#487469)
- Fix blkid null ptr deref in initrd (#486997)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.41.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 29 2009 Eric Sandeen <sandeen@redhat.com> 1.41.4-2
- Fix debugfs "stat" segfault if no open fs (#482894)
- Fix name of libext2fs info page (#481620)

* Thu Jan 29 2009 Eric Sandeen <sandeen@redhat.com> 1.41.4-1
- New upstream release
- Dropped btrfs & resize fixes, upstream now

* Tue Jan 20 2009 Eric Sandeen <sandeen@redhat.com> 1.41.3-4
- resize2fs fixes, esp. for ext4

* Sat Jan 10 2009 Eric Sandeen <sandeen@redhat.com> 1.41.3-3
- Remove conservative "don't change journal location" patch for F11
- Add btrfs recognition to blkid

* Fri Nov 07 2008 Eric Sandeen <sandeen@redhat.com> 1.41.3-2
- Bump to revision 2, f10 was behind f9, oops.

* Mon Oct 13 2008 Eric Sandeen <sandeen@redhat.com> 1.41.3-1
- New upstream version (very minor fixes, ext4-related)

* Thu Oct 02 2008 Eric Sandeen <sandeen@redhat.com> 1.41.2-2
- Fix blkid to recognize ext4dev filesystems as ext4-mountable

* Thu Oct 02 2008 Eric Sandeen <sandeen@redhat.com> 1.41.2-1
- New upstream version
- Updated default dir hash (half_md4) for better perf & fewer collisions
- Fixed ext4 online resizing with flex_bg
- ext4 journal now in extents format and in middle of filesystem
- fix unreadable e2image files
- fix file descriptor leak in libcom_err (#464689)

* Sat Aug 23 2008 Eric Sandeen <sandeen@redhat.com> 1.41.0-2
- Don't check the group checksum when !GDT_CSUM (#459875)

* Thu Jul 10 2008 Eric Sandeen <sandeen@redhat.com> 1.41.0-1
- New upstream version
- ext4 capable

* Mon Jul 07 2008 Eric Sandeen <sandeen@redhat.com> 1.41-0.2.WIP.0707
- Fix release macro snafu

* Mon Jul 07 2008 Eric Sandeen <sandeen@redhat.com> 1.41-0.1.WIP.0707
- New upstream snapshot release

* Fri Jun 20 2008 Eric Sandeen <sandeen@redhat.com> 1.41-0.WIP.0617.1
- Fix blkid -g segfault when clearing entries (#452333)

* Wed Jun 18 2008 Eric Sandeen <sandeen@redhat.com> 1.41-0.WIP.0617
- New upstream snapshot release for ext4 capability

* Wed Jun 04 2008 Eric Sandeen <sandeen@redhat.com> 1.40.10-3
- Tidy up multilib hack for non-multilib arches (#446016)
- Fix up postun script (#449868)

* Wed Jun 04 2008 Dennis Gilmore <dennis@ausil.us> 1.40.10-2
- setup header support for sparc

* Fri May 23 2008 Eric Sandeen <esandeen@redhat.com> 1.40.10-1
- New upstream version
- Fixes unprivileged blkid use problem (#448591)

* Mon May 12 2008 Eric Sandeen <esandeen@redhat.com> 1.40.9-2
- Fix blkid swap recognition on big-endian boxes (#445786)

* Sun Apr 27 2008 Eric Sandeen <esandeen@redhat.com> 1.40.9-1
- New upstream version

* Fri Mar 14 2008 Eric Sandeen <esandeen@redhat.com> 1.40.8-2
- Update ext2fs_swap_inode_full() fix to match upstream
- Check more of swapv1 header in blkid detection (#442937)

* Fri Mar 14 2008 Eric Sandeen <esandeen@redhat.com> 1.40.8-1
- New upstream version

* Mon Mar 03 2008 Eric Sandeen <esandeen@redhat.com> 1.40.7-2
- second try at fixing resize2fs vs. large inodes... (#434893)

* Fri Feb 29 2008 Eric Sandeen <esandeen@redhat.com> 1.40.7-1
- New upstream version, special leap-day edition
- Fix resize2fs losing inline xattrs when shrinking (#434893)
  and add patch to fix swap_inode_full in this case
- Allow mke2fs & tune2fs to manipulate large_file feature (#258381)
- Handle lvm error conditions in libblkid (#433857)
- Allow tune2fs to clear the resize_inode feature (#167816)
- Teach blkid to detect LVM2 physical volumes (#409321)
- Show "mostly printable" xattrs as text in debugfs (#430621)
- Trimmed pre-1.38 rpm changelog entries

* Sun Feb 10 2008 Eric Sandeen <esandeen@redhat.com> 1.40.6-1
- New upstream version

* Fri Feb 08 2008 Eric Sandeen <esandeen@redhat.com> 1.40.5-2
- gcc-4.3 rebuild

* Mon Jan 28 2008 Eric Sandeen <esandeen@redhat.com> 1.40.5-1
- New upstream version, drop several now-upstream patches.

* Thu Jan 24 2008 Eric Sandeen <sandeen@redhat.com> 1.40.4-7
- Fix sb flag comparisons properly this time (#428893)
- Make 256-byte inodes for the [default] mkfs case.
  This will facilitate upgrades to ext4 later, and help xattr perf.

* Wed Jan 23 2008 Eric Sandeen <sandeen@redhat.com> 1.40.4-6
- Completely clobber e2fsck.static build.

* Wed Jan 23 2008 Eric Sandeen <sandeen@redhat.com> 1.40.4-5
- Ignore some primary/backup superblock flag differences (#428893)
- Teach libblkid about ext4dev.

* Tue Jan 15 2008 Eric Sandeen <sandeen@redhat.com> 1.40.4-4
- Build e2fsck as a dynamically linked binary.
- Re-fix uidd manpage default paths.

* Mon Jan 14 2008 Eric Sandeen <sandeen@redhat.com> 1.40.4-3
- New uuidd subpackage, and properly set up uuidd at install.

* Tue Jan 01 2008 Eric Sandeen <esandeen@redhat.com> 1.40.4-2
- Add new uidd files to specfile

* Tue Jan 01 2008 Eric Sandeen <esandeen@redhat.com> 1.40.4-1
- New upstream version, drop several now-upstream patches.

* Tue Jan 01 2008 Eric Sandeen <esandeen@redhat.com> 1.40.2-15
- Drop resize_inode removal patch from tune2fs; ostensibly was
  for old kernels which could not mount, but seems to be fine.
- Drop pottcdate removal patch, and don't rebuild .po files,
  causes multilib problems and we generally shouldn't rebuild.
- Drop multilib patch; wrapper header should take care of this now.
- Drop ->open rename, Fedora seems ok with this now.

* Tue Dec 11 2007 Eric Sandeen <esandeen@redhat.com> 1.40.2-14
- Fix integer overflows (#414591 / CVE-2007-5497)

* Tue Dec  4 2007 Stepan Kasal <skasal@redhat.com> 1.40.2-13
- The -devel package now requires device-mapper-devel, to match
  the dependency in blkid.pc (#410791)

* Tue Nov 27 2007 Eric Sandeen <esandeen@redhat.com> 1.40.2-12
- Use upstream patch for blkid fat detection, avoids div-by-zero
  when encountering some BSD partitions (#398281)

* Tue Oct 23 2007 Eric Sandeen <esandeen@redhat.com> 1.40.2-11
- Add arm to multilib header wrapper

* Sat Oct 20 2007 Eric Sandeen <esandeen@redhat.com> 1.40.2-10
- Make (more) file timestamps match those in tarball for multilib tidiness 
- Fix e2fsprogs-libs summary (shared libs not static)

* Mon Oct 15 2007 Eric Sandeen <esandeen@redhat.com> 1.40.2-9
- Detect big-endian squashfs filesystems in libblkid (#305151)

* Tue Oct 02 2007 Eric Sandeen <esandeen@redhat.com> 1.40.2-8
- Detect squashfs filesystems in libblkid (#305151)

* Tue Sep 18 2007 Eric Sandeen <esandeen@redhat.com> 1.40.2-7
- Fix blkid fat probe when there is a real MBR (#290951)

* Tue Sep 18 2007 Oliver Falk <oliver@linux-kernel.at> 1.40.2-6
- Add alpha to the header wrappers 

* Fri Sep 07 2007 Eric Sandeen <esandeen@redhat.com> 1.40.2-5
- wrap a couple headers to fix multilib issues (#270441)

* Wed Aug 29 2007 Eric Sandeen <esandeen@redhat.com> 1.40.2-4
- add gawk to e2fsprogs-devel Requires, compile_et needs it (#265961)

* Thu Aug 23 2007 Eric Sandeen <esandeen@redhat.com> 1.40.2-3
- Update license tags
- Fix one open-create caller with no mode
- Protect ->open ops from glibc open-create-mode-checker
- Fix source URL
- Add gawk to BuildRequires

* Wed Jul 18 2007 Eric Sandeen <esandeen@redhat.com> 1.40.2-2
- Fix bug in ext2fs_swap_inode_full() on big-endian boxes

* Tue Jul 17 2007 Eric Sandeen <esandeen@redhat.com> 1.40.2-1
- New version 1.40.2
- Fix up warning in badblocks

* Mon Jun 25 2007 Eric Sandeen <esandeen@redhat.com> 1.39-15
- Fix up .po files to remove timestamps; multilib issues (#245653)

* Fri Jun 22 2007 Eric Sandeen <esandeen@redhat.com> 1.39-14
- Many coverity-found potential leaks, segfaults, etc (#239354)
- Fix debugfs segfaults when no fs open (#208416, #209330)
- Avoid recursive loops in logdump due to symlinks in /dev (#210371)
- Don't write changes to the backup superblocks by default (#229561)
- Correct byteswapping for fast symlinks with xattrs (#232663)
- e2fsck: added sanity check for xattr validation (#230193)

* Wed Jun 20 2007 Eric Sandeen <esandeen@redhat.com> 1.39-13
- add dist tag to release field

* Wed Jun 20 2007 Eric Sandeen <esandeen@redhat.com> 1.39-12
- add LUKS support to libblkid (#242421)

* Fri Feb 23 2007 Karsten Hopp <karsten@redhat.com> 1.39-11
- fix post/preun requirements
- use smp flags

* Mon Feb 05 2007 Alasdair Kergon <agk@redhat.com> - 1.39-10
- Add build dependency on new device-mapper-devel package.

* Mon Dec 25 2006 Thomas Woerner <twoerner@redhat.com> - 1.39-9
- build fixes for new automake 1.10 (#220715)

* Mon Dec 18 2006 Thomas Woerner <twoerner@redhat.com> - 1.39-8
- make uuid_generate_time generate unique uuids (#218606)

* Wed Sep 20 2006 Jarod Wilson <jwilson@redhat.com> - 1.39-7
- 32-bit 16T fixups from esandeen (#202807)
- Update summaries and descriptions

* Sun Sep 17 2006 Karel Zak <kzak@redhat.com> - 1.39-6
- Fix problem with empty FAT label (#206656)

* Tue Sep  5 2006 Peter Jones <pjones@redhat.com> - 1.39-5
- Fix memory leak in device probing.

* Mon Jul 24 2006 Thomas Woerner <twoerner@redhat.com> - 1.39-4
- fixed multilib devel conflicts (#192665)

* Thu Jul 20 2006 Bill Nottingham <notting@redhat.com> - 1.39-3
- prevent libblkid returning /dev/dm-X

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.39-2.1
- rebuild

* Mon Jul 10 2006 Karel Zak <kzak@redhat.com> - 1.39-2
- add GFS abd GFS2 support to libblkid

* Thu Jul  6 2006 Thomas Woerner <twoerner@redhat.com> - 1.39-1
- new version 1.39
- dropped ext2online, because resize2fs is now able to do online resize
- spec file cleanup
- enabled checks for build

* Tue Jun 13 2006 Bill Nottingham <notting@redhat.com> - 1.38-15
- prevent libblkid returning /dev/dm-X
- fix build

* Tue Mar 21 2006 Karel Zak <kzak@redhat.com> - 1.38-14
- prevent error messages to stderr caused by libblkid calling libdevmapper

* Mon Mar 13 2006 Karel Zak <kzak@redhat.com>  - 1.38-13
- used upstream version of the blkid-epoch patch (by Theodore Tso, #182188)

* Wed Mar  8 2006 Peter Jones <pjones@redhat.com> - 1.38-12
- Move /etc/blkid.tab to /etc/blkid/blkid.tab

* Tue Mar  7 2006 David Cantrell <dcantrell@redhat.com> - 1.38-11
- BuildRequires pkgconfig

* Tue Mar  7 2006 David Cantrell <dcantrell@redhat.com> - 1.38-10
- Disable /etc/blkid.tab caching if time is set before epoch (#182188)

* Fri Feb 24 2006 Peter Jones <pjones@redhat.com> - 1.38-9
- _don't_ handle selinux context on blkid.tab, dwalsh says this is a no-no.

* Wed Feb 22 2006 Peter Jones <pjones@redhat.com> - 1.38-8
- handle selinux context on blkid.tab

* Mon Feb 20 2006 Karsten Hopp <karsten@redhat.de> 1.38-7
- BuildRequires: gettext-devel

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.38-6.2
- bump again for double-long bug on ppc(64)

* Tue Feb  7 2006 Jesse Keating <jkeating@redhat.com> - 1.38-6.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 11 2006 Karel Zak <kzak@redhat.com> 1.38-6
- cleanup device-mapper patch
- use pkg-config for device-mapper

* Mon Jan  9 2006 Peter Jones <pjones@redhat.com> 1.38-5
- fix some more minor logic errors in dm probing

* Wed Jan  4 2006 Peter Jones <pjones@redhat.com> 1.38-4
- fix a logic error in dm probing
- add priority group for dm devices, so they'll be preferred

* Tue Jan  3 2006 Peter Jones <pjones@redhat.com> 1.38-3
- added support for device-mapper devices

* Fri Dec  9 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov 10 2005 Thomas Woerner <twoerner@redhat.com> 1.38-2.1
- fixed file conflicts between 32bit and 64bit packages (#168815)
- fixed mklost+found crashes with buffer overflow (#157773)
  Thanks to Arjan van de Ven for the patch

* Wed Nov  9 2005 Thomas Woerner <twoerner@redhat.com> 1.38-2
- splitted up libs from main package, into a new e2fsprogs-libs package
- fixed requires and prereqs

* Thu Sep  8 2005 Thomas Woerner <twoerner@redhat.com> 1.38-1
- new version 1.38
- Close File descriptor for unregognized devices (#159878)
  Thanks to David Milburn for the patch.
  Merged from RHEL-4
- enable tune2fs to set and clear feature resize_inode (#167816)
- removed outdated information from ext2online man page (#164383)

