# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: Tracks and displays system calls associated with a running process
Name: strace
Version: 6.19
Release: 2%{?dist}
# The test suite is GPLv2+, the bundled headers are GPLv2 with Linux syscall
# exception, all the rest is LGPLv2.1+.
%if 0%{?fedora} >= 35 || 0%{?centos} >= 9 || 0%{?rhel} >= 9
# https://docs.fedoraproject.org/en-US/legal/license-field/#_no_effective_license_analysis
# BSD-2-Clause:
#   bundled/linux/include/uapi/linux/tee.h
# BSD-3-Clause:
#   bundled/linux/include/uapi/linux/quota.h
# GPL-1.0-or-later WITH Linux-syscall-note:
#   bundled/linux/include/uapi/linux/if_bonding.h
#   bundled/linux/include/uapi/linux/loop.h
# GPL-2.0-or-later WITH Linux-syscall-note:
#   bundled/linux/include/uapi/linux/dm-ioctl.h
#   bundled/linux/include/uapi/linux/hiddev.h
#   bundled/linux/include/uapi/linux/if_alg.h
#   bundled/linux/include/uapi/linux/if_bridge.h
#   bundled/linux/include/uapi/linux/in6.h
#   bundled/linux/include/uapi/linux/in.h
#   bundled/linux/include/uapi/linux/keyctl.h
#   bundled/linux/include/uapi/linux/mptcp.h
#   bundled/linux/include/uapi/linux/ptp_clock.h
#   bundled/linux/include/uapi/linux/tcp.h
#   bundled/linux/include/uapi/mtd/mtd-abi.h
#   bundled/linux/include/uapi/mtd/ubi-user.h
# LGPL-2.0-or-later WITH Linux-syscall-note:
#   bundled/linux/include/uapi/linux/dm-ioctl.h
# LGPL-2.1-or-later WITH Linux-syscall-note:
#   bundled/linux/include/uapi/linux/dqblk_xfs.h
#   bundled/linux/include/uapi/linux/mqueue.h
# (GPL-2.0-only WITH Linux-syscall-note) OR Linux-OpenIB:
#   bundled/linux/include/uapi/linux/tls.h
#   bundled/linux/include/uapi/rdma/ib_user_verbs.h
# (GPL-2.0-only WITH Linux-syscall-note) OR MIT:
#   bundled/linux/include/uapi/linux/io_uring.h
# (GPL-2.0-or-later WITH Linux-syscall-note) OR BSD-3-Clause:
#   bundled/linux/include/uapi/linux/v4l2-common.h
#   bundled/linux/include/uapi/linux/v4l2-controls.h
#   bundled/linux/include/uapi/linux/videodev2.h
# GPL-2.0-only WITH Linux-syscall-note:
#   bundled/linux/include/uapi/asm-generic/hugetlb_encode.h (no explicit license in the file)
#   bundled/linux/include/uapi/linux/mount.h (no explicit license in the file)
#   bundled/linux/include/uapi/linux/netfilter/nfnetlink_osf.h (no explicit license in the file)
#   bundled/linux/include/uapi/linux/version.h (no explicit license in the file)
#   bundled/linux/include/uapi/asm/hugetlb_encode.h (no explicit license in the file)
#   the rest of bundled/linux
# ISC:
#   bundled/linux/include/uapi/linux/nfc.h
# X11:
#   build-aux/install-sh (dist only)
# LGPL-2.1-or-later:
#   build-aux/copyright-year-gen
#   build-aux/file-date-gen
#   m4/ax_code_coverage.m4
#   m4/mpers.m4
#   m4/st_demangle.m4
#   m4/st_esyscmd_s.m4
#   m4/st_libdw.m4
#   m4/st_libunwind.m4
#   m4/st_save_restore_var.m4
#   m4/st_selinux.m4
#   m4/st_stacktrace.m4
#   m4/st_warn_cflags.m4
# GPL-2.0-or-later:
#   build-aux/ar-lib (dist only)
#   build-aux/compile (dist only)
#   build-aux/depcomp (dist only)
#   build-aux/missing (dist only)
#   build-aux/test-driver (dist only)
# GPL-3.0-or-later:
#   build-aux/config.guess (dist only)
#   build-aux/config.sub (dist only)
#   build-aux/git-version-gen
# FSFAP:
#   README-configure
#   m4/ax_prog_cc_for_build.m4
#   m4/ax_valgrind_check.m4
# FSFUL:
#   configure (dist only)
# FSFULLR:
#   m4/warnings.m4
# FSFULLRWD:
#   aclocal.m4 (dist only)
#   Makefile.in (dist only)
#   bundled/Makefile.in (dist only)
#   src/Makefile.in (dist only)
#   tests/Makefile.in (dist only)
#   tests-m32/Makefile.in (dist only)
#   tests-mx32/Makefile.in (dist only)
License: LGPL-2.1-or-later AND GPL-2.0-or-later AND GPL-3.0-or-later AND BSD-2-Clause AND BSD-3-Clause AND (GPL-1.0-or-later WITH Linux-syscall-note) AND (GPL-2.0-or-later WITH Linux-syscall-note) AND (GPL-2.0-only WITH Linux-syscall-note) AND (LGPL-2.0-or-later WITH Linux-syscall-note) AND (LGPL-2.1-or-later WITH Linux-syscall-note) AND ((GPL-2.0-only WITH Linux-syscall-note) OR Linux-OpenIB) AND ((GPL-2.0-only WITH Linux-syscall-note) OR MIT) AND ((GPL-2.0-or-later WITH Linux-syscall-note) OR BSD-3-Clause) AND ISC AND X11 AND FSFAP AND FSFUL AND FSFULLR AND FSFULLRWD
%else
License: LGPL-2.1+ and GPL-2.0+
%endif
# Some distros require Group tag to be present,
# some require Group tag to be absent,
# some do not care about Group tag at all,
# and we have to cater for all of them.
%if 0%{?fedora} < 28 && 0%{?centos} < 8 && 0%{?rhel} < 8 && 0%{?suse_version} < 1500
Group: Development%{?suse_version:/Tools}/Debuggers
%endif
URL: https://strace.io
%if 0%{?fedora} >= 12 || 0%{?centos} >= 6 || 0%{?rhel} >= 6 || 0%{?suse_version} >= 1200
Source: https://strace.io/files/%{version}/strace-%{version}.tar.xz
BuildRequires: xz
%else
Source: strace-%{version}.tar.gz
%endif
BuildRequires: gcc gzip make

# Install Bluetooth headers for AF_BLUETOOTH sockets decoding.
%if 0%{?fedora} >= 18 || 0%{?centos} >= 6 || 0%{?rhel} >= 8 || 0%{?suse_version} >= 1200
BuildRequires: pkgconfig(bluez)
%endif

# Install elfutils-devel or libdw-devel to enable strace -k option.
# Install binutils-devel to enable symbol demangling.
%if 0%{?fedora} >= 20 || 0%{?centos} >= 6 || 0%{?rhel} >= 6
%define buildrequires_stacktrace BuildRequires: elfutils-devel binutils-devel
%define buildrequires_selinux BuildRequires: libselinux-devel
%endif
%if 0%{?suse_version} >= 1100
%define buildrequires_stacktrace BuildRequires: libdw-devel binutils-devel
%define buildrequires_selinux BuildRequires: libselinux-devel
%endif
%{?buildrequires_stacktrace}
%{?buildrequires_selinux}

# OBS compatibility
%{?!buildroot:BuildRoot: %_tmppath/buildroot-%name-%version-%release}
%define maybe_use_defattr %{?suse_version:%%defattr(-,root,root)}

# Fallback definitions for make_build/make_install macros
%{?!__make:       %global __make %_bindir/make}
%{?!__install:    %global __install %_bindir/install}
%{?!make_build:   %global make_build %__make %{?_smp_mflags}}
%{?!make_install: %global make_install %__make install DESTDIR="%{?buildroot}" INSTALL="%__install -p"}

%description
The strace program intercepts and records the system calls called and
received by a running process.  Strace can print a record of each
system call, its arguments and its return value.  Strace is useful for
diagnosing problems and debugging, as well as for instructional
purposes.

Install strace if you need a tool to track the system calls made and
received by a process.

%prep
%setup -q
echo -n %version-%release > .tarball-version
echo -n 2026 > .year
echo -n 2025-11-13 > doc/.strace.1.in.date
echo -n 2025-07-02 > doc/.strace-log-merge.1.in.date

%build
echo 'BEGIN OF BUILD ENVIRONMENT INFORMATION'
uname -a |head -1
libc="$(ldd /bin/sh |sed -n 's|^[^/]*\(/[^ ]*/libc\.so[^ ]*\).*|\1|p' |head -1)"
$libc |head -1
file -L /bin/sh
gcc --version |head -1
ld --version |head -1
kver="$(printf '%%s\n%%s\n' '#include <linux/version.h>' 'LINUX_VERSION_CODE' | gcc -E -P -)"
printf 'kernel-headers %%s.%%s.%%s\n' $((kver/65536)) $((kver/256%%256)) $((kver%%256))
echo 'END OF BUILD ENVIRONMENT INFORMATION'

CFLAGS_FOR_BUILD="$RPM_OPT_FLAGS"; export CFLAGS_FOR_BUILD
%configure --enable-mpers=check --enable-bundled=yes
%make_build

%install
%make_install

# some say uncompressed changelog files are too big
for f in ChangeLog ChangeLog-CVS; do
	gzip -9n < "$f" > "$f".gz &
done
wait

%check
width=$(echo __LONG_WIDTH__ |%__cc -E -P -)
skip_32bit=0
%if 0%{?fedora} >= 35 || 0%{?rhel} > 9
skip_32bit=1
%endif

if [ "${width}" != 32 ] || [ "${skip_32bit}" != 1 ]; then
	%{buildroot}%{_bindir}/strace -V
	%make_build -k check VERBOSE=1
	echo 'BEGIN OF TEST SUITE INFORMATION'
	tail -n 99999 -- tests*/test-suite.log tests*/ksysent.gen.log
	find tests* -type f -name '*.log' -print0 |
		xargs -r0 grep -H '^KERNEL BUG:' -- ||:
	echo 'END OF TEST SUITE INFORMATION'
fi

%files
%maybe_use_defattr
%doc CREDITS ChangeLog.gz ChangeLog-CVS.gz COPYING NEWS README
%{_bindir}/strace
%{_bindir}/strace-log-merge
%{_mandir}/man1/*

%changelog
* Tue Feb 10 2026 Dmitry V. Levin <ldv@strace.io> - 6.19-1
- v6.18 -> v6.19 (resolves: #2435125).

* Sun Dec 07 2025 Dmitry V. Levin <ldv@strace.io> - 6.18-1
- v6.17 -> v6.18 (resolves: #2341392).

* Mon Sep 29 2025 Dmitry V. Levin <ldv@strace.io> - 6.17-1
- v6.16 -> v6.17.

* Tue Aug 05 2025 Dmitry V. Levin <ldv@strace.io> - 6.16-1
- v6.15 -> v6.16.

* Mon May 26 2025 Dmitry V. Levin <ldv@strace.io> - 6.15-1
- v6.14 -> v6.15.

* Tue Mar 25 2025 Dmitry V. Levin <ldv@strace.io> - 6.14-1
- v6.13 -> v6.14.

* Thu Jan 23 2025 Dmitry V. Levin <ldv@strace.io> - 6.13-1
- v6.12 -> v6.13 (resolves: #2341392).

* Mon Nov 18 2024 Dmitry V. Levin <ldv@strace.io> - 6.12-1
- v6.11 -> v6.12.

* Mon Oct 28 2024 Florian Weimer <fweimer@redhat.com> - 6.11-3
- Backport upstream patch for compatibility with kernel MAP_DENYWRITE changes

* Fri Oct 25 2024 Florian Weimer <fweimer@redhat.com> - 6.11-2
- Fix FTBFS with glibc 2.41 (#2317070)

* Sun Sep 15 2024 Dmitry V. Levin <ldv@strace.io> - 6.11-1
- v6.10 -> v6.11.

* Sun Jul 21 2024 Dmitry V. Levin <ldv@strace.io> - 6.10-1
- v6.9 -> v6.10.

* Tue May 14 2024 Dmitry V. Levin <ldv@strace.io> - 6.9-1
- v6.8 -> v6.9.

* Wed Mar 20 2024 Dmitry V. Levin <ldv@strace.io> - 6.8-1
- v6.7 -> v6.8.

* Mon Jan 29 2024 Dmitry V. Levin <ldv@strace.io> - 6.7-1
- v6.6 -> v6.7.

* Tue Oct 31 2023 Dmitry V. Levin <ldv@strace.io> - 6.6-1
- v6.5 -> v6.6 (resolves: #2243631).

* Fri Sep 01 2023 Dmitry V. Levin <ldv@strace.io> - 6.5-1
- v6.4 -> v6.5.
- Updated the SPDX license expression (by Eugene Syromyatnikov).

* Mon Jun 26 2023 Dmitry V. Levin <ldv@strace.io> - 6.4-1
- v6.3 -> v6.4.

* Mon May 08 2023 Dmitry V. Levin <ldv@strace.io> - 6.3-1
- v6.2 -> v6.3.

* Sun Feb 26 2023 Dmitry V. Levin <ldv@strace.io> - 6.2-1
- v6.1 -> v6.2.

* Mon Dec 12 2022 Dmitry V. Levin <ldv@strace.io> - 6.1-1
- v6.0 -> v6.1.

* Sat Oct 29 2022 Dmitry V. Levin <ldv@strace.io> - 6.0-1
- v5.19 -> v6.0.

* Fri Aug 12 2022 Dmitry V. Levin <ldv@strace.io> - 5.19-1
- v5.18 -> v5.19.

* Sat Jun 18 2022 Dmitry V. Levin <ldv@strace.io> - 5.18-1
- v5.17 -> v5.18.

* Sat Mar 26 2022 Dmitry V. Levin <ldv@strace.io> - 5.17-1
- v5.16 -> v5.17 (resolves: #2047030).

* Mon Jan 10 2022 Dmitry V. Levin <ldv@strace.io> - 5.16-1
- v5.15 -> v5.16.

* Wed Dec 01 2021 Dmitry V. Levin <ldv@strace.io> - 5.15-1
- v5.14 -> v5.15.

* Thu Sep 02 2021 Dmitry V. Levin <ldv@strace.io> - 5.14-1
- v5.13 -> v5.14.

* Sun Jul 18 2021 Dmitry V. Levin <ldv@strace.io> - 5.13-1
- v5.12 -> v5.13.

* Mon Apr 26 2021 Dmitry V. Levin <ldv@strace.io> - 5.12-1
- v5.11 -> v5.12.

* Wed Feb 17 2021 Dmitry V. Levin <ldv@strace.io> - 5.11-1
- v5.10 -> v5.11.

* Mon Dec 14 2020 Dmitry V. Levin <ldv@strace.io> - 5.10-1
- v5.9 -> v5.10.

* Thu Sep 24 2020 Dmitry V. Levin <ldv@strace.io> - 5.9-1
- v5.8 -> v5.9.

* Thu Aug 06 2020 Dmitry V. Levin <ldv@strace.io> - 5.8-1
- v5.7 -> v5.8.

* Mon Jun 01 2020 Dmitry V. Levin <ldv@strace.io> - 5.7-1
- v5.6 -> v5.7.

* Tue Apr 07 2020 Dmitry V. Levin <ldv@strace.io> - 5.6-1
- v5.5 -> v5.6.

* Thu Feb 06 2020 Dmitry V. Levin <ldv@strace.io> - 5.5-1
- v5.4 -> v5.5.

* Thu Nov 28 2019 Dmitry V. Levin <ldv@strace.io> - 5.4-1
- v5.3 -> v5.4.

* Wed Sep 25 2019 Dmitry V. Levin <ldv@strace.io> - 5.3-1
- v5.2 -> v5.3.

* Fri Jul 12 2019 Dmitry V. Levin <ldv@strace.io> - 5.2-1
- v5.1 -> v5.2.

* Wed May 22 2019 Dmitry V. Levin <ldv@strace.io> - 5.1-1
- v5.0 -> v5.1.

* Tue Mar 19 2019 Dmitry V. Levin <ldv@strace.io> - 5.0-1
- v4.26 -> v5.0 (resolves: #478419, #526740, #851457, #1609318,
  #1610774, #1662936, #1676045).

* Wed Dec 26 2018 Dmitry V. Levin <ldv@strace.io> - 4.26-1
- v4.25 -> v4.26.

* Tue Oct 30 2018 Dmitry V. Levin <ldv@strace.io> - 4.25-1
- v4.24 -> v4.25.

* Tue Aug 14 2018 Dmitry V. Levin <ldv@strace.io> - 4.24-1
- v4.23 -> v4.24.

* Thu Jun 14 2018 Dmitry V. Levin <ldv@strace.io> - 4.23-1
- v4.22 -> v4.23.
- Enabled libdw backend for -k option (#1568647).

* Thu Apr 05 2018 Dmitry V. Levin <ldv@strace.io> - 4.22-1
- v4.21 -> v4.22.

* Tue Feb 13 2018 Dmitry V. Levin <ldv@strace.io> - 4.21-1
- v4.20 -> v4.21.

* Mon Nov 13 2017 Dmitry V. Levin <ldv@strace.io> - 4.20-1
- v4.19 -> v4.20.

* Tue Sep 05 2017 Dmitry V. Levin <ldv@strace.io> - 4.19-1
- v4.18 -> v4.19.

* Wed Jul 05 2017 Dmitry V. Levin <ldv@strace.io> - 4.18-1
- v4.17 -> v4.18.

* Wed May 24 2017 Dmitry V. Levin <ldv@strace.io> - 4.17-1
- v4.16 -> v4.17.

* Tue Feb 14 2017 Dmitry V. Levin <ldv@strace.io> - 4.16-1
- v4.15 -> v4.16.

* Wed Dec 14 2016 Dmitry V. Levin <ldv@strace.io> - 4.15-1
- v4.14-100-g622af42 -> v4.15.

* Wed Nov 16 2016 Dmitry V. Levin <ldv@strace.io> - 4.14.0.100.622a-1
- v4.14 -> v4.14-100-g622af42:
  + implemented syscall fault injection.

* Tue Oct 04 2016 Dmitry V. Levin <ldv@strace.io> - 4.14-1
- v4.13 -> v4.14:
  + added printing of the mode argument of open and openat syscalls
    when O_TMPFILE flag is set (#1377846).

* Tue Jul 26 2016 Dmitry V. Levin <ldv@strace.io> - 4.13-1
- v4.12 -> v4.13.

* Tue May 31 2016 Dmitry V. Levin <ldv@strace.io> - 4.12-1
- v4.11-163-g972018f -> v4.12.

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.0.163.9720-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Dmitry V. Levin <ldv@strace.io> - 4.11.0.163.9720-1
- New upstream snapshot v4.11-163-g972018f:
  + fixed decoding of syscalls unknown to the kernel on s390/s390x (#1298294).

* Wed Dec 23 2015 Dmitry V. Levin <ldv@strace.io> - 4.11-2
- Enabled experimental -k option on x86_64 (#1170296).

* Mon Dec 21 2015 Dmitry V. Levin <ldv@strace.io> - 4.11-1
- New upstream release:
  + print nanoseconds along with seconds in stat family syscalls (#1251176).

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 11 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 4.10-2
- Backport set of upstream patches to get it buildable on AArch64

* Fri Mar 06 2015 Dmitry V. Levin <ldv@strace.io> - 4.10-1
- New upstream release:
  + enhanced ioctl decoding (#902788).

* Mon Nov 03 2014 Lubomir Rintel <lkundrak@v3.sk> - 4.9-3
- Regenerate ioctl entries with proper kernel headers

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Dmitry V. Levin <ldv@strace.io> - 4.9-1
- New upstream release:
  + fixed build when <sys/ptrace.h> and <linux/ptrace.h> conflict (#993384);
  + updated CLOCK_* constants (#1088455);
  + enabled ppc64le support (#1122323);
  + fixed attach to a process on ppc64le (#1129569).

* Fri Jul 25 2014 Dan Horák <dan[at]danny.cz> - 4.8-5
- update for ppc64

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Dec  6 2013 Peter Robinson <pbrobinson@fedoraproject.org> 4.8-3
- Fix FTBFS

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 03 2013 Dmitry V. Levin <ldv@strace.io> - 4.8-1
- New upstream release:
  + fixed ERESTARTNOINTR leaking to userspace on ancient kernels (#659382);
  + fixed decoding of *xattr syscalls (#885233);
  + fixed handling of files with 64-bit inode numbers by 32-bit strace (#912790);
  + added aarch64 support (#969858).

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 02 2012 Dmitry V. Levin <ldv@strace.io> 4.7-1
- New upstream release.
  + implemented proper handling of real SIGTRAPs (#162774).

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Mar 14 2011 Dmitry V. Levin <ldv@strace.io> - 4.6-1
- New upstream release.
  + fixed a corner case in waitpid handling (#663547).

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Apr 13 2010 Roland McGrath <roland@redhat.com> - 4.5.20-1
- New upstream release, work mostly by Andreas Schwab and Dmitry V. Levin.
  + fixed potential stack buffer overflow in select decoder (#556678);
  + fixed FTBFS (#539044).

* Wed Oct 21 2009 Roland McGrath <roland@redhat.com> - 4.5.19-1
- New upstream release, work mostly by Dmitry V. Levin <ldv@strace.io>
  + exit/kill strace with traced process exitcode/signal (#105371);
  + fixed build on ARM EABI (#507576);
  + fixed display of 32-bit argv array on 64-bit architectures (#519480);
  + fixed display of 32-bit fcntl(F_SETLK) on 64-bit architectures (#471169);
  + fixed several bugs in strings decoder, including potential heap
    memory corruption (#470529, #478324, #511035).

* Thu Aug 28 2008 Roland McGrath <roland@redhat.com> - 4.5.18-1
- build fix for newer kernel headers (#457291)
- fix CLONE_VFORK handling (#455078)
- Support new Linux/PPC system call subpage_prot and PROT_SAO flag.
- In sigaction system call, display sa_flags value along with SIG_DFL/SIG_IGN.

* Mon Jul 21 2008 Roland McGrath <roland@redhat.com> - 4.5.17-1
- handle O_CLOEXEC, MSG_CMSG_CLOEXEC (#365781)
- fix biarch stat64 decoding (#222275)
- fix spurious "..." in printing of environment strings (#358241)
- improve prctl decoding (#364401)
- fix hang wait on exited child with exited child (#354261)
- fix biarch fork/vfork (-f) tracing (#447475)
- fix biarch printing of negative argument kill (#430585)
- fix biarch decoding of error return values (#447587)
- fix -f tracing of CLONE_VFORK (#455078)
- fix ia64 register clobberation in -f tracing (#453438)
- print SO_NODEFER, SA_RESETHAND instead of SA_NOMASK, SA_ONESHOT (#455821)
- fix futex argument decoding (#448628, #448629)

* Fri Aug  3 2007 Roland McGrath <roland@redhat.com> - 4.5.16-1
- fix multithread issues (#240962, #240961, #247907)
- fix spurious SIGSTOP on early interrupt (#240986)
- fix utime for biarch (#247185)
- fix -u error message (#247170)
- better futex syscall printing (##241467)
- fix argv/envp printing with small -s settings, and for biarch
- new syscalls: getcpu, eventfd, timerfd, signalfd, epoll_pwait,
  move_pages, utimensat

* Tue Jan 16 2007 Roland McGrath <roland@redhat.com> - 4.5.15-1
- biarch fixes (#179740, #192193, #171626, #173050, #218433, #218043)
- fix -ff -o behavior (#204950, #218435, #193808, #219423)
- better quotactl printing (#118696)
- *at, inotify*, pselect6, ppoll and unshare syscalls (#178633, #191275)
- glibc-2.5 build fixes (#209856)
- memory corruption fixes (#200621
- fix race in child setup under -f (#180293)
- show ipc key values in hex (#198179, #192182)
- disallow -c with -ff (#187847)
- Resolves: RHBZ #179740, RHBZ #192193, RHBZ #204950, RHBZ #218435
- Resolves: RHBZ #193808, RHBZ #219423, RHBZ #171626, RHBZ #173050
- Resolves: RHBZ #218433, RHBZ #218043, RHBZ #118696, RHBZ #178633
- Resolves: RHBZ #191275, RHBZ #209856, RHBZ #200621, RHBZ #180293
- Resolves: RHBZ #198179, RHBZ #198182, RHBZ #187847

* Mon Nov 20 2006 Jakub Jelinek <jakub@redhat.com> - 4.5.14-4
- Fix ia64 syscall decoding (#206768)
- Fix build with glibc-2.4.90-33 and up on all arches but ia64
- Fix build against 2.6.18+ headers

* Tue Aug 22 2006 Roland McGrath <roland@redhat.com> - 4.5.14-3
- Fix bogus decoding of syscalls >= 300 (#201462, #202620).

* Fri Jul 14 2006 Jesse Keating <jkeating@redhat.com> - 4.5.14-2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.5.14-1.2
- bump again for long double bug on ppc{,64}

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.5.14-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 16 2006 Roland McGrath <roland@redhat.com> - 4.5.14-1
- Fix biarch decoding of socket syscalls (#174354).
- Fix biarch -e support (#173986).
- Accept numeric syscalls in -e (#174798).
- Fix ipc syscall decoding (#164755).
- Improve msgrcv printing (#164757).
- Man page updates (#165375).
- Improve mount syscall printing (#165377).
- Correct printing of restarting syscalls (#165469).

* Wed Aug  3 2005 Roland McGrath <roland@redhat.com> - 4.5.13-1
- Fix setsockopt decoding on 64-bit (#162449).
- Fix typos in socket option name strings (#161578).
- Display more IPV6 socket options by name (#162450).
- Don't display inappropriate syscalls for -e trace=file (#159340).
- New selector type -e trace=desc for file-descriptor using calls (#159400).
- Fix 32-bit old_mmap syscall decoding on x86-64 (#162467, #164215).
- Fix errors detaching from multithreaded process on interrupt (#161919).
- Note 4.5.12 fix for crash handling bad signal numbers (#162739).

* Wed Jun  8 2005 Roland McGrath <roland@redhat.com> - 4.5.12-1
- Fix known syscall recognition for IA32 processes on x86-64 (#158934).
- Fix bad output for ptrace on x86-64 (#159787).
- Fix potential buffer overruns (#151570, #159196).
- Make some diagnostics more consistent (#159308).
- Update PowerPC system calls.
- Better printing for Linux aio system calls.
- Don't truncate statfs64 fields to 32 bits in output (#158243).
- Cosmetic code cleanups (#159688).

* Tue Mar 22 2005 Roland McGrath <roland@redhat.com> - 4.5.11-1
- Build tweaks.
- Note 4.5.10 select fix (#151570).

* Mon Mar 14 2005 Roland McGrath <roland@redhat.com> - 4.5.10-1
- Fix select handling on nonstandard fd_set sizes.
- Don't print errors for null file name pointers.
- Fix initial execve output with -i (#143365).

* Fri Feb  4 2005 Roland McGrath <roland@redhat.com> - 4.5.9-2
- update ia64 syscall list (#146245)
- fix x86_64 syscall argument extraction for 32-bit processes (#146093)
- fix -e signal=NAME parsing (#143362)
- fix x86_64 exit_group syscall handling
- improve socket ioctl printing (#138223)
- code cleanups (#143369, #143370)
- improve mount flags printing (#141932)
- support symbolic printing of x86_64 arch_prctl parameters (#142667)
- fix potential crash in getxattr printing

* Tue Oct 19 2004 Roland McGrath <roland@redhat.com> - 4.5.8-1
- fix multithreaded exit handling (#132150, #135254)
- fix ioctl name matching (#129808)
- print RTC_* ioctl structure contents (#58606)
- grok epoll_* syscalls (#134463)
- grok new RLIMIT_* values (#133594)
- print struct cmsghdr contents for sendmsg (#131689)
- fix clock_* and timer_* argument output (#131420)

* Tue Aug 31 2004 Roland McGrath <roland@redhat.com> - 4.5.7-2
- new upstream version, misc fixes and updates (#128091, #129166, #128391, #129378, #130965, #131177)

* Mon Jul 12 2004 Roland McGrath <roland@redhat.com> 4.5.6-1
- new upstream version, updates ioctl lists (#127398), fixes quotactl (#127393), more ioctl decoding (#126917)

* Sun Jun 27 2004 Roland McGrath <roland@redhat.com> 4.5.5-1
- new upstream version, fixes x86-64 biarch support (#126547)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com> 4.5.4-2
- rebuilt

* Thu Jun  3 2004 Roland McGrath <roland@redhat.com> 4.5.4-0.FC1
- rebuilt for FC1 update

* Thu Jun  3 2004 Roland McGrath <roland@redhat.com> 4.5.4-1
- new upstream version, more ioctls (#122257), minor fixes

* Fri Apr 16 2004 Roland McGrath <roland@redhat.com> 4.5.3-1
- new upstream version, mq_* calls (#120701), -p vs NPTL (#120462), more fixes (#118694, #120541, #118685)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com> 4.5.2-1.1
- rebuilt

* Mon Mar  1 2004 Roland McGrath <roland@redhat.com> 4.5.2-1
- new upstream version, sched_* calls (#116990), show core flag (#112117)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Nov 13 2003 Roland McGrath <roland@redhat.com> 4.5.1-1
- new upstream version, more fixes (#108012, #105366, #105359, #105358)

* Tue Sep 30 2003 Roland McGrath <roland@redhat.com> 4.5-3
- revert bogus s390 fix

* Thu Sep 25 2003 Roland McGrath <roland@redhat.com> 4.5-1.2.1AS
- rebuilt for 2.1AS erratum

* Wed Sep 24 2003 Roland McGrath <roland@redhat.com> 4.5-2
- rebuilt

* Wed Sep 24 2003 Roland McGrath <roland@redhat.com> 4.5-1
- new upstream version, more fixes (#101499, #104365)

* Thu Jul 17 2003 Roland McGrath <roland@redhat.com> 4.4.99-2
- rebuilt

* Thu Jul 17 2003 Roland McGrath <roland@redhat.com> 4.4.99-1
- new upstream version, groks more new system calls, PF_INET6 sockets

* Tue Jun 10 2003 Roland McGrath <roland@redhat.com> 4.4.98-1
- new upstream version, more fixes (#90754, #91085)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Mar 30 2003 Roland McGrath <roland@redhat.com> 4.4.96-1
- new upstream version, handles yet more 2.5 syscalls, x86_64 & ia64 fixes

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com> 4.4.95-2
- rebuilt

* Mon Feb 24 2003 Roland McGrath <roland@redhat.com> 4.4.95-1
- new upstream version, fixed getresuid/getresgid (#84959)

* Wed Feb 19 2003 Roland McGrath <roland@redhat.com> 4.4.94-1
- new upstream version, new option -E to set environment variables (#82392)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 4.4.93-2
- rebuilt

* Tue Jan 21 2003 Roland McGrath <roland@redhat.com> 4.4.93-1
- new upstream version, fixes ppc and s390 bugs, adds missing ptrace requests

* Fri Jan 10 2003 Roland McGrath <roland@redhat.com> 4.4.91-1
- new upstream version, fixes -f on x86-64

* Fri Jan 10 2003 Roland McGrath <roland@redhat.com> 4.4.90-1
- new upstream version, fixes all known bugs modulo ia64 and s390 issues

* Fri Jan 03 2003 Florian La Roche <Florian.LaRoche@redhat.de> 4.4-11
- add further s390 patch from IBM

* Wed Nov 27 2002 Tim Powers <timp@redhat.com> 4.4-10
- remove unpackaged files from the buildroot

* Mon Oct 07 2002 Phil Knirsch <pknirsch@redhat.com> 4.4-9.1
- Added latest s390(x) patch.

* Fri Sep 06 2002 Karsten Hopp <karsten@redhat.de> 4.4-9
- preliminary x86_64 support with an ugly patch to help
  debugging. Needs cleanup!

* Mon Sep  2 2002 Jakub Jelinek <jakub@redhat.com> 4.4-8
- newer version of the clone fixing patch (Roland McGrath)
- aio syscalls for i386/ia64/ppc (Ben LaHaise)

* Wed Aug 28 2002 Jakub Jelinek <jakub@redhat.com> 4.4-7
- fix strace -f (Roland McGrath, #68994)
- handle ?et_thread_area, SA_RESTORER (Ulrich Drepper)

* Fri Jun 21 2002 Jakub Jelinek <jakub@redhat.com> 4.4-6
- handle futexes, *xattr, sendfile64, etc. (Ulrich Drepper)
- handle modify_ldt (#66894)

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Apr 16 2002 Jakub Jelinek <jakub@redhat.com> 4.4-4
- fix for the last patch by Jeff Law (#62591)

* Mon Mar  4 2002 Preston Brown <pbrown@redhat.com> 4.4-3
- integrate patch from Jeff Law to eliminate hang tracing threads

* Sat Feb 23 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- minor update from debian tar-ball

* Wed Jan 02 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 4.4

* Sun Jul 22 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- disable s390 patches, they are already included

* Wed Jul 18 2001 Preston Brown <pbrown@redhat.com> 4.3-1
- new upstream version.  Seems to have integrated most new syscalls
- tracing threaded programs is now functional.

* Mon Jun 11 2001 Than Ngo <than@redhat.com>
- port s390 patches from IBM

* Wed May 16 2001 Nalin Dahyabhai <nalin@redhat.com>
- modify new syscall patch to allocate enough heap space in setgroups32()

* Wed Feb 14 2001 Jakub Jelinek <jakub@redhat.com>
- #include <time.h> in addition to <sys/time.h>

* Fri Jan 26 2001 Karsten Hopp <karsten@redhat.com>
- clean up conflicting patches. This happened only
  when building on S390

* Fri Jan 19 2001 Bill Nottingham <notting@redhat.com>
- update to CVS, reintegrate ia64 support

* Fri Dec  8 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Get S/390 support into the normal package

* Sat Nov 18 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- added S/390 patch from IBM, adapting it to not conflict with
  IA64 patch

* Sat Aug 19 2000 Jakub Jelinek <jakub@redhat.com>
- doh, actually apply the 2.4 syscalls patch
- make it compile with 2.4.0-test7-pre4+ headers, add
  getdents64 and fcntl64

* Thu Aug  3 2000 Jakub Jelinek <jakub@redhat.com>
- add a bunch of new 2.4 syscalls (#14036)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild
- excludearch ia64

* Fri Jun  2 2000 Matt Wilson <msw@redhat.com>
- use buildinstall for FHS

* Wed May 24 2000 Jakub Jelinek <jakub@redhat.com>
- make things compile on sparc
- fix sigreturn on sparc

* Fri Mar 31 2000 Bill Nottingham <notting@redhat.com>
- fix stat64 misdef (#10485)

* Tue Mar 21 2000 Michael K. Johnson <johnsonm@redhat.com>
- added ia64 patch

* Thu Feb 03 2000 Cristian Gafton <gafton@redhat.com>
- man pages are compressed
- version 4.2 (why are we keeping all these patches around?)

* Sat Nov 27 1999 Jeff Johnson <jbj@redhat.com>
- update to 4.1 (with sparc socketcall patch).

* Fri Nov 12 1999 Jakub Jelinek <jakub@redhat.com>
- fix socketcall on sparc.

* Thu Sep 02 1999 Cristian Gafton <gafton@redhat.com>
- fix KERN_SECURELVL compile problem

* Tue Aug 31 1999 Cristian Gafton <gafton@redhat.com>
- added alpha patch from HJLu to fix the osf_sigprocmask interpretation

* Sat Jun 12 1999 Jeff Johnson <jbj@redhat.com>
- update to 3.99.1.

* Wed Jun  2 1999 Jeff Johnson <jbj@redhat.com>
- add (the other :-) jj's sparc patch.

* Wed May 26 1999 Jeff Johnson <jbj@redhat.com>
- upgrade to 3.99 in order to
-    add new 2.2.x open flags (#2955).
-    add new 2.2.x syscalls (#2866).
- strace 3.1 patches carried along for now.

* Sun May 16 1999 Jeff Johnson <jbj@redhat.com>
- don't rely on (broken!) rpm %%patch (#2735)

* Tue Apr 06 1999 Preston Brown <pbrown@redhat.com>
- strip binary

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 16)

* Tue Feb  9 1999 Jeff Johnson <jbj@redhat.com>
- vfork est arrive!

* Tue Feb  9 1999 Christopher Blizzard <blizzard@redhat.com>
- Add patch to follow clone() syscalls, too.

* Sun Jan 17 1999 Jeff Johnson <jbj@redhat.com>
- patch to build alpha/sparc with glibc 2.1.

* Thu Dec 03 1998 Cristian Gafton <gafton@redhat.com>
- patch to build on ARM

* Wed Sep 30 1998 Jeff Johnson <jbj@redhat.com>
- fix typo (printf, not tprintf).

* Sat Sep 19 1998 Jeff Johnson <jbj@redhat.com>
- fix compile problem on sparc.

* Tue Aug 18 1998 Cristian Gafton <gafton@redhat.com>
- buildroot

* Mon Jul 20 1998 Cristian Gafton <gafton@redhat.com>
- added the umoven patch from James Youngman <jay@gnu.org>
- fixed build problems on newer glibc releases

* Mon Jun 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr
