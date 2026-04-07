# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary:	Utilities for managing the XFS filesystem
Name:		xfsprogs
Version:	6.15.0
Release:	3%{?dist}
License:	GPL-1.0-or-later AND LGPL-2.1-or-later
URL:		https://xfs.wiki.kernel.org
Source0:	http://kernel.org/pub/linux/utils/fs/xfs/xfsprogs/%{name}-%{version}.tar.xz
Source1:	http://kernel.org/pub/linux/utils/fs/xfs/xfsprogs/%{name}-%{version}.tar.sign
Source2:	https://git.kernel.org/pub/scm/docs/kernel/pgpkeys.git/plain/keys/13F703E6C11CF6F0.asc
Source3:	https://git.kernel.org/pub/scm/docs/kernel/pgpkeys.git/plain/keys/46A7EA18AC33E108.asc

BuildRequires:	make
BuildRequires:	gcc
BuildRequires:	g++
BuildRequires:	libtool, gettext, libattr-devel, libuuid-devel
BuildRequires:	libedit-devel, libblkid-devel >= 2.17-0.1.git5e51568
Buildrequires:	libicu-devel >= 4.6, systemd
BuildRequires:	gnupg2, xz, inih-devel, userspace-rcu-devel
Provides:	xfs-cmds
Obsoletes:	xfs-cmds <= %{version}
Provides:	xfsprogs-qa-devel
Obsoletes:	xfsprogs-qa-devel <= %{version}
Conflicts:	xfsdump < 3.0.1
Suggests:	xfsprogs-xfs_scrub

%if "%{_sbindir}" == "%{_bindir}"
# Compat symlinks for Requires in other packages.
# We rely on filesystem to create the symlinks for us.
Requires:       filesystem(unmerged-sbin-symlinks)
Provides:       /usr/sbin/fsck.xfs
Provides:       /usr/sbin/mkfs.xfs
%endif

%description
A set of commands to use the XFS filesystem, including mkfs.xfs.

XFS is a high performance journaling filesystem which originated
on the SGI IRIX platform.  It is completely multi-threaded, can
support large files and large filesystems, extended attributes,
variable block sizes, is extent based, and makes extensive use of
Btrees (directories, extents, free space) to aid both performance
and scalability.

This implementation is on-disk compatible with the IRIX version
of XFS.

%package devel
Summary:	XFS filesystem-specific headers
Requires:	xfsprogs = %{version}-%{release}, libuuid-devel

%description devel
xfsprogs-devel contains the header files needed to develop XFS
filesystem-specific programs.

You should install xfsprogs-devel if you want to develop XFS
filesystem-specific programs,  If you install xfsprogs-devel, you'll
also want to install xfsprogs.

%package xfs_scrub
Summary:	XFS filesystem online scrubbing utilities
Requires:	xfsprogs = %{version}-%{release}, python3
Requires:	util-linux

%description xfs_scrub
xfs_scrub attempts to check and repair all metadata in a mounted XFS filesystem.
WARNING!  This program is EXPERIMENTAL, which means that its behavior and
interface could change at any time!

%package xfs_extras
Summary:	XFS filesystem extra utilities
Requires:	xfsprogs = %{version}-%{release}, python3
Requires:	util-linux

%description xfs_extras
Extra utilities for XFS filesystems, such as xfs_protofile, that may require
Python.

%prep
xzcat '%{SOURCE0}' | %{gpgverify} --keyring='%{SOURCE3}' --signature='%{SOURCE1}' --data=-
%autosetup -p1

# Inject libicuuc to fix link error:
# /usr/bin/ld: /tmp/ccRHx17I.ltrans1.ltrans.o: undefined reference to symbol 'uiter_setString_76'
# /usr/bin/ld: /usr/lib64/libicuuc.so.76: error adding symbols: DSO missing from command line
sed -r -i 's/\$\(LIBICU_LIBS\)/\0 -licuuc/' scrub/Makefile

%build
export tagname=CC

%configure \
	--enable-editline=yes	\
	--enable-blkid=yes	\
	--enable-lto=no

%make_build

%install
make DIST_ROOT=$RPM_BUILD_ROOT install install-dev \
	PKG_ROOT_SBIN_DIR=%{_sbindir} PKG_ROOT_LIB_DIR=%{_libdir}

# nuke .la files, etc
rm -f $RPM_BUILD_ROOT/{%{_lib}/*.{la,a,so},%{_libdir}/*.{la,a}}

# remove non-versioned docs location
rm -rf $RPM_BUILD_ROOT/%{_datadir}/doc/xfsprogs/

%find_lang %{name}

%ldconfig_scriptlets

%files -f %{name}.lang
%doc doc/CHANGES README
%{_libdir}/*.so.*
%dir %{_libexecdir}/xfsprogs
%{_libexecdir}/xfsprogs/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_sbindir}/*
%{_datadir}/xfsprogs/mkfs/*.conf
%dir %{_datadir}/xfsprogs/
%dir %{_datadir}/xfsprogs/mkfs/
%exclude %{_datadir}/xfsprogs/xfs_scrub_all.cron
%exclude %{_sbindir}/xfs_scrub*
%exclude %{_sbindir}/xfs_protofile*
%exclude %{_mandir}/man8/xfs_scrub*
%exclude %{_libexecdir}/xfsprogs/xfs_scrub*
%exclude %{_mandir}/man8/xfs_scrub_all*
%exclude %{_mandir}/man8/xfs_protofile*

%files xfs_scrub
%{_sbindir}/xfs_scrub*
%{_mandir}/man8/xfs_scrub*
%{_libexecdir}/xfsprogs/xfs_scrub*
%{_unitdir}/*
%{_udevrulesdir}/64-xfs.rules
%{_datadir}/xfsprogs/xfs_scrub_all.cron

%files xfs_extras
%{_sbindir}/xfs_protofile*
%{_mandir}/man8/xfs_protofile*

%files devel
%{_mandir}/man2/*
%{_mandir}/man3/*
%dir %{_includedir}/xfs
%{_includedir}/xfs/handle.h
%{_includedir}/xfs/jdm.h
%{_includedir}/xfs/linux.h
%{_includedir}/xfs/xfs.h
%{_includedir}/xfs/xfs_arch.h
%{_includedir}/xfs/xfs_fs.h
%{_includedir}/xfs/xfs_fs_compat.h
%{_includedir}/xfs/xfs_types.h
%{_includedir}/xfs/xfs_format.h
%{_includedir}/xfs/xfs_da_format.h
%{_includedir}/xfs/xfs_log_format.h
%{_includedir}/xfs/xqm.h

%{_libdir}/*.so

%changelog
* Wed Aug 06 2025 František Zatloukal <fzatlouk@redhat.com> - 6.15.0-3
- Rebuilt for icu 77.1

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 24 2025 Pavel Reichl <preichl@redhat.com> - 6.15.0-1
- Rebase to v6.15.0
- Related: rhbz#2374614

* Tue Apr 15 2025 Pavel Reichl <preichl@redhat.com> - 6.14.0-1
- Update to the latest upstream version v6.14
- Related: rhbz#2359550

* Tue Feb 18 2025 Timothée Ravier <tim@siosm.fr> - 6.13.0-2
- Split xfs_protofile into its own sub package (fedora#2346282)
- Move xfs_scrub.slice to xfs_scrub sub package (fedora#2312868)

* Mon Feb 17 2025 Pavel Reichl <preichl@redhat.com> - 6.13.0-1
- Update to the latest upstream version

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 12 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 6.12.0-2
- Rebuilt for the bin-sbin merge (2nd attempt)

* Wed Dec 04 2024 Pavel Reichl <preichl@redhat.com> - 6.12.0-1
- Rebase to upstream version 6.12.0
- Related: rhbz#2330151

* Mon Oct 21 2024 Pavel Reichl <preichl@redhat.com> - 6.11.0-1
- Update to the latest upstream version
- Related: rhbz#2319902

* Thu Sep 05 2024 Eric Sandeen <sandeen@redhat.com> - 6.10.1-1
- Update to latest upstream version
- Fix C++ compilation errors in xfs_fs.h
- Related: rhbz#2309693, rhbz#2308609

* Mon Aug 26 2024 Pavel Reichl <preichl@redhat.com> - 6.10.0-1
- Update to latest upstream version
- Related: rhbz#2307855

* Mon Jul 22 2024 Pavel Reichl <preichl@redhat.com> - 6.9.0-1
- new version

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 6.8.0-3
- Rebuilt for the bin-sbin merge

* Tue May 28 2024 Pavel Reichl <preichl@redhat.com> - 6.8.0-2
- Add missing directories to RPM database
- Related: rhbz#2279737

* Mon May 27 2024 Pavel Reichl <preichl@redhat.com> - 6.8.0-1
- Rebase to the latest upstream version
- Related: rhbz#2280969

* Wed Apr 17 2024 Pavel Reichl <preichl@redhat.com> - 6.7.0-1
- Rebase to upstream version 6.7.0

* Mon Feb 05 2024 Pavel Reichl <preichl@redhat.com> - 6.6.0-1
- Rebase to upstream version 6.6.0
- Related: rhbz#2262783

* Wed Jan 31 2024 Pete Walter <pwalter@fedoraproject.org> - 6.5.0-3
- Rebuild for ICU 74

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Oct 13 2023 Pavel Reichl <preichl@redhat.com> - 6.5.0-1
- Rebase to upstream version 6.5.0

* Tue Oct 03 2023 Pavel Reichl <preichl@redhat.com> - 6.4.0-2
- Convert License tag to SPDX format

* Tue Aug 08 2023 Pavel Reichl <preichl@redhat.com> - 6.4.0-1
- New upstream release (#2223973)

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 6.3.0-2
- Rebuilt for ICU 73.2

* Mon May 22 2023 Eric Sandeen <sandeen@redhat.com> - 6.3.0-1
- New upstream release

* Fri Mar 24 2023 Eric Sandeen <sandeen@redhat.com> - 6.2.0-1
- New upstream release

* Wed Feb 08 2023 Arjun Shankar <arjun@redhat.com> - 6.1.0-3
- Port to C99

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 11 2023 Eric Sandeen <sandeen@redhat.com> - 6.1.0-1
- New upstream release

* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 6.0.0-2
- Rebuild for ICU 72

* Thu Nov 17 2022 Eric Sandeen <sandeen@redhat.com> - 6.0.0-1
- New upstream release
- New GPG public key for tarball signing due to new upstream maintainer

* Fri Aug 12 2022 Eric Sandeen <sandeen@redhat.com> - 5.19.0-1
- New upstream release
- New minimum size requirements in mkfs.xfs

* Mon Aug 01 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 5.18.0-3
- Rebuilt for ICU 71.1

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Eric Sandeen <sandeen@redhat.com> 5.18.0-1
- New upstream release

* Tue May 10 2022 Eric Sandeen <sandeen@redhat.com> 5.16.0-1
- New upstream release

* Wed Apr 06 2022 Eric Sandeen <sandeen@redhat.com> 5.15.0-1
- New upstream release
- Y2038 compatibility (bigtime) on by default in mkfs.xfs

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.14.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 06 2021 Eric Sandeen <sandeen@redhat.com> 5.14.2-1
- New upstream release
- Fixes "fallthrough" macro contamination in xfsprogs-devel linux.h

* Thu Dec 02 2021 Eric Sandeen <sandeen@redhat.com> 5.14.1-1
- New upstream release
- New dependency on userspace-rcu

* Thu Sep 09 2021 Eric Sandeen <sandeen@redhat.com> 5.13.0-2
- Move util-linux/lsblk requirement to scrub package

* Tue Aug 24 2021 Eric Sandeen <sandeen@redhat.com> 5.13.0-1
- New upstream release

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Eric Sandeen <sandeen@redhat.com> 5.12.0-1
- New upstream release

* Thu May 20 2021 Pete Walter <pwalter@fedoraproject.org> - 5.11.0-3
- Rebuild for ICU 69

* Wed May 19 2021 Pete Walter <pwalter@fedoraproject.org> - 5.11.0-2
- Rebuild for ICU 69

* Fri Mar 12 2021 Eric Sandeen <sandeen@redhat.com> 5.11.0-1
- New upstream release

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec 11 2020 Eric Sandeen <sandeen@redhat.com> 5.10.0-1
- New upstream release
- New mkfs config file feature
- Y2038+ format support

* Tue Oct 20 2020 Eric Sandeen <sandeen@redhat.com> 5.9.0-1
- New upstream release

* Fri Sep 04 2020 Eric Sandeen <sandeen@redhat.com> 5.8.0-1
- New upstream release

* Fri Jul 24 2020 Eric Sandeen <sandeen@redhat.com> 5.7.0-1
- New upstream release
- Replace libreadline with libedit
- Add tarball signature checking

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 5.6.0-3
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Sat May 16 2020 Pete Walter <pwalter@fedoraproject.org> - 5.6.0-2
- Rebuild for ICU 67

* Tue Apr 14 2020 Eric Sandeen <sandeen@redhat.com> 5.6.0-1
- New upstream release

* Fri Mar 13 2020 Eric Sandeen <sandeen@redhat.com> 5.5.0-1
- New upstream release

* Fri Jan 31 2020 Eric Sandeen <sandeen@redhat.com> 5.4.0-3
- Fix global redefinitions for gcc10 build

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Eric Sandeen <sandeen@redhat.com> 5.4.0-1
- New upstream release

* Fri Nov 15 2019 Eric Sandeen <sandeen@redhat.com> 5.3.0-1
- New upstream release

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 5.2.1-2
- Rebuild for ICU 65

* Wed Aug 21 2019 Eric Sandeen <sandeen@redhat.com> 5.2.1-1
- New upstream release

* Fri Aug 16 2019 Eric Sandeen <sandeen@redhat.com> 5.2.0-1
- New upstream release

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 19 2019 Eric Sandeen <sandeen@redhat.com> 5.1.0-1
- New upstream release

* Wed May 08 2019 Eric Sandeen <sandeen@redhat.com> 5.0.0-2
- Create new xfs_scrub subpackage (#1666839)

* Fri May 03 2019 Eric Sandeen <sandeen@redhat.com> 5.0.0-1
- New upstream release

* Fri Feb 22 2019 Eric Sandeen <sandeen@redhat.com> 4.20.0-1
- New upstream release

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.19.0-4
- Rebuild for readline 8.0

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Pete Walter <pwalter@fedoraproject.org> - 4.19.0-2
- Rebuild for ICU 63

* Tue Nov 13 2018 Eric Sandeen <sandeen@redhat.com> 4.19.0-1
- New upstream release

* Fri Aug 24 2018 Eric Sandeen <sandeen@redhat.com> 4.18.0-1
- New upstream release

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.17.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 4.17.0-2
- Rebuild for ICU 62

* Thu Jun 28 2018 Eric Sandeen <sandeen@redhat.com> 4.17.0-1
- New upstream release

* Mon Apr 30 2018 Pete Walter <pwalter@fedoraproject.org> - 4.16.0-2
- Rebuild for ICU 61.1

* Thu Apr 26 2018 Eric Sandeen <sandeen@redhat.com> 4.16.0-1
- New upstream release
- Clean up specfile

* Mon Feb 26 2018 Eric Sandeen <sandeen@redhat.com> 4.15.1-1
- New upstream release
- Update Polish translation

* Mon Feb 26 2018 Eric Sandeen <sandeen@redhat.com> 4.15.0-2
- BuildRequires: gcc

* Sat Feb 24 2018 Eric Sandeen <sandeen@redhat.com> 4.15.0-1
- New upstream release
- Adds new xfs_scrub utility and services

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Nov 27 2017 Eric Sandeen <sandeen@redhat.com> 4.14.0-1
- New upstream release

* Wed Sep 27 2017 Eric Sandeen <sandeen@redhat.com> 4.13.1-1
- New upstream release
- Trim ancient changelog

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 4.12.0-3
- Rebuild with binutils fix for ppc64le (#1475636)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Eric Sandeen <sandeen@redhat.com> 4.12.0-1
- New upstream release

* Fri May 05 2017 Eric Sandeen <sandeen@redhat.com> 4.11.0-1
- New upstream release

* Sun Feb 26 2017 Eric Sandeen <sandeen@redhat.com> 4.10.0-1
- New upstream release

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 4.9.0-2
- Rebuild for readline 7.x

* Thu Jan 05 2017 Eric Sandeen <sandeen@redhat.com> 4.9.0-1
- New upstream release

* Tue Oct 18 2016 Eric Sandeen <sandeen@redhat.com> 4.8.0-1
- New upstream release

* Tue Sep 06 2016 Eric Sandeen <sandeen@redhat.com> 4.7.0-2
- Add libattr-devel build dependency to fix xfs_fsr

* Sun Sep 04 2016 Eric Sandeen <sandeen@redhat.com> 4.7.0-1
- New upstream release

* Tue Mar 15 2016 Eric Sandeen <sandeen@redhat.com> 4.5.0-1
- New upstream release

* Thu Mar 10 2016 Eric Sandeen <sandeen@redhat.com> 4.3.0-3
- Fix build w/ new kernels which have [sg]etxattr promotion

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 30 2015 Eric Sandeen <sandeen@redhat.com> 4.3.0-1
- New upstream release

* Wed Sep 09 2015 Eric Sandeen <sandeen@redhat.com> 4.2.0-1
- New upstream release

* Thu Jul 30 2015 Eric Sandeen <sandeen@redhat.com> 3.2.4-1
- New upstream release
- Addresses CVE-2012-2150 for xfs_metadump

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Eric Sandeen <sandeen@redhat.com> 3.2.3-1
- New upstream release
