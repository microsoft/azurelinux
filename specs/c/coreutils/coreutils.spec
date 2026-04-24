# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: A set of basic GNU tools commonly used in shell scripts
Name:    coreutils
Version: 9.7
Release: 8%{?dist}
# some used parts of gnulib are under various variants of LGPL
License: GPL-3.0-or-later AND GFDL-1.3-no-invariants-or-later AND LGPL-2.1-or-later AND LGPL-3.0-or-later
Url:     https://www.gnu.org/software/coreutils/
Source0: https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
Source1: https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz.sig
# From https://savannah.gnu.org/project/release-gpgkeys.php?group=coreutils&download=1
# which is linked as project keyring on https://savannah.gnu.org/projects/coreutils
Source2: coreutils-keyring.gpg
Source50:   supported_utils
Source105:  coreutils-colorls.sh
Source106:  coreutils-colorls.csh

# do not make coreutils-single depend on /usr/bin/coreutils
%global __requires_exclude ^%{_bindir}/coreutils$

# disable the test-lock gnulib test prone to deadlock
Patch100: coreutils-8.26-test-lock.patch

# require_selinux_(): use selinuxenabled(8) if available
Patch101: coreutils-8.26-selinuxenable.patch

# downstream changes to default DIR_COLORS
Patch102: coreutils-8.32-DIR_COLORS.patch

# use python3 in tests
Patch103: coreutils-python3.patch

# df --direct
Patch104: coreutils-df-direct.patch

# cp/mv: do not fail when copying of trivial NFSv4 ACLs fails (rhbz#2363149)
# https://git.savannah.gnu.org/cgit/gnulib.git/patch?id=8a356b77717a2e4f735ec06e326880ca1f61aadb
# https://git.savannah.gnu.org/cgit/gnulib.git/patch?id=955360a66c99bdd9ac3688519a8b521b06958fd3
Patch105: coreutils-9.6-cp-improve-nfsv4-acl-support.patch

# sort: fix buffer under-read (CVE-2025-5278)
# https://cgit.git.savannah.gnu.org/cgit/coreutils.git/patch/?id=8c9602e3a145e9596dc1a63c6ed67865814b6633
Patch106: coreutils-CVE-2025-5278.patch

# stty: add support for arbitrary baud rates (rhbz#2375439)
# https://cgit.git.savannah.gnu.org/cgit/coreutils.git/patch/?id=357fda90d15fd3f7dba61e1ab322b183a48d0081
# https://cgit.git.savannah.gnu.org/cgit/coreutils.git/patch/?id=efaec8078142996d958b6720b85a13b12497c3d0
# https://cgit.git.savannah.gnu.org/cgit/coreutils.git/patch/?id=b7db7757831e93ca44ae59e1921bc4ebbc87974f
# https://cgit.git.savannah.gnu.org/cgit/coreutils.git/patch/?id=8b05eca972f70858749a946ac24f08d0718c1be6
# https://cgit.git.savannah.gnu.org/cgit/coreutils.git/patch/?id=3d35b3c0e56bd556c90dc98c3e5e2e7289b0eb0d
Patch107: coreutils-9.7-stty-arbitrary-baud-rates.patch

# (sb) lin18nux/lsb compliance - multibyte functionality patch
Patch800: coreutils-i18n.patch

# downstream SELinux options deprecated since 2009
Patch950: coreutils-selinux.patch

Conflicts: filesystem < 3

# To avoid clobbering installs
Conflicts: coreutils-single

BuildRequires: attr
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc
BuildRequires: gettext-devel
BuildRequires: gmp-devel
BuildRequires: hostname
BuildRequires: libacl-devel
BuildRequires: libattr-devel
BuildRequires: libcap-devel
BuildRequires: libselinux-devel
BuildRequires: libselinux-utils
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: strace
BuildRequires: systemd-devel
BuildRequires: texinfo

# For gpg verification of source tarball
BuildRequires: gnupg2

# test-only dependencies
BuildRequires: acl
BuildRequires: gdb
BuildRequires: perl-interpreter
BuildRequires: perl(FileHandle)
BuildRequires: python3
BuildRequires: tzdata
%ifarch %valgrind_arches
BuildRequires: valgrind
%endif

%if 0%{?fedora}
BuildRequires: perl(Expect)
BuildRequires: python3-inotify
%endif

%if 23 < 0%{?fedora} || 7 < 0%{?rhel}
# needed by i18n test-cases
BuildRequires: glibc-langpack-en
BuildRequires: glibc-langpack-fr
BuildRequires: glibc-langpack-ko
BuildRequires: glibc-langpack-sv
%endif

Requires: %{name}-common = %{version}-%{release}

Provides: coreutils-full = %{version}-%{release}
Provides: bundled(gnulib)
Obsoletes: %{name} < 8.24-100

%description
These are the GNU core utilities.  This package is the combination of
the old GNU fileutils, sh-utils, and textutils packages.

%package single
Summary:  coreutils multicall binary
Suggests: coreutils-common
Provides: coreutils = %{version}-%{release}
Provides: coreutils%{?_isa} = %{version}-%{release}
Provides: bundled(gnulib)
# To avoid clobbering installs
Conflicts: coreutils < 8.24-100
# Note RPM doesn't support separate buildroots for %files
# http://rpm.org/ticket/874 so use RemovePathPostfixes
# (new in rpm 4.13) to support separate file sets.
RemovePathPostfixes: .single
%description single
These are the GNU core utilities,
packaged as a single multicall binary.


%package common
# yum obsoleting rules explained at:
# https://bugzilla.redhat.com/show_bug.cgi?id=1107973#c7
Obsoletes: %{name} < 8.24-100

# Gnulib translations are maintained seprately since coreutils 9.6 (#2393892)
Requires: gnulib-l10n

# info doc refers to "Specifying the Time Zone" from glibc-doc (#959597)
Suggests: glibc-doc

Summary:  coreutils common optional components
%description common
Optional though recommended components,
including documentation and translations.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -N

# will be regenerated in the build directories
rm -f src/fs.h

# will be further modified by coreutils-8.32-DIR_COLORS.patch
sed src/dircolors.hin \
        -e 's| 00;36$| 01;36|' \
        > DIR_COLORS
sed src/dircolors.hin \
        -e 's| 01;31$| 00;31|' \
        -e 's| 01;35$| 00;35|' \
        > DIR_COLORS.lightbgcolor

# git add DIR_COLORS{,.lightbgcolor}
# git commit -m "clone DIR_COLORS before patching"

# apply all patches
%autopatch -p1

(echo ">>> Fixing permissions on tests") 2>/dev/null
find tests -name '*.sh' -perm 0644 -print -exec chmod 0755 '{}' '+'
(echo "<<< done") 2>/dev/null

# FIXME: Force a newer gettext version to workaround `autoreconf -i` errors
# with coreutils 9.6 and bundled gettext 0.19.2 from gettext-common-devel.
sed -i 's/0.19.2/0.22.5/' bootstrap.conf configure.ac

autoreconf -fiv

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -fpic"

# Upstream suggests to build with -Dlint for static analyzers:
# https://lists.gnu.org/archive/html/coreutils/2018-06/msg00110.html
# ... and even for production binary RPMs:
# https://lists.gnu.org/archive/html/bug-gnulib/2020-05/msg00130.html
# There is currently no measurable performance drop or other known downside.
CFLAGS="$CFLAGS -Dlint"

# make mknod work again in chroot without /proc being mounted (#1811038)
export ac_cv_func_lchmod="no"

# needed for out-of-tree build
%global _configure ../configure

%{expand:%%global optflags %{optflags} -D_GNU_SOURCE=1}
for type in separate single; do
  mkdir -p $type && \
  (cd $type || exit $?
  if test $type = 'single'; then
    config_single='--enable-single-binary'
    config_single="$config_single --without-openssl"  # smaller/slower sha*sum
    config_single="$config_single --without-libgmp"   # expr/factor machine ints
  else
    config_single='--with-openssl'  # faster sha*sum
  fi
  %configure $config_single \
             --cache-file=../config.cache \
             --enable-install-program=arch \
             --enable-no-install-program=kill,uptime \
             --enable-systemd \
             --with-tty-group \
             DEFAULT_POSIX2_VERSION=200112 alternative=199209 || :
  %make_build all V=1

  # make sure that parse-datetime.{c,y} ends up in debuginfo (#1555079)
  ln -fv ../lib/parse-datetime.{c,y} .
  )
done

# Get the list of supported utilities
cp %SOURCE50 .

%check
# Check section disabled: Test tests/tail/inotify-rotate-resources.sh seems to fail due to environment issue and is blocking image build
exit 0

for type in separate single; do
  test $type = 'single' && subdirs='SUBDIRS=.' # Only check gnulib once
  (cd $type && make check %{?_smp_mflags} $subdirs)
done

%install
for type in separate single; do
  install=install
  if test $type = 'single'; then
    subdir=%{_libexecdir}/%{name}; install=install-exec
  fi
  (cd $type && make DESTDIR=$RPM_BUILD_ROOT/$subdir $install)

%if "%{_sbindir}" != "%{_bindir}"
  # chroot was in /usr/sbin :
  mkdir -p $RPM_BUILD_ROOT/$subdir/%_sbindir
  mv $RPM_BUILD_ROOT/$subdir/{%_bindir,%_sbindir}/chroot
%endif

  # Move multicall variants to *.single.
  # RemovePathPostfixes will strip that later.
  if test $type = 'single'; then
    for dir in %{_bindir} \
%if "%{_sbindir}" != "%{_bindir}"
%{_sbindir} \
%endif
%{_libexecdir}/%{name}; do
      for bin in $RPM_BUILD_ROOT/%{_libexecdir}/%{name}/$dir/*; do
        basebin=$(basename $bin)
        mv $bin $RPM_BUILD_ROOT/$dir/$basebin.single
      done
    done
  fi
done

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -p -c -m644 DIR_COLORS{,.lightbgcolor} $RPM_BUILD_ROOT%{_sysconfdir}
install -p -c -m644 %SOURCE105 $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/colorls.sh
install -p -c -m644 %SOURCE106 $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/colorls.csh

%find_lang %name
# Add the %%lang(xyz) ownership for the LC_TIME dirs as well...
grep LC_TIME %name.lang | cut -d'/' -f1-6 | sed -e 's/) /) %%dir /g' >>%name.lang

# (sb) Deal with Installed (but unpackaged) file(s) found
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%files -f supported_utils
%exclude %{_bindir}/*.single
%dir %{_libexecdir}/coreutils
%{_libexecdir}/coreutils/*.so

%files single
%{_bindir}/*.single
%if "%{_sbindir}" != "%{_bindir}"
%{_sbindir}/chroot.single
%endif
%dir %{_libexecdir}/coreutils
%{_libexecdir}/coreutils/*.so.single
# duplicate the license because coreutils-common does not need to be installed
%{!?_licensedir:%global license %%doc}
%license COPYING

%files common -f %{name}.lang
%config(noreplace) %{_sysconfdir}/DIR_COLORS*
%config(noreplace) %{_sysconfdir}/profile.d/*
%{_infodir}/coreutils*
%{_mandir}/man*/*
# The following go to /usr/share/doc/coreutils-common
%doc ABOUT-NLS NEWS README THANKS TODO
%license COPYING

%changelog
* Fri Jan 16 2026 Lukáš Zaoral <lzaoral@redhat.com> - 9.7-7
- fold: fix processing of malformed UTF-8 sequences

* Mon Sep 29 2025 Lukáš Zaoral <lzaoral@redhat.com> - 9.7-6
- require gnulib-l10n for translations of gnulib messages (rhbz#2393892)

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 9.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 30 2025 Lukáš Zaoral <lzaoral@redhat.com> - 9.7-4
- stty: add support for arbitrary baud rates (rhbz#2375439)

* Wed May 28 2025 Lukáš Zaoral <lzaoral@redhat.com> - 9.7-3
- sort: fix buffer under-read (CVE-2025-5278)

* Mon May 19 2025 Lukáš Zaoral <lzaoral@redhat.com> - 9.7-2
- cp/mv: do not fail when copying of trivial NFSv4 ACLs fails (rhbz#2363149)

* Wed Apr 09 2025 Lukáš Zaoral <lzaoral@redhat.com> - 9.7-1
- rebase to latest upstream release (rhbz#2358624)

* Tue Feb 25 2025 Lukáš Zaoral <lzaoral@redhat.com> - 9.6-2
- fix 'who -m' with guessed tty names (rhbz#2343998)

* Mon Jan 20 2025 Lukáš Zaoral <lzaoral@redhat.com> - 9.6-1
- rebase to latest upstream version (rhbz#2338620)
- sync i18n patch with SUSE (Kudos to Berny Völker!)

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 9.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 12 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 9.5-12
- Rebuilt for the bin-sbin merge (2nd attempt)

* Wed Nov 13 2024 Florian Weimer <fweimer@redhat.com> - 9.5-11
- Affinity mask handling in nproc for large CPU counts (rhbz#2325167)

* Fri Sep 27 2024 Lukáš Zaoral <lzaoral@redhat.com> - 9.5-10
- fix fold -b with UTF8 locale (RHEL-60295)

* Tue Aug 27 2024 Lukáš Zaoral <lzaoral@redhat.com> - 9.5-9
- show web sessions in who output (rhbz#2307847)

* Wed Aug 21 2024 Lukáš Zaoral <lzaoral@redhat.com> - 9.5-8
- add missing systemd-devel buildrequires

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 15 2024 Lukáš Zaoral <lzaoral@redhat.com> - 9.5-6
- Rebuilt for the bin-sbin merge

* Mon Jul 15 2024 Sohum Mendon <sohum.mendon@proton.me> - 9.5-5
- fix incorrect exit status when fold is called with a non-existent file

* Tue Jul 09 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 9.5-4
- Rebuilt for the bin-sbin merge

* Thu Jul 04 2024 Lukáš Zaoral <lzaoral@redhat.com> - 9.5-3
- do not buildrequire perl(Expect) on ELN

* Tue Jun 04 2024 Lukáš Zaoral <lzaoral@redhat.com> - 9.5-2
- enable LTO on ppc64le

* Tue Apr 02 2024 Lukáš Zaoral <lzaoral@redhat.com> - 9.5-1
- rebase to latest upstream version (rhbz#2272063)
- sync i18n patch with SUSE (Kudos to Berny Völker!)
- add some test dependencies to execute additional part of the upstream test-suite

* Mon Jan 29 2024 Lukáš Zaoral <lzaoral@redhat.com> - 9.4-6
- fix tail on kernels with 64k page sizes (RHEL-22866)

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 18 2024 Lukáš Zaoral <lzaoral@redhat.com> - 9.4-3
- fix compilation on i686

* Thu Jan 18 2024 Lukáš Zaoral <lzaoral@redhat.com> - 9.4-2
- fix buffer overflow in split (CVE-2024-0684)

* Fri Sep 15 2023 Lukáš Zaoral <lzaoral@redhat.com> - 9.4-1
- new upstream release 9.4 (#2235759)
- enable integration with systemd
- fix the license field

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Apr 18 2023 Kamil Dudka <kdudka@redhat.com> - 9.3-1
- remove obsolete Provides for absolute paths
- new upstream release 9.3

* Tue Apr 11 2023 Lukáš Zaoral <lzaoral@redhat.com> - 9.2-4
- migrate to SPDX license format

* Fri Mar 24 2023 Kamil Dudka <kdudka@redhat.com> - 9.2-3
- copy: fix --reflink=auto to fallback in more cases (#2180056)
- cksum: fix reporting of failed checks (#2180056)

* Wed Mar 22 2023 Kamil Dudka <kdudka@redhat.com> - 9.2-2
- coreutils-getgrouplist.patch: drop a patch no longer needed

* Wed Mar 22 2023 Kamil Dudka <kdudka@redhat.com> - 9.2-1
- new upstream release 9.2

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 02 2023 Kamil Dudka <kdudka@redhat.com> - 9.1-10
- drop obsolete downstream-only extension of date(1) man page
- undocument downstream SELinux options deprecated since 2009

* Mon Jan 02 2023 Kamil Dudka <kdudka@redhat.com> - 9.1-9
- basic support for checking NFSv4 ACLs (#2137866)

* Mon Sep 19 2022 Kamil Dudka <kdudka@redhat.com> - 9.1-8
- remove obsolete extension of mkdir(1) info documentation

* Tue Aug 23 2022 Kamil Dudka <kdudka@redhat.com> - 9.1-7
- remove non-upstream patch for uname -i/-p (#548834)

* Mon Aug 08 2022 Kamil Dudka <kdudka@redhat.com> - 9.1-6
- improve wording of a comment in /etc/DIR_COLORS (#2112593)

* Mon Aug 08 2022 Kamil Dudka <kdudka@redhat.com> - 9.1-5
- improve handling of control characters in unexpand (#2112870)

* Mon Aug 01 2022 Kamil Dudka <kdudka@redhat.com> - 9.1-4
- prevent unexpand from failing on control characters (#2112870)

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Apr 23 2022 Pádraig Brady <P@draigBrady.com> - 9.1-2
- make simple backups in correct dir; broken in 9.1

* Tue Apr 19 2022 Kamil Dudka <kdudka@redhat.com> - 9.1-1
- new upstream release 9.1

* Mon Mar 21 2022 Kamil Dudka <kdudka@redhat.com> - 9.0-5
- ls, stat: avoid triggering automounts (#2044981)

* Tue Mar 01 2022 Kamil Dudka <kdudka@redhat.com> - 9.0-4
- make `df --direct` work again (#2058686)

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Oct 04 2021 Kamil Dudka <kdudka@redhat.com> - 9.0-2
- chmod: fix exit status when ignoring symlinks

* Sun Sep 26 2021 Kamil Dudka <kdudka@redhat.com> - 9.0-1
- new upstream release 9.0

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com>
- Rebuilt with OpenSSL 3.0.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 07 2021 Kamil Dudka <kdudka@redhat.com> - 8.32-30
- df: fix duplicated remote entries due to bind mounts (#1979814)

* Thu Jul 01 2021 Kamil Dudka <kdudka@redhat.com> - 8.32-28
- tail: fix stack out-of-bounds write with --follow

* Tue Jun 08 2021 Kamil Dudka <kdudka@redhat.com> - 8.32-27
- mountlist: recognize fuse.portal as dummy file system (#1913358)

* Mon May 17 2021 Kamil Dudka <kdudka@redhat.com> - 8.32-26
- cp: pick additional copy_file_range()-related fixes from upstream

* Mon May 03 2021 Kamil Dudka <kdudka@redhat.com> - 8.32-24
- copy: ensure we enforce --reflink=never (#1956080)

* Tue Apr 27 2021 Kamil Dudka <kdudka@redhat.com> - 8.32-23
- copy: do not refuse to copy a swap file

* Fri Apr 09 2021 Kamil Dudka <kdudka@redhat.com> - 8.32-22
- weaken the dependency on glibc-doc to reduce minimal installations
- drop the last use of ncurses no longer needed (#1830318)
- utimens: fix confusing arg type in internal func

* Fri Mar 26 2021 Kamil Dudka <kdudka@redhat.com> - 8.32-21
- hostname,ln: fix memory leaks detected by Coverity

* Wed Mar 24 2021 Kamil Dudka <kdudka@redhat.com> - 8.32-20
- cp: use copy_file_range if available

* Thu Feb 18 2021 Kamil Dudka <kdudka@redhat.com> - 8.32-19
- stat: add support for the exfat file system (#1921427)

* Wed Feb 03 2021 Kamil Dudka <kdudka@redhat.com> - 8.32-18
- make coreutils-common recommend glibc-doc for info doc refs (#959597)

* Tue Feb 02 2021 Kamil Dudka <kdudka@redhat.com> - 8.32-17
- ls: fix crash printing SELinux context for unstatable files (#1921249)
- split: fix --number=K/N to output correct part of file (#1921246)
- expr: fix invalid read with unmatched \(...\) (#1919775)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 08 2020 Kamil Dudka <kdudka@redhat.com> - 8.32-15
- rm: do not skip files upon failure to remove an empty dir (#1905481)

* Tue Nov 03 2020 Kamil Dudka <kdudka@redhat.com> - 8.32-14
- df,stat,tail: recognize more file system types

* Wed Oct 14 2020 Kamil Dudka <kdudka@redhat.com> - 8.32-13
- make the %%build section idempotent

* Mon Aug 17 2020 Kamil Dudka <kdudka@redhat.com> - 8.32-12
- do not install /etc/DIR_COLORS.256color (#1830318)

* Thu Jul 30 2020 Kamil Dudka <kdudka@redhat.com> - 8.32-11
- cp: default to --reflink=auto (#1861108)

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 24 2020 Kamil Dudka <kdudka@redhat.com> - 8.32-9
- disable -flto on ppc64le to make test-float pass (#1789115)

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 8.32-8
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Fri Jun 26 2020 James Cassell <cyberpear@fedoraproject.org> - 8.32-7
- move ncurses to -common package since it's needed for colorls.sh
- make ncurses optional

* Fri May 15 2020 Kamil Dudka <kdudka@redhat.com> - 8.32-6
- compile with -Dlint to enable optional initialization and cleanup code

* Thu Apr 23 2020 Kamil Dudka <kdudka@redhat.com> - 8.32-5
- du: simplify leaf optimization for XFS (#1823247)

* Fri Apr 17 2020 Tom Stellard <tstellar@redhat.com> - 8.32-4
- Fix missing inline function definition

* Wed Mar 11 2020 Kamil Dudka <kdudka@redhat.com> - 8.32-3
- uniq: remove collation handling as required by newer POSIX

* Mon Mar 09 2020 Kamil Dudka <kdudka@redhat.com> - 8.32-2
- make mknod work again in chroot without /proc being mounted (#1811038)
- ls: restore 8.31 behavior on removed directories

* Thu Mar 05 2020 Kamil Dudka <kdudka@redhat.com> - 8.32-1
- new upstream release 8.32

* Tue Feb 11 2020 Kamil Dudka <kdudka@redhat.com> - 8.31-10
- make upstream test-suite work with root privileges (#1800597)

* Wed Feb 05 2020 Kamil Dudka <kdudka@redhat.com> - 8.31-9
- use upstream fix the cp/proc-short-read test

* Thu Jan 30 2020 Kamil Dudka <kdudka@redhat.com> - 8.31-8
- skip a test that relies on /proc/kallsyms having immutable content

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 17 2019 Kamil Dudka <kdudka@redhat.com> - 8.31-6
- temporarily disable the use of statx (#1760300)

* Fri Oct 11 2019 Kamil Dudka <kdudka@redhat.com> - 8.31-5
- use statx instead of stat when available (#1760300)

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 16 2019 Kamil Dudka <kdudka@redhat.com> - 8.31-3
- disable flashing in ls colors for broken symbolic links (#1728986)

* Mon Mar 18 2019 Kamil Dudka <kdudka@redhat.com> - 8.31-2
- fix formatting of sha512sum(1) man page (#1688740)

* Mon Mar 11 2019 Kamil Dudka <kdudka@redhat.com> - 8.31-1
- new upstream release 8.31

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 07 2018 Kamil Dudka <kdudka@redhat.com> - 8.30-8
- sync: fix open() fallback bug
- fix implicit declaration warning in coreutils-getgrouplist.patch

* Sat Nov 03 2018 Kevin Fenzi <kevin@scrye.com> - 8.30-7
- Also remove Requires pre/post used by info scriptlets.

* Sat Nov 03 2018 Kevin Fenzi <kevin@scrye.com> - 8.30-6
- Remove no longer needed info scriptlets

* Thu Oct 11 2018 Kamil Dudka <kdudka@redhat.com> - 8.30-5
- fix heap-based buffer overflow in vasnprintf() (CVE-2018-17942)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.30-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Kamil Dudka <kdudka@redhat.com> - 8.30-3
- rename gnulib's renameat2 to renameatu to avoid clash with glibc (#1598518)

* Wed Jul 04 2018 Kamil Dudka <kdudka@redhat.com> - 8.30-2
- sync i18n patches with Suse (patch by Bernhard Voelker)

* Mon Jul 02 2018 Kamil Dudka <kdudka@redhat.com> - 8.30-1
- new upstream release 8.30

* Wed May 30 2018 Kamil Dudka <kdudka@redhat.com> - 8.29-12
- add provides to coreutils-single to make it a drop-in replacement

* Mon May 28 2018 Kamil Dudka <kdudka@redhat.com> - 8.29-11
- ls: increase the allowed abmon width from 5 to 12 (#1577872)
- date, ls: pick strftime fixes from glibc to improve locale support (#1577872)

* Fri Apr 20 2018 Kamil Dudka <kdudka@redhat.com> - 8.29-10
- fix crash caused by mistakenly enabled leaf optimization (#1558249)

* Fri Mar 23 2018 Kamil Dudka <kdudka@redhat.com> - 8.29-9
- make it possible to install the latest available Adobe Reader RPM for Linux

* Mon Mar 19 2018 Kamil Dudka <kdudka@redhat.com> - 8.29-8
- drop BR for bison, which is not used during the build

* Fri Mar 16 2018 Kamil Dudka <kdudka@redhat.com> - 8.29-7
- make sure that parse-datetime.{c,y} ends up in debuginfo (#1555079)

* Tue Mar 06 2018 Kamil Dudka <kdudka@redhat.com> - 8.29-6
- fix build failure with glibc-2.28

* Mon Feb 26 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 8.29-5
- Remove /bin/* Provides

* Mon Feb 19 2018 Kamil Dudka <kdudka@redhat.com> - 8.29-4
- add explicit BR for the gcc compiler

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Kamil Dudka <kdudka@redhat.com> - 8.29-2
- doc: warn about following symlinks recursively in chown/chgrp (CVE-2017-18018)
- mv -n: do not overwrite the destination

* Tue Jan 02 2018 Kamil Dudka <kdudka@redhat.com> - 8.29-1
- new upstream release 8.29

* Tue Nov 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 8.28-2
- Remove very old Provides (mktemp, sh-utils, textwrap, fileutils, stat)

* Mon Sep 04 2017 Kamil Dudka <kdudka@redhat.com> - 8.28-1
- new upstream release 8.28

* Tue Aug 22 2017 Ville Skyttä <ville.skytta@iki.fi> - 8.27-16
- Own the %%{_libexecdir}/coreutils dir

* Fri Aug 18 2017 Kamil Dudka <kdudka@redhat.com> - 8.27-15
- ptx: fix a possible crash caused by integer overflow (#1482445)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.27-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Fri Jul 28 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 8.27-13
- Enable separate debuginfo back

* Wed Jul 26 2017 Kamil Dudka <kdudka@redhat.com> - 8.27-12
- avoid build failure caused broken RPM code that produces debuginfo packages

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.27-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 30 2017 Sebastian Kisela <skisela@redhat.com> - 8.27-10
- doc: mention `setpriv --no-new-privs` feature in runcon info

* Tue May 16 2017 Kamil Dudka <kdudka@redhat.com> - 8.27-9
- add coreutils-full provides for coreutils to make it explicitly installable

* Wed May 03 2017 Kamil Dudka <kdudka@redhat.com> - 8.27-8
- drop coreutils-overflow.patch no longer needed (#158405)

* Wed May 03 2017 Kamil Dudka <kdudka@redhat.com> - 8.27-7
- drop workaround for already fixed rpm-build bug (#1306559)

* Wed May 03 2017 Kamil Dudka <kdudka@redhat.com> - 8.27-6
- do not mention a deprecated option in localized man pages
- drop workaround no longer needed for 10 years old rpm-build bug (#246729)
- drop unnecessary uses of %%defattr

* Fri Apr 28 2017 Sebastian Kisela <skisela@redhat.com> - 8.27-5
- tail: revert to polling if a followed directory is replaced (#1283760)

* Thu Apr 27 2017 Kamil Dudka <kdudka@redhat.com> - 8.27-4
- date, touch: fix out-of-bounds write via large TZ variable (CVE-2017-7476)

* Tue Apr 25 2017 Kamil Dudka <kdudka@redhat.com> - 8.27-3
- do not obsolete coreutils-single, so it can be installed by DNF2 (#1444802)

* Wed Mar 15 2017 Kamil Dudka <kdudka@redhat.com> - 8.27-2
- fix spurious build failure caused by the misc/date-debug test

* Thu Mar 09 2017 Kamil Dudka <kdudka@redhat.com> - 8.27-1
- new upstream release 8.27

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.26-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 03 2017 Kamil Dudka <kdudka@redhat.com> - 8.26-6
- fold: preserve new-lines in mutlibyte text (#1418505)

* Mon Jan 23 2017 Kamil Dudka <kdudka@redhat.com> - 8.26-5
- date: fix TZ= regression (patch by Pádraig Brady)

* Mon Jan 02 2017 Kamil Dudka <kdudka@redhat.com> - 8.26-4
- use upstream patch for gnulib's test-lock (instead of disabling it)

* Thu Dec 15 2016 Kamil Dudka <kdudka@redhat.com> - 8.26-3
- drop build fixes no longer needed

* Fri Dec 02 2016 Kamil Dudka <kdudka@redhat.com> - 8.26-2
- apply patches automatically to ease maintenance

* Thu Dec 01 2016 Kamil Dudka <kdudka@redhat.com> - 8.26-1
- new upstream release 8.26

* Mon Oct 31 2016 Kamil Dudka <kdudka@redhat.com> - 8.25-17
- md5sum,sha*sum: fix --ignore-missing with checksums starting with 00

* Tue Oct 11 2016 Tomáš Mráz <tmraz@redhat.com> - 8.25-16
- rebuild with OpenSSL 1.1.0

* Wed Sep 07 2016 Kamil Dudka <kdudka@redhat.com> - 8.25-15
- ls: allow interruption when reading slow directories (#1365933)

* Tue Jul 19 2016 Kamil Dudka <kdudka@redhat.com> - 8.25-14
- run autoreconf in %%prep
- drop post-install fix for Japanese locales that no longer applies
- fix 'sort -h -k' in locales that use blank as thousands separator (#1355780)

* Thu Jul 14 2016 Kamil Dudka <kdudka@redhat.com> - 8.25-13
- make 'sort -h' work for arbitrary column even when using UTF-8 locales

* Mon Jul 11 2016 Kamil Dudka <kdudka@redhat.com> - 8.25-12
- install -Z now sets default SELinux context for created directories (#1339135)
- drop the %%pre scriptlet, which is no longer needed (#1354078)
- clarify recognition of "^COLOR.*none" in /etc/DIR_COLORS (#1349579)

* Thu Jul 07 2016 Jakub Martisko <jamartis@redhat.com> - 8.25-11
- switch to UTF8 locale when (un)expand input contains BOM header
  (#1158494)
- fixed regression where (un)expand would end with "long input line"
  error when BOM header is present

* Fri Jun 24 2016 Ondrej Vasik <ovasik@redhat.com> - 8.25-10
- change way of detection of interactive shell in colorls.sh script
  (#1321648)

* Mon Jun 20 2016 Kamil Dudka <kdudka@redhat.com> - 8.25-9
- add BR for glibc-langpack-en to prevent the expand/mb test from failing
- do not use /bin/mv in %%post to avoid a circular dependency (#1348043)

* Fri Jun 17 2016 Kamil Dudka <kdudka@redhat.com> - 8.25-8
- sync /etc/DIR_COLORS with latest upstream (#1335320)

* Wed Jun 15 2016 Kamil Dudka <kdudka@redhat.com> - 8.25-7
- handle info doc in RPM scriptlets of coreutils-common, which provides it
- make sure that the license file is installed, even if coreutils-common is not

* Thu Jun 09 2016 Jakub Martisko <jamartis@redhat.com> - 8.25-6
- (un)expand: fix regression in handling input files, where only
  the first file was processed.

* Sat Mar 05 2016 Ondrej Vasik <ovasik@redhat.com> - 8.25-5
- cut: move back to the old i18n implementation (#1314722)

* Mon Feb 15 2016 Ondrej Vasik <ovasik@redhat.com> - 8.25-4
- cut: fix regression in handling fields for lines wider
  than 64 chars (#1304839)

* Thu Feb 11 2016 Lubomir Rintel <lkundrak@v3.sk> - 8.25-3
- Fix a regression in unexpand empty line handling

* Thu Jan 21 2016 Ondrej Vasik <ovasik@redhat.com> - 8.25-2
- Adjust the i18n patch for coreutils-8.25
- add new base32 binary

* Wed Jan 20 2016 Ondrej Vasik <ovasik@redhat.com> - 8.25-1
- new upstream release(#1300282)

* Fri Jan 15 2016 Ondrej Oprala <ooprala@redhat.com> - 8.24-108
- cut: be MB for ALL archs

* Fri Jan 15 2016 Ondrej Oprala <ooprala@redhat.com> - 8.24-107
- Use the new i18n implementation for the cut utility

* Wed Jan 13 2016 Ondrej Vasik <ovasik@redhat.com> - 8.24-106
- mv: prevent dataloss when source dir is specified multiple
  times (#1297464, by P.Brady)

* Mon Dec 14 2015 Pádraig Brady <pbrady@redhat.com> - 8.24-105
- Give explicit priority to coreutils over coreutils-single

* Thu Dec 03 2015 Pádraig Brady <pbrady@redhat.com> - 8.24-104
- Avoid libgmp and libcrypto dependencies from coreutils-single

* Thu Dec 03 2015 Pádraig Brady <pbrady@redhat.com> - 8.24-103
- Remove erroneous /usr/bin/kill from coreutils-single

* Tue Dec 01 2015 Ondrej Oprala <ooprala@redhat.com> - 8.24-102
- Use the new i18n implementation for expand/unexpand

* Mon Nov 30 2015 Ondrej Vasik <ovasik@redhat.com> - 8.24-101
- coreutils-single should provide versioned coreutils (#1286338)

* Wed Nov 18 2015 Pádraig Brady <pbrady@redhat.com> - 8.24-100
- Split package to more easily support smaller installs

* Wed Sep 16 2015 Kamil Dudka <kdudka@redhat.com> - 8.24-4
- fix memory leak in sort/I18N (patches written by Pádraig, #1259942)

* Sat Sep 12 2015 Ondrej Vasik <ovasik@redhat.com> 8.24-3
- fix one still existing occurance of non-full path in colorls.sh

* Thu Jul 16 2015 Ondrej Vasik <ovasik@redhat.com> 8.24-2
- use newer version of sort/I18N fix for CVE-2015-4041
  and CVE-2015-4042

* Sun Jul 05 2015 Ondrej Vasik <ovasik@redhat.com> 8.24-1
- new upstream release 8.24

* Sat Jul  4 2015 Peter Robinson <pbrobinson@fedoraproject.org> 8.23-14
- Disable failing test-update-copyright to fix FTBFS

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.23-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Ondrej Vasik <ovasik@redhat.com> - 8.23-12
- call utilities in colorls.* scripts with full path (#1222140)

* Thu May 14 2015 Kamil Dudka <kdudka@redhat.com> - 8.23-11
- run 'make check' in parallel to speed up the build

* Wed May 13 2015 Ondrej Oprala <ooprala@redhat.com> - 8.23-10
- sort - fix buffer overflow in some case conversions
  - patch by Pádraig Brady

* Mon Apr 20 2015 Pádraig Brady <pbrady@redhat.com> - 8.23-9
- Adjust LS_COLORS in 256 color mode; brighten some, remove hardlink colors (#1196642)

* Sun Mar 22 2015 Peter Robinson <pbrobinson@fedoraproject.org> 8.23-8
- Drop large ancient docs

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 8.23-7
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Dec 01 2014 Ondrej Vasik <ovasik@redhat.com> - 8.23-6
- have the LC_TIME subdirs with lang macro (#1169027)

* Wed Oct 15 2014 Ondrej Vasik <ovasik@redhat.com> - 8.23-5
- handle situation with ro /tmp in colorls scripts (#1149761)

* Wed Oct 01 2014 Ondrej Vasik <ovasik@redhat.com> - 8.23-4
- fix the sorting in multibyte locales (NUL-terminate sort keys)
  - patch by Andreas Schwab (#1146185)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 05 2014 Ondrej Vasik <ovasik@redhat.com> - 8.23-2
- enable smp_flags again (by B.Voelker)
- fix regression in chroot

* Tue Jul 22 2014 Ondrej Vasik <ovasik@redhat.com> - 8.23-1
- new upstream release 8.23
- synchronize the old differences in ls SELinux options
  with upstream
- skip df/skip-duplicates.sh test for now (passing locally, failing in koji)

* Fri Jul 11 2014 Tom Callaway <spot@fedoraproject.org> - 8.22-17
- fix license handling

* Mon Jun 23 2014 Jakub Čajka <jcajka@redhat.com> - 8.22-16
- fix failed tests on ppc(backport from gnulib upstream)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.22-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Apr 12 2014 Ondrej Vasik <ovasik@redhat.com> 8.22-14
- fix dd sparse test failure on xfs filesystem(#1085727,
  by P.Brady)

* Wed Mar 05 2014 Ondrej Vasik <ovasik@redhat.com> 8.22-13
- drop the util-linux requirements (smaller docker images),
  drop ancient obsoletes of -libs subpackage

* Sun Mar 02 2014 Ondrej Vasik <ovasik@redhat.com> 8.22-12
- fix the date crash or infloop in TZ="" parsing (#1069657)

* Mon Jan 13 2014 Ondrej Vasik <ovasik@redhat.com> 8.22-11
- cp/mv/install: do not crash when getfscreatecon() is
  returning a NULL context

* Mon Jan 13 2014 Ondrej Vasik <ovasik@redhat.com> 8.22-10
- unset the unnecessary envvars after colorls scripts(#1051703)
- improve the limitation (check for both utf8 and utf-8)

* Fri Jan 10 2014 Ondrej Oprala <ooprala@redhat.com> 8.22-9
- Limit the cut optimizations to UTF-8 locales only

* Wed Jan 08 2014 Ondrej Oprala <ooprala@redhat.com> 8.22-8
- Don't use cut mb path if not necessary (#1021403, #499220)
- several i18n patch improvements merged from OpenSUSE (fixed
  compilation warnings, simplify mb handling in uniq)

* Mon Jan 06 2014 Ondrej Oprala <ooprala@redhat.com> 8.22-7
- Fix sorting by non-first field (#1003544)

* Fri Jan 03 2014 Ondrej Vasik <ovasik@redhat.com> 8.22-6
- do not modify SELinux contexts of existing parent
  directories when copying files (fix by P.Brady, #1045122)

* Thu Jan 02 2014 Ondrej Oprala <ooprala@redhat.com> 8.22-5
- reverted an old change and constricted it's condition
- turned off two multibyte tests (wrong strcoll return value)

* Mon Dec 23 2013 Ondrej Vasik <ovasik@redhat.com> 8.22-4
- skip even the ls aliases in noninteractive mode
  (suggested by T. Cordes, #988152)

* Sun Dec 22 2013 Ondrej Vasik <ovasik@redhat.com> 8.22-3
- reset buffer before copying to prevent some rare cases of
  invalid output in join and uniq(#1036289)

* Sat Dec 14 2013 Ondrej Vasik <ovasik@redhat.com> 8.22-1
- new upstream version 8.22
- temporarily disable multibyte cut.pl part and df symlink
  tests

* Thu Dec 12 2013 Ondrej Vasik <ovasik@redhat.com> 8.21-23
- skip output-is-input-mb.p test - failing on armv7l (reported
  by B.Voelker)

* Mon Dec  9 2013 Peter Robinson <pbrobinson@fedoraproject.org> 8.21-22
- Add upstream patch to fix test failures on aarch64

* Thu Nov 28 2013 Ondrej Vasik <ovasik@redhat.com> 8.21-21
- turn on the multibyte path in the testsuite to cover
  i18n regressions

* Wed Nov 06 2013 Ondrej Vasik <ovasik@redhat.com> 8.21-20
- fix possible colorls.csh script errors for tcsh with
  noclobber set and entered include file (#1027279)

* Mon Oct 14 2013 Ondrej Vasik <ovasik@redhat.com> 8.21-19
- cp: correct error message for invalid arguments
  of '--no-preserve' (#1018206)

* Thu Aug 15 2013 Ondrej Vasik <ovasik@redhat.com> 8.21-18
- pr -e, with a mix of backspaces and TABs, could corrupt the heap
  in multibyte locales (analyzed by J.Koncicky)

* Wed Aug 14 2013 Ondrej Oprala <ooprala@redhat.com> 8.21-17
- Fix sort multibyte incompatibilities

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.21-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Ondrej Oprala <ooprala@redhat.com> 8.21-15
- change the TMP variable name in colorls.csh to _tmp (#981373)

* Fri May 17 2013 Ondrej Vasik <ovasik@redhat.com 8.21-14
- revert the last change

* Fri May 17 2013 Ondrej Vasik <ovasik@redhat.com 8.21-13
- require glibc-devel to prevent broken links in coreutils
  info manual (#959597)

* Wed May 08 2013 Ondrej Vasik <ovasik@redhat.com 8.21-12
- optimization of colorls scripts by Ville Skytta (#961012)

* Fri Apr 05 2013 Ondrej Oprala <ooprala@redhat.com 8.21-11
- Fix tmp file location in colorls scripts (#948008)

* Thu Mar 14 2013 Ondrej Vasik <ovasik@redhat.com> 8.21-10
- DIR_COLORS.$TERM should have higher priority than
  DIR_COLORS.256color (#921651)

* Mon Mar 11 2013 Ondrej Oprala <ooprala@redhat.com> 8.21-9
- add support for INCLUDE in colorls scripts (#818069)

* Mon Mar 04 2013 Ondrej Vasik <ovasik@redhat.com> 8.21-8
- fix factor on AArch64 (M.Salter, #917735)

* Fri Mar 01 2013 Ondrej Vasik <ovasik@redhat.com> 8.21-7
- ls: colorize several new archive/compressed types (#868510)

* Sat Feb 23 2013 Ondrej Vasik <ovasik@redhat.com> 8.21-6
- install: do proper cleanup when strip fails
  (O.Oprala, B.Voekler, #632444)

* Wed Feb 20 2013 Ondrej Vasik <ovasik@redhat.com> 8.21-5
- fix multibyte issue in unexpand(by R.Kollar, #821262)

* Mon Feb 18 2013 Ondrej Oprala <ooprala@redhat.com> 8.21-4
- fix sort-mb-tests.sh test (B.Voelker)

* Mon Feb 18 2013 Mark Wielaard <mjw@redhat.com> 8.21-3
- fix coreutils-i18n.patch to terminate mbdelim string (#911929)

* Mon Feb 18 2013 Ondrej Vasik <ovasik@redhat.com> 8.21-2
- remove unnecessary powerpc factor patch

* Fri Feb 15 2013 Ondrej Vasik <ovasik@redhat.com> 8.21-1
- new upstream release 8.21, update patches

* Thu Feb 07 2013 Ondrej Oprala <ooprala@redhat.com> 8.20-8
- add missing sort-mb-tests.sh to local.mk

* Tue Feb 05 2013 Ondrej Vasik <ovasik@redhat.com> 8.20-7
- add support for DTR/DSR control flow in stty(#445213)

* Wed Jan 23 2013 Ondrej Vasik <ovasik@redhat.com> 8.20-6
- fix multiple segmantation faults in i18n patch (by SUSE)
  (#869442, #902917)

* Thu Dec 20 2012 Ondrej Vasik <ovasik@redhat.com> 8.20-5
- seq: fix newline output when -s specified (upstream)

* Mon Dec 10 2012 Ondrej Vasik <ovasik@redhat.com> 8.20-4
- fix showing duplicates in df (#709351, O.Oprala, B.Voelker)

* Thu Dec 06 2012 Ondrej Vasik <ovasik@redhat.com> 8.20-3
- fix factor on 32bit powerpc (upstream, #884715)

* Mon Nov 05 2012 Ondrej Vasik <ovasik@redhat.com> 8.20-2
- disable the temporary O_SYNC fix (glibc is fixed - #872366)

* Sat Oct 27 2012 Ondrej Vasik <ovasik@redhat.com> 8.20-1
- new upstream release 8.20
- Temporarily require util-linux >= 2.22.1-3 (to prevent missing
  su/runuser on system)

* Mon Aug 20 2012 Ondrej Vasik <ovasik@redhat.com> 8.19-1
- new upstream release 8.19
- fix multibyte issues in cut and expand (M.Briza, #821260)

* Sun Aug 12 2012 Ondrej Vasik <ovasik@redhat.com> 8.18-1
- new upstream release 8.18
- su/runuser moved to util-linux

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 15 2012 Ondrej Vasik <ovasik@redhat.com> 8.17-3
- add virtual provides for bundled(gnulib) copylib (#821748)

* Fri May 11 2012 Ondrej Vasik <ovasik@redhat.com> 8.17-2
- ls: upstream fix - correctly show symlinks in /

* Fri May 11 2012 Ondrej Vasik <ovasik@redhat.com> 8.17-1
- new upstream release 8.17

* Fri May 04 2012 Ondrej Vasik <ovasik@redhat.com> 8.16-3
- add .htm and .shtml to colorized DIR_COLORS document
  type (#817218)

* Mon Apr 16 2012 Ondrej Vasik <ovasik@redhat.com> 8.16-2
- fix the tcsh colorls.csh behaviour in non-interactive
  mode (#804604)

* Mon Mar 26 2012 Ondrej Vasik <ovasik@redhat.com> 8.16-1
- new upstream release 8.16
- defuzz patches, remove already applied patches

* Thu Mar 08 2012 Ondrej Vasik <ovasik@redhat.com> 8.15-8
- fix regression in du -x with nondir argument (by J.Meyering)

* Wed Mar 07 2012 Ondrej Vasik <ovasik@redhat.com> 8.15-7
- fix sort segfault with multibyte locales (by P.Brady)

* Fri Feb 10 2012 Harald Hoyer <harald@redhat.com> 8.15-6
- turn on testsuite again

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 8.15-5
- add filesystem guard

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 8.15-4
- add missing provides for the /usr-move

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 8.15-3
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Mon Jan 16 2012 Kamil Dudka <kdudka@redhat.com> - 8.15-2
- fix stack smashing, buffer overflow, and invalid output of pr (#772172)

* Sat Jan 07 2012 Ondrej Vasik <ovasik@redhat.com> - 8.15-1
- new upstream release 8.15

* Thu Jan 05 2012 Ondrej Vasik <ovasik@redhat.com> - 8.14-6
- do not use shebang in sourced colorls.csh

* Thu Jan 05 2012 Ondrej Vasik <ovasik@redhat.com> - 8.14-5
- fix pr -c and pr -v segfault with multibyte locales

* Mon Oct 31 2011 Rex Dieter <rdieter@fedoraproject.org> 8.14-4
- rebuild (gmp), last time, I promise

* Mon Oct 24 2011 Ondrej Vasik <ovasik@redhat.com> - 8.14-3
- require at least pam 1.1.3-7 (#748215)

* Thu Oct 20 2011 Ondrej Vasik <ovasik@redhat.com> - 8.14-2
- rebuild for gmp

* Wed Oct 12 2011 Ondrej Vasik <ovasik@redhat.com> - 8.14-1
- new upstream release 8.14

* Mon Sep 26 2011 Peter Schiffer <pschiffe@redhat.com> - 8.13-2.2
- rebuild with new gmp

* Mon Sep 12 2011 Ondrej Vasik <ovasik@redhat.com> - 8.13-2
- Obsolete coreutils-libs (#737287)

* Fri Sep 09 2011 Ondrej Vasik <ovasik@redhat.com> - 8.13-1
- new upstream release 8.13
- temporarily disable recently added multibyte checks in
  misc/cut test
- fix the SUSE fix for cut output-delimiter
- drop coreutils-libs subpackage, no longer needed

* Mon Sep 05 2011 Ondrej Vasik <ovasik@redhat.com> - 8.12-7
- incorporate some i18n patch fixes from OpenSUSE:
  - fix cut output-delimiter option
  - prevent infinite loop in sort when ignoring chars
  - prevent using unitialized variable in cut

* Tue Aug 23 2011 Ondrej Vasik <ovasik@redhat.com> - 8.12-6
- su: fix shell suspend in tcsh (#597928)

* Thu Aug 18 2011 Ondrej Vasik <ovasik@redhat.com> - 8.12-5
- variable "u" should be static in uname processor type patch

* Thu Aug 11 2011 Ondrej Vasik <ovasik@redhat.com> - 8.12-4
- deprecate non-upstream cp -Z/--context (install should be
  used instead of it), make it working if destination exists
  (#715557)

* Fri Jul 29 2011 Ondrej Vasik <ovasik@redhat.com> - 8.12-3
- use acl_extended_file_nofollow() if available (#692823)

* Fri Jul 15 2011 Ondrej Vasik <ovasik@redhat.com> - 8.12-2
- support ecryptfs mount of Private (postlogin into su.pamd)
  (#722323)

* Wed Apr 27 2011 Ondrej Vasik <ovasik@redhat.com> - 8.12-1
- new upstream release 8.12

* Thu Apr 14 2011 Ondrej Vasik <ovasik@redhat.com> - 8.11-2
- fix issue with df --direct(extra new line)

* Thu Apr 14 2011 Ondrej Vasik <ovasik@redhat.com> - 8.11-1
- new upstream release 8.11, defuzz patches

* Tue Mar 22 2011 Ondrej Vasik <ovasik@redhat.com> - 8.10-7
- add note about mkdir mode behaviour into info
  documentation (#610559)

* Mon Mar 14 2011 Ondrej Vasik <ovasik@redhat.com> - 8.10-6
- fix possible uninitalized variables usage caused by i18n
  patch(#683799)

* Fri Mar  4 2011 Ondrej Vasik <ovasik@redhat.com> - 8.10-5
- make coreutils build even without patches (with
  nopam, norunuser and noselinux variables)

* Thu Feb 17 2011 Ondrej Vasik <ovasik@redhat.com> - 8.10-4
- colorize documents by DIR_COLORS files(brown like mc)

* Thu Feb 17 2011 Ondrej Vasik <ovasik@redhat.com> - 8.10-3
- add several new TERMs to DIR_COLORS files(#678147)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Ondrej Vasik <ovasik@redhat.com> - 8.10-1
- new upstream release coreutils-8.10

* Sat Jan 08 2011 Dennis Gilmore <dennis@ausil.us> - 8.9-2
- drop no longer needed mkstemp patch for sparc 

* Tue Jan 04 2011 Ondrej Vasik <ovasik@redhat.com> - 8.9-1
- new upstream release coreutils-8.9

* Fri Dec 31 2010 Ondrej Vasik <ovasik@redhat.com> - 8.8-2
- The suffix length was dependent on the number of bytes
  or lines per file (#666293)

* Thu Dec 23 2010 Ondrej Vasik <ovasik@redhat.com> - 8.8-1
- fix parallel sorting issue (#655096)
- new upstream release coreutils-8.8 (#665164)

* Thu Nov 18 2010 Ondrej Vasik <ovasik@redhat.com> - 8.7-2
- don't prompt for password with runuser(#654367)

* Mon Nov 15 2010 Ondrej Vasik <ovasik@redhat.com> - 8.7-1
- new upstream release coreutils-8.7
- pam support in su consolidation with SUSE(#622700)

* Wed Nov 03 2010 Kamil Dudka <kdudka@redhat.com> - 8.6-3
- prevent sort from assertion failure in case LC_CTYPE does not match LC_TIME
  (#647938)

* Tue Oct 26 2010 Kamil Dudka <kdudka@redhat.com> - 8.6-2
- improve i18n support in sort (debug-keys test is now back)

* Wed Oct 20 2010 Ondrej Vasik <ovasik@redhat.com> - 8.6-1
- new upstream release 8.6
- remove applied patches, temporarily disable sort
  debug-keys test for multibyte locales (failing
  because of i18n patch)

* Thu Sep 30 2010 Ondrej Vasik <ovasik@redhat.com> - 8.5-10
- various fixes for case conversion in tr(#611274)

* Wed Sep 29 2010 jkeating - 8.5-9
- Rebuilt for gcc bug 634757

* Mon Sep 20 2010 Ondrej Vasik <ovasik@redhat.com> - 8.5-8
- change assertion failure for invalid multibyte input
  in sort to less confusing error message(#591352)

* Wed Sep 08 2010 Ondrej Vasik <ovasik@redhat.com> - 8.5-7
- add RELRO protection to su as well (#630017)

* Mon Sep 06 2010 Ondrej Vasik <ovasik@redhat.com> - 8.5-6
- compile su with pie again (#630017)

* Mon Aug 30 2010 Ondrej Vasik <ovasik@redhat.com> - 8.5-5
- fix double free abort in tac (#628213)

* Thu Jul 22 2010 Ondrej Vasik <ovasik@redhat.com> - 8.5-4
- Add .ear, .war, .sar , for Java jar-like archives to
  dircolors (#616497)

* Fri Jul  2 2010 Dan Horák <dan[at]danny.cz> - 8.5-3
- rebuilt with the updated configuration patch
- drop the old -O1 exception for s390(x)
- updated the getgrouplist patch (Kamil Dudka)

* Tue Apr 27 2010 Ondrej Vasik <ovasik@redhat.com> - 8.5-2
- doublequote LS_COLORS in colorls.*sh scripts to speedup
  shell start(#586029)
- add patch for mkstemp on sparc64(Dennis Gilmore)
- update /etc/DIR_COLORS* files

* Mon Apr 26 2010 Ondrej Vasik <ovasik@redhat.com> - 8.5-1
- new upstream release 8.5

* Thu Apr 15 2010 Ondrej Vasik <ovasik@redhat.com> - 8.4-8
- move readlink from /usr/bin to bin, keep symlink in
  /usr/bin(#580682)

* Mon Mar 29 2010 Kamil Dudka <kdudka@redhat.com> - 8.4-7
- a new option df --direct

* Sat Mar 20 2010 Ondrej Vasik <ovasik@redhat.com> - 8.4-6
- run tput colors in colorls profile.d scripts only
  in the interactive mode(#450424)

* Fri Feb 12 2010 Ondrej Vasik <ovasik@redhat.com> - 8.4-5
- fix exit status of terminated child processes in su with
  pam(#559098)

* Fri Feb 05 2010 Ondrej Vasik <ovasik@redhat.com> - 8.4-4
- do not depend on selinux patch application in
  _require_selinux tests(#556350)

* Fri Jan 29 2010 Ondrej Vasik <ovasik@redhat.com> - 8.4-3
- do not fail tests if there are no loopdevices left
  (#558898)

* Tue Jan 26 2010 Ondrej Vasik <ovasik@redhat.com> - 8.4-2
- who doesn't determine user's message status correctly
  (#454261)

* Thu Jan 14 2010 Ondrej Vasik <ovasik@redhat.com> - 8.4-1
- new upstream release 8.4

* Fri Jan 08 2010 Ondrej Vasik <ovasik@redhat.com> - 8.3-1
- new upstream release 8.3

* Wed Jan 06 2010 Ondrej Vasik <ovasik@redhat.com> - 8.2-6
- require gmp-devel/gmp for large numbers support(#552846)

* Sun Dec 27 2009 Ondrej Vasik <ovasik@redhat.com> - 8.2-5
- fix misc/selinux root-only test(#550494)

* Sat Dec 19 2009 Ondrej Vasik <ovasik@redhat.com> - 8.2-4
- bring back uname -p/-i functionality except of the
  athlon hack(#548834)
- comment patches

* Wed Dec 16 2009 Ondrej Vasik <ovasik@redhat.com> - 8.2-3
- use grep instead of deprecated egrep in colorls.sh script
  (#548174)
- remove unnecessary versioned requires/conflicts
- remove non-upstream hack for uname -p

* Wed Dec 16 2009 Ondrej Vasik <ovasik@redhat.com> - 8.2-2
- fix DIR_COLORS.256color file

* Fri Dec 11 2009 Ondrej Vasik <ovasik@redhat.com> - 8.2-1
- new upstream release 8.2
- removed applied patches, temporarily do not run dup_cloexec()
  dependent gnulib tests failing in koji

* Fri Nov 27 2009 Ondrej Vasik <ovasik@redhat.com> - 8.1-1
- new upstream release 8.1
- fix build under koji (no test failures with underlying
  RHEL-5 XEN kernel due to unsearchable path and lack of
  futimens functionality)

* Wed Oct 07 2009 Ondrej Vasik <ovasik@redhat.com> - 8.0-2
- update /etc/DIR_COLORS* files

* Wed Oct 07 2009 Ondrej Vasik <ovasik@redhat.com> - 8.0-1
- New upstream release 8.0 (beta), defuzz patches,
  remove applied patches

* Mon Oct 05 2009 Ondrej Vasik <ovasik@redhat.com> - 7.6-7
- chcon no longer aborts on a selinux disabled system
  (#527142)

* Fri Oct 02 2009 Ondrej Vasik <ovasik@redhat.com> - 7.6-6
- ls -LR exits with status 2, not 0, when it encounters
  a cycle(#525402)
- ls: print "?", not "0" as inode of dereferenced dangling
  symlink(#525400)
- call the install-info on .gz info files

* Tue Sep 22 2009 Ondrej Vasik <ovasik@redhat.com> - 7.6-5
- improve and correct runuser documentation (#524805)

* Mon Sep 21 2009 Ondrej Vasik <ovasik@redhat.com> - 7.6-4
- add dircolors color for GNU lzip (#516897)

* Fri Sep 18 2009 Ondrej Vasik <ovasik@redhat.com> - 7.6-3
- fixed typo in DIR_COLORS.256color causing no color for
  multihardlink

* Wed Sep 16 2009 Ondrej Vasik <ovasik@redhat.com> - 7.6-2
- fix copying of extended attributes for read only source
  files

* Sat Sep 12 2009 Ondrej Vasik <ovasik@redhat.com> - 7.6-1
- new upstream bugfix release 7.6, removed applied patches,
  defuzzed the rest

* Thu Sep 10 2009 Ondrej Vasik <ovasik@redhat.com> - 7.5-6
- fix double free error in fold for singlebyte locales
  (caused by multibyte patch)

* Tue Sep 08 2009 Ondrej Vasik <ovasik@redhat.com> - 7.5-5
- fix sort -h for multibyte locales (reported via
  http://bugs.archlinux.org/task/16022)

* Thu Sep 03 2009 Ondrej Vasik <ovasik@redhat.com> - 7.5-4
- fixed regression where df -l <device> as regular user
  cause "Permission denied" (#520630, introduced by fix for
  rhbz #497830)

* Fri Aug 28 2009 Ondrej Vasik <ovasik@redhat.com> - 7.5-3
- ls -i: print consistent inode numbers also for mount points
  (#453709)

* Mon Aug 24 2009 Ondrej Vasik <ovasik@redhat.com> - 7.5-2
- Better fix than workaround the koji insufficient utimensat
  support issue to prevent failures in other packages

* Fri Aug 21 2009 Ondrej Vasik <ovasik@redhat.com> - 7.5-1
- New upstream release 7.5, remove already applied patches,
  defuzz few others, xz in default set(by dependencies),
  so no explicit br required
- skip two new tests on system with insufficient utimensat
  support(e.g. koji)
- libstdbuf.so in separate coreutils-libs subpackage
- update /etc/DIRCOLORS*

* Thu Aug 06 2009 Ondrej Vasik <ovasik@redhat.com> - 7.4-6
- do process install-info only with info files present(#515970)
- BuildRequires for xz, use xz tarball

* Wed Aug 05 2009 Kamil Dudka <kdudka@redhat.com> - 7.4-5
- ls -1U with two or more arguments (or with -R or -s) works properly again
- install runs faster again with SELinux enabled (#479502)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 06 2009 Ondrej Vasik <ovasik@redhat.com> 7.4-3
- do not ignore sort's version sort for multibyte locales
  (#509688)

* Thu Jun 18 2009 Ondrej Vasik <ovasik@redhat.com> 7.4-2
- temporarily workaround probable kernel issue with
  TCSADRAIN(#504798)

* Mon May 25 2009 Ondrej Vasik <ovasik@redhat.com> 7.4-1
- new upstream release 7.4, removed applied patches

* Thu Apr 23 2009 Ondrej Vasik <ovasik@redhat.com> 7.2-3
- fix segfaults in join (i18n patch) when using multibyte
  locales(#497368)

* Fri Apr 17 2009 Ondrej Vasik <ovasik@redhat.com> 7.2-2
- make mv xattr support failures silent (as is done for
  cp -a) - #496142

* Tue Mar 31 2009 Ondrej Vasik <ovasik@redhat.com> 7.2-1
- New upstream bugfix release 7.2
- removed applied patches
- temporarily disable strverscmp failing gnulib test

* Thu Mar 19 2009 Ondrej Vasik <ovasik@redhat.com> 7.1-7
- do not ship /etc/DIR_COLORS.xterm - as many terminals
  use TERM xterm and black background as default - making
  ls color output unreadable
- shipping /etc/DIR_COLORS.lightbgcolor instead of it for
  light(white/gray) backgrounds
- try to preserve xattrs in cp -a when possible

* Mon Mar 02 2009 Ondrej Vasik <ovasik@redhat.com> 7.1-6
- fix sort bugs (including #485715) for multibyte locales
  as well

* Fri Feb 27 2009 Ondrej Vasik <ovasik@redhat.com> 7.1-5
- fix infinite loop in recursive cp (upstream, introduced
  by 7.1)

* Thu Feb 26 2009 Ondrej Vasik <ovasik@redhat.com> 7.1-4
- fix showing ACL's for ls -Z (#487374), fix automatic
  column width for it as well

* Wed Feb 25 2009 Ondrej Vasik <ovasik@redhat.com> 7.1-3
- fix couple of bugs (including #485715) in sort with
  determining end of fields(upstream)

* Wed Feb 25 2009 Ondrej Vasik <ovasik@redhat.com> 7.1-2
- workaround libcap issue with broken headers (#483548)
- fix gnulib testsuite failure (4x77 (skip) is not
  77(skip) ;) )

* Tue Feb 24 2009 Ondrej Vasik <ovasik@redhat.com> - 7.1-1
- New upstream release 7.1 (temporarily using tar.gz tarball
  as there are no xz utils in Fedora), removed applied
  patches, amended patches and LS_COLORS files

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 28 2009 Kamil Dudka <kdudka@redhat.com> - 7.0-7
- added BuildRequires for libattr-devel and attr

* Wed Jan 28 2009 Kamil Dudka <kdudka@redhat.com> - 7.0-6
- cp/mv: add --no-clobber (-n) option to not overwrite target
- cp/mv: add xattr support (#202823)

* Thu Dec 04 2008 Ondrej Vasik <ovasik@redhat.com> - 7.0-5
- fix info documentation for expr command as well(#474434)

* Thu Dec 04 2008 Ondrej Vasik <ovasik@redhat.com> - 7.0-4
- fixed syntax error w/ "expr" command using negative
  string/integer as first (i.e expr -125) - due to
  complexity of changes used diff against upstream git-head
  (#474434)
- enable total-awk test again (and skip it when df not working)

* Tue Nov 25 2008 Ondrej Vasik <ovasik@redhat.com> - 7.0-3
- package summary tuning

* Fri Nov 21 2008 Ondrej Vasik <ovasik@redhat.com> - 7.0-2
- added requirements for util-linux-ng >= 2.14
  because of file conflict in update from F-8/F-9(#472445)
- some sed cleanup, df totaltests patch changes (not working
  correctly yet :( )

* Wed Nov 12 2008 Ondrej Vasik <ovasik@redhat.com> - 7.0-1
- new upstream release
- modification/removal of related patches
- use automake 1.10.1 instead of 1.10a
- temporarily skip df --total tests (failures),
  timeout-paramaters (failure on ppc64)

* Mon Nov 03 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-17
- Requires: ncurses (#469277)

* Wed Oct 22 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-16
- make possible to disable capability in ls due to
  performance impact when not cached(#467508)
- do not patch generated manpages - generate them at build
  time
- do not mistakenly display -g and -G runuser option in su
  --help output

* Mon Oct 13 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-15
- fix several date issues(e.g. countable dayshifts, ignoring
  some cases of relative offset, locales conversions...)
- clarify ls exit statuses documentation (#446294)

* Sun Oct 12 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-14
- cp -Z now correctly separated in man page (#466646)
- cp -Z works again (#466653)
- make preservation of SELinux CTX non-mandatory for
  preserve=all cp option

* Wed Oct 08 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-13
- remove unimplemented (never accepted by upstream) option
  for chcon changes only. Removed from help and man.
- remove ugly lzma hack as lzma is now supported by setup
  macro

* Mon Oct 06 2008 Jarod Wilson <jarod@redhat.com> - 6.12-12
- fix up potential test failures when building in certain
  slightly quirky environments (part of bz#442352)

* Mon Oct 06 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-11
- added requires for libattr (#465569)

* Mon Sep 29 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-10
- seq should no longer fail to display final number of some
  float usages of seq with utf8 locales(#463556)

* Wed Aug 13 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-9
- mention that DISPLAY and XAUTHORITY envvars are preserved
  for pam_xauth in su -l (#450505)

* Mon Aug 04 2008 Kamil Dudka <kdudka@redhat.com> - 6.12-8
- ls -U1 now uses constant memory

* Wed Jul 23 2008 Kamil Dudka <kdudka@redhat.com> - 6.12-7
- dd: iflag=fullblock now read full blocks if possible
  (#431997, #449263)
- ls: --color now highlights files with capabilities (#449985)

* Wed Jul 16 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-6
- Get rid off fuzz in patches

* Fri Jul 04 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-5
- fix authors for basename and echo
- fix who info pages, print last runlevel only for printable
  chars

* Mon Jun 16 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-4
- print verbose output of chcon with newline after each 
  message (#451478)

* Fri Jun 06 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-3
- workaround for koji failures(#449910, #442352) now 
  preserves timestamps correctly - fallback to supported
  functions, added test case
- runuser binary is no longer doubled in /usr/bin/runuser

* Wed Jun 04 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-2
- workaround for strange koji failures(#449910,#442352)
- fixed ls -ZC segfault(#449866, introduced by 6.10-1 
  SELinux patch reworking) 

* Mon Jun 02 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-1
- New upstream release 6.12, adapted patches

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 6.11-5
- fix SHA256/SHA512 to work on sparc

* Tue May 20 2008 Ondrej Vasik <ovasik@redhat.com> - 6.11-4
- fixed a HUGE memory leak in install binary(#447410)

* Mon May 19 2008 Ondrej Vasik <ovasik@redhat.com> - 6.11-3
- added arch utility (from util-linux-ng)
- do not show executable file types without executable bit
  in colored ls as executable

* Wed Apr 23 2008 Ondrej Vasik <ovasik@redhat.com> - 6.11-2
- Do not show misleading scontext in id command when user
  is specified (#443485)
- Avoid possible test failures on non-english locales

* Mon Apr 21 2008 Ondrej Vasik <ovasik@redhat.com> - 6.11-1
- New upstream release 6.11 
- removed accepted patches + few minor patch changes

* Fri Apr 18 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-21
- fix wrong checksum line handling in sha1sum -c 
  command(#439531)

* Tue Apr 15 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-20
- fix possible segfault in sha1sum/md5sum command

* Mon Apr 14 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-19
- fix possible build-failure typo in i18n patch(#442205)

* Mon Apr  7 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-18
- fix colorls.sh syntax with Zsh (#440652)
- mention that cp -a includes -c option + mention cp -c 
  option in manpages (#440056)
- fix typo in runuser manpages (#439410)

* Sat Mar 29 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-17
- better workaround of glibc getoptc change(factor test)
- don't segfault mknod, mkfifo with invalid-selinux-context

* Thu Mar 27 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-16
- keep LS_COLORS when USER_LS_COLORS defined
- someupstream fixes:
- mkdir -Z invalid-selinux-context dir no longer segfaults
- ptx with odd number of backslashes no longer leads to buffer
  overflow
- paste -d'\' file" no longer ovveruns memory

* Wed Mar 26 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-15
- covered correct handling for some test conditions failures
  e.g. root build+selinux active and not running mcstrans(d)
  or selinux enforcing (#436717)

* Wed Mar 19 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-14
- mv: never unlink a destination file before calling rename
  (upstream, #438076)

* Mon Mar 17 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-13
- disable echo option separator behavior(added by #431005,
  request for removal #437653 + upstream)
- temporarily disabled longoptions change until full 
  clarification upstreamery (#431005)

* Tue Mar 11 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-12
- fixed harmless double close of stdout in dd(#436368)

* Thu Mar  6 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-11
- fixed broken order of params in stat(#435669)

* Tue Mar  4 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-10
- colorls.csh missing doublequotes (#435789)
- fixed possibility to localize verbose outputs

* Mon Mar  3 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-9
- consolidation of verbose output to stdout (upstream)

* Mon Feb 18 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-8
- use default security context in install - broken by 
  coreutils-6.10 update(#319231)
- some sh/csh scripts optimalizations(by ville.skytta@iki.fi,
  - #433189, #433190)

* Mon Feb 11 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-7
- keep old csh/sh usermodified colorls shell scripts
  but use the new ones(#432154)

* Thu Feb  7 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-6
- better 256-color support in colorls shell scripts
- color tuning(based on feedback in #429121)

* Mon Feb  4 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-5
- enabled 256-color support in colorls shell scripts(#429121)
- fixed syntax error in csh script(#431315)

* Thu Jan 31 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-4
- forgotten return in colorls.sh change

* Thu Jan 31 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-3
- fix unability of echo to display certain strings(added --
  separator, #431005)
- do not require only one long_opt for certain commands 
  e.g. sleep, yes - but use first usable (#431005)
- do not override userspecified LS_COLORS variable, but
  use it for colored ls(#430827)
- discard errors from dircolors to /dev/null + some tuning 
  of lscolor sh/csh scripts(#430823)
- do not consider files with SELinux security context as
  files having ACL in ls long format(#430779)

* Mon Jan 28 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-2
- some manpages improvements(#406981,#284881)
- fix non-versioned obsoletes of mktemp(#430407)

* Fri Jan 25 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-1
- New upstream release(changed %%prep because of lack of lzma
  support in %%setup macro)
- License GPLv3+
- removed patches cp-i-u,du-ls-upstream,statsecuritycontext,
  futimens,getdateYYYYMMDD,ls-x
- modified patches to be compilable after upstream changes
- selinux patch reworked to have backward compatibility with
  F8(cp,ls and stat behaviour differ from upstream in SELinux
  options)
- su-l/runuser-l pam file usage a bit documented(#368721)
- more TERMs for DIR_COLORS, added colors for audio files,
  more image/compress file types(taken from upstream 
  dircolors.hin)
- new file DIR_COLORS.256color which takes advantage from 
  256color term types-not really used yet(#429121)

* Wed Jan 16 2008 Ondrej Vasik <ovasik@redhat.com> - 6.9-17
- added several missing colored TERMs(including rxvt-unicode,
  screen-256color and xterm-256color) to DIR_COLORS and
  DIR_COLORS.xterm(#239266) 

* Wed Dec 05 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-16
- fix displaying of security context in stat(#411181)

* Thu Nov 29 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-15
- completed fix of wrong colored broken symlinks in ls(#404511)

* Fri Nov 23 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-14
- fixed bug in handling YYYYMMDD date format with relative
  signed offset(#377821)

* Tue Nov 13 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-13
- fixed bug in selinux patch which caused bad preserving
  of security context in install(#319231)

* Fri Nov 02 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-12
- added some upstream supported dircolors TERMs(#239266)
- fixed du output for unaccesible dirs(#250089)
- a bit of upstream tunning for symlinks

* Tue Oct 30 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-11
- allow cp -a to rewrite file on different filesystem(#219900)
  (based on upstream patch)

* Mon Oct 29 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-10
- modified coreutils-i18n.patch because of sort -R in
  a non C locales(fix by Andreas Schwab) (#249315)

* Mon Oct 29 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-9
- applied upstream patch for runuser to coreutils-selinux.patch(#232652)
- License tag to GPLv2+

* Thu Oct 25 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-8
- applied upstream patch for cp and mv(#248591)

* Thu Aug 23 2007 Pete Graner <pgraner@redhat.com> - 6.9-7
- Fix typo in spec file. (CVS merge conflict leftovers)

* Thu Aug 23 2007 Pete Graner <pgraner@redhat.com> - 6.9-6
- Remove --all-name from spec file its now provided in the upstream rpm's find-lang.sh
- Rebuild

* Tue Aug 14 2007 Tim Waugh <twaugh@redhat.com> 6.9-5
- Don't generate runuser.1 since we ship a complete manpage for it
  (bug #241662).

* Wed Jul  4 2007 Tim Waugh <twaugh@redhat.com> 6.9-4
- Use hard links instead of symbolic links for LC_TIME files (bug #246729).

* Wed Jun 13 2007 Tim Waugh <twaugh@redhat.com> 6.9-3
- Fixed 'ls -x' output (bug #240298).
- Disambiguate futimens() from the glibc implementation (bug #242321).

* Mon Apr 02 2007 Karsten Hopp <karsten@redhat.com> 6.9-2
- /bin/mv in %%post requires libselinux

* Mon Mar 26 2007 Tim Waugh <twaugh@redhat.com> 6.9-1
- 6.9.

* Fri Mar  9 2007 Tim Waugh <twaugh@redhat.com>
- Better install-info scriptlets (bug #225655).

* Thu Mar  1 2007 Tim Waugh <twaugh@redhat.com> 6.8-1
- 6.8+, in preparation for 6.9.

* Thu Feb 22 2007 Tim Waugh <twaugh@redhat.com> 6.7-9
- Use sed instead of perl for text replacement (bug #225655).
- Use install-info scriptlets from the guidelines (bug #225655).

* Tue Feb 20 2007 Tim Waugh <twaugh@redhat.com> 6.7-8
- Don't mark profile scripts as config files (bug #225655).
- Avoid extra directory separators (bug #225655).

* Mon Feb 19 2007 Tim Waugh <twaugh@redhat.com> 6.7-7
- Better Obsoletes/Provides versioning (bug #225655).
- Use better defattr (bug #225655).
- Be info file compression tolerant (bug #225655).
- Moved changelog compression to %%install (bug #225655).
- Prevent upstream changes being masked (bug #225655).
- Added a comment (bug #225655).
- Use install -p for non-compiled files (bug #225655).
- Use sysconfdir macro for /etc (bug #225655).
- Use Requires(pre) etc for install-info (bug #225655).

* Fri Feb 16 2007 Tim Waugh <twaugh@redhat.com> 6.7-6
- Provide version for stat (bug #225655).
- Fixed permissions on profile scripts (bug #225655).

* Wed Feb 14 2007 Tim Waugh <twaugh@redhat.com> 6.7-5
- Removed unnecessary stuff in pre scriptlet (bug #225655).
- Prefix sources with 'coreutils-' (bug #225655).
- Avoid %%makeinstall (bug #225655).

* Tue Feb 13 2007 Tim Waugh <twaugh@redhat.com> 6.7-4
- Ship COPYING file (bug #225655).
- Use datadir and infodir macros in %%pre scriptlet (bug #225655).
- Use spaces not tabs (bug #225655).
- Fixed build root.
- Change prereq to requires (bug #225655).
- Explicitly version some obsoletes tags (bug #225655).
- Removed obsolete pl translation fix.

* Mon Jan 22 2007 Tim Waugh <twaugh@redhat.com> 6.7-3
- Make scriptlet unconditionally succeed (bug #223681).

* Fri Jan 19 2007 Tim Waugh <twaugh@redhat.com> 6.7-2
- Build does not require libtermcap-devel.

* Tue Jan  9 2007 Tim Waugh <twaugh@redhat.com> 6.7-1
- 6.7.  No longer need sort-compatibility, rename, newhashes, timestyle,
  acl, df-cifs, afs or autoconf patches.

* Tue Jan  2 2007 Tim Waugh <twaugh@redhat.com>
- Prevent 'su --help' showing runuser-only options such as --group.

* Fri Nov 24 2006 Tim Waugh <twaugh@redhat.com> 5.97-16
- Unbreak id (bug #217177).

* Thu Nov 23 2006 Tim Waugh <twaugh@redhat.com> 5.97-15
- Fixed stat's 'C' format specifier (bug #216676).
- Misleading 'id -Z root' error message (bug #211089).

* Fri Nov 10 2006 Tim Waugh <twaugh@redhat.com> 5.97-14
- Clarified runcon man page (bug #213846).

* Tue Oct 17 2006 Tim Waugh <twaugh@redhat.com> 5.97-13
- Own LC_TIME locale directories (bug #210751).

* Wed Oct  4 2006 Tim Waugh <twaugh@redhat.com> 5.97-12
- Fixed 'cp -Z' when destination exists, again (bug #189967).

* Thu Sep 28 2006 Tim Waugh <twaugh@redhat.com> 5.97-11
- Back-ported rename patch (bug #205744).

* Tue Sep 12 2006 Tim Waugh <twaugh@redhat.com> 5.97-10
- Ignore 'cifs' filesystems for 'df -l' (bug #183703).
- Include -g/-G in runuser man page (part of bug #199344).
- Corrected runuser man page (bug #200620).

* Thu Aug 24 2006 Tim Waugh <twaugh@redhat.com> 5.97-9
- Fixed warnings in pam, i18n, sysinfo, selinux and acl patches (bug #203166).

* Wed Aug 23 2006 Tim Waugh <twaugh@redhat.com> 5.97-8
- Don't chdir until after PAM bits in su (bug #197659).

* Tue Aug 15 2006 Tim Waugh <twaugh@redhat.com> 5.97-7
- Fixed 'sort -b' multibyte problem (bug #199986).

* Fri Jul 21 2006 Tim Waugh <twaugh@redhat.com> 5.97-6
- Added runuser '-g' and '-G' options (bug #199344).
- Added su '--session-command' option (bug #199066).

* Tue Jul 18 2006 Tomas Mraz <tmraz@redhat.com> 5.97-5
- 'include' su and runuser scripts in su-l and runuser-l scripts

* Thu Jul 13 2006 David Howells <dhowells@redhat.com> 5.97-4
- split the PAM scripts for "su -l"/"runuser -l" from that of normal "su" and
  "runuser" (#198639)
- add keyinit instructions to PAM scripts

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 5.97-3.1
- rebuild

* Tue Jul 11 2006 Tomas Mraz <tmraz@redhat.com> 5.97-3
- allow root to su to expired user (#152420)

* Thu Jun 29 2006 Tim Waugh <twaugh@redhat.com> 5.97-2
- Allow 'sort +1 -2' (patch from upstream).

* Sun Jun 25 2006 Tim Waugh <twaugh@redhat.com> 5.97-1
- 5.97.  No longer need tempname or tee patches, or pl translation.

* Sun Jun 25 2006 Tim Waugh <twaugh@redhat.com> 5.96-4
- Include new hashes (bug #196369).  Patch from upstream.
- Build at -O1 on s390 for the moment (bug #196369).

* Fri Jun  9 2006 Tim Waugh <twaugh@redhat.com>
- Fix large file support for temporary files.

* Mon Jun  5 2006 Tim Waugh <twaugh@redhat.com> 5.96-3
- Fixed Polish translation.

* Mon May 22 2006 Tim Waugh <twaugh@redhat.com> 5.96-2
- 5.96.  No longer need proc patch.

* Fri May 19 2006 Tim Waugh <twaugh@redhat.com>
- Fixed pr properly in multibyte locales (bug #192381).

* Tue May 16 2006 Tim Waugh <twaugh@redhat.com> 5.95-3
- Upstream patch to fix cp -p when proc is not mounted (bug #190601).
- BuildRequires libacl-devel.

* Mon May 15 2006 Tim Waugh <twaugh@redhat.com>
- Fixed pr in multibyte locales (bug #189663).

* Mon May 15 2006 Tim Waugh <twaugh@redhat.com> 5.95-2
- 5.95.

* Wed Apr 26 2006 Tim Waugh <twaugh@redhat.com> 5.94-4
- Avoid redeclared 'tee' function.
- Fix 'cp -Z' when the destination exists (bug #189967).

* Thu Apr 20 2006 Tim Waugh <twaugh@redhat.com> 5.94-3
- Make 'ls -Z' output more consistent with other output formats.

* Fri Mar 24 2006 Tim Waugh <twaugh@redhat.com> 5.94-2
- 5.94.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 5.93-7.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 5.93-7.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 23 2006 Tim Waugh <twaugh@redhat.com>
- Fixed chcon(1) bug reporting address (bug #178523).

* Thu Jan  5 2006 Tim Waugh <twaugh@redhat.com> 5.93-7
- Don't suppress chown/chgrp errors in install(1) (bug #176708).

* Mon Jan  2 2006 Dan Walsh <dwalsh@redhat.com> 5.93-6
- Remove pam_selinux.so from su.pamd, not needed for targeted and Strict/MLS 
  will have to newrole before using.

* Fri Dec 23 2005 Tim Waugh <twaugh@redhat.com> 5.93-5
- Fix "sort -n" (bug #176468).

* Fri Dec 16 2005 Tim Waugh <twaugh@redhat.com>
- Explicitly set default POSIX2 version during configure stage.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec  2 2005 Tim Waugh <twaugh@redhat.com>
- Parametrize SELinux (bug #174067).
- Fix runuser.pamd (bug #173807).

* Thu Nov 24 2005 Tim Waugh <twaugh@redhat.com> 5.93-4
- Rebuild to pick up new glibc *at functions.
- Apply runuser PAM patch from bug #173807.  Ship runuser PAM file.

* Tue Nov 15 2005 Dan Walsh <dwalsh@redhat.com> 5.93-3
- Remove multiple from su.pamd

* Mon Nov 14 2005 Tim Waugh <twaugh@redhat.com> 5.93-2
- Call setsid() in su under some circumstances (bug #173008).
- Prevent runuser operating when setuid (bug #173113).

* Tue Nov  8 2005 Tim Waugh <twaugh@redhat.com> 5.93-1
- 5.93.
- No longer need alt-md5sum-binary, dircolors, mkdir, mkdir2 or tac patches.

* Fri Oct 28 2005 Tim Waugh <twaugh@redhat.com> 5.92-1
- Finished porting i18n patch to sort.c.
- Fixed for sort-mb-tests (avoid +n syntax).

* Fri Oct 28 2005 Tim Waugh <twaugh@redhat.com> 5.92-0.2
- Fix chgrp basic test.
- Include md5sum patch from ALT.

* Mon Oct 24 2005 Tim Waugh <twaugh@redhat.com> 5.92-0.1
- 5.92.
- No longer need afs, dircolors, utmp, gcc4, brokentest, dateseconds,
  chown, rmaccess, copy, stale-utmp, no-sign-extend, fchown patches.
- Updated acl, dateman, pam, langinfo, i18n, getgrouplist, selinux patches.
- Dropped printf-ll, allow_old_options, jday, zh_CN patches.
- NOTE: i18n patch not ported for sort(1) yet.

* Fri Sep 30 2005 Tomas Mraz <tmraz@redhat.com> - 5.2.1-56
- use include instead of pam_stack in pam config

* Fri Sep 9 2005 Dan Walsh <dwalsh@redhat.com> 5.2.1-55
- Reverse change to use raw functions

* Thu Sep  8 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-54
- Explicit setuid bit for /bin/su in file manifest (bug #167745).

* Tue Sep 6 2005 Dan Walsh <dwalsh@redhat.com> 5.2.1-53
- Allow id to run even when SELinux security context can not be run
- Change chcon to use raw functions.

* Tue Jun 28 2005 Tim Waugh <twaugh@redhat.com>
- Corrected comments in DIR_COLORS.xterm (bug #161711).

* Wed Jun 22 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-52
- Fixed stale-utmp patch so that 'who -r' and 'who -b' work
  again (bug #161264).

* Fri Jun 17 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-51
- Use upstream hostid fix.

* Thu Jun 16 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-50
- Don't display the sign-extended part of the host id (bug #160078).

* Tue May 31 2005 Dan Walsh <dwalsh@redhat.com> 5.2.1-49
- Eliminate bogus "can not preserve context" message when moving files.

* Wed May 25 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-48
- Prevent buffer overflow in who(1) (bug #158405).

* Fri May 20 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-47
- Better error checking in the pam patch (bug #158189).

* Mon May 16 2005 Dan Walsh <dwalsh@redhat.com> 5.2.1-46
- Fix SELinux patch to better handle MLS integration

* Mon May 16 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-45
- Applied Russell Coker's selinux changes (bug #157856).

* Fri Apr  8 2005 Tim Waugh <twaugh@redhat.com>
- Fixed pam patch from Steve Grubb (bug #154946).
- Use better upstream patch for "stale utmp".

* Tue Mar 29 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-44
- Added "stale utmp" patch from upstream.

* Thu Mar 24 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-43
- Removed patch that adds -C option to install(1).

* Wed Mar 16 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-42
- Fixed pam patch.
- Fixed broken configure test.
- Fixed build with GCC 4 (bug #151045).

* Wed Feb  9 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-41
- Jakub Jelinek's sort -t multibyte fixes (bug #147567).

* Sat Feb  5 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-40
- Undo last change (bug #145266).

* Fri Feb  4 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-38
- Special case for ia32e in uname (bug #145266).

* Thu Jan 13 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-37
- Fixed zh_CN translation (bug #144845).  Patch from Mitrophan Chin.

* Tue Dec 28 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-36
- Fix to only setdefaultfilecon if not overridden by command line

* Mon Dec 27 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-35
- Change install to restorecon if it can

* Wed Dec 15 2004 Tim Waugh <twaugh@redhat.com>
- Fixed small bug in i18n patch.

* Mon Dec  6 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-34
- Don't set fs uid until after pam_open_session (bug #77791).

* Thu Nov 25 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-33
- Fixed colorls.csh (bug #139988).  Patch from Miloslav Trmac.

* Mon Nov  8 2004 Tim Waugh <twaugh@redhat.com>
- Updated URL (bug #138279).

* Mon Oct 25 2004 Steve Grubb <sgrubb@redhat.com> 5.2.1-32
- Handle the return code of function calls in runcon.

* Mon Oct 18 2004 Tim Waugh <twaugh@redhat.com>
- Prevent compiler warning in coreutils-i18n.patch (bug #136090).

* Tue Oct  5 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-31
- getgrouplist() patch from Ulrich Drepper.
- The selinux patch should be applied last.

* Mon Oct  4 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-30
- Mv runuser to /sbin

* Mon Oct  4 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-28
- Fix runuser man page.

* Mon Oct  4 2004 Tim Waugh <twaugh@redhat.com>
- Fixed build.

* Fri Sep 24 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-26
- Add runuser as similar to su, but only runable by root

* Fri Sep 24 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-25
- chown(1) patch from Ulrich Drepper.

* Tue Sep 14 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-24
- SELinux patch fix: don't display '(null)' if getfilecon() fails
  (bug #131196).

* Fri Aug 20 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-23
- Fixed colorls.csh quoting (bug #102412).
- Fixed another join LSB test failure (bug #121153).

* Mon Aug 16 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-22
- Fixed sort -t LSB test failure (bug #121154).
- Fixed join LSB test failure (bug #121153).

* Wed Aug 11 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-21
- Apply upstream patch to fix 'cp -a' onto multiply-linked files (bug #128874).
- SELinux patch fix: don't error out if lgetfilecon() returns ENODATA.

* Tue Aug 10 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-20
- Added 'konsole' TERM to DIR_COLORS (bug #129544).

* Wed Aug  4 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-19
- Added 'gnome' TERM to DIR_COLORS (bug #129112).
- Worked around a bash bug #129128.
- Fixed an i18n patch bug in cut (bug #129114).

* Tue Aug  3 2004 Tim Waugh <twaugh@redhat.com>
- Fixed colorls.{sh,csh} so that the l. and ll aliases are always defined
  (bug #128948).

* Tue Jul 13 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-18
- Fixed field extraction in sort (bug #127694).

* Fri Jun 25 2004 Tim Waugh <twaugh@redhat.com>
- Added 'TERM screen.linux' to DIR_COLORS (bug #78816).

* Wed Jun 23 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-17
- Move pam-xauth to after pam-selinux

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun  7 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-15
- Fix ls -Z (bug #125447).

* Fri Jun  4 2004 Tim Waugh <twaugh@redhat.com>
- Build requires bison (bug #125290).

* Fri Jun  4 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-14
- Fix selinux patch causing problems with ls --format=... (bug #125238).

* Thu Jun 3 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-13
- Change su to use pam_selinux open and pam_selinux close

* Wed Jun  2 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-12
- Don't call access() on symlinks about to be removed (bug #124699).

* Wed Jun  2 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-11
- Fix ja translation (bug #124862).

* Tue May 18 2004 Jeremy Katz <katzj@redhat.com> 5.2.1-10
- rebuild

* Mon May 17 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-9
- Mention pam in the info for su (bug #122592).
- Remove wheel group rant again (bug #122886).
- Change default behaviour for chgrp/chown (bug #123263).  Patch from
  upstream.

* Mon May 17 2004 Thomas Woerner <twoerner@redhat.com> 5.2.1-8
- compiling su PIE

* Wed May 12 2004 Tim Waugh <twaugh@redhat.com>
- Build requires new versions of autoconf and automake (bug #123098).

* Tue May  4 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-7
- Fix join -t (bug #122435).

* Tue Apr 20 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-6
- Fix 'ls -Z' displaying users/groups if stat() failed (bug #121292).

* Fri Apr 9 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-5
- Add ls -LZ fix
- Fix chcon to handle "."

* Wed Mar 17 2004 Tim Waugh <twaugh@redhat.com>
- Apply upstream fix for non-zero seconds for --date="10:00 +0100".

* Tue Mar 16 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-3
- If preserve fails, report as warning unless user requires preserve

* Tue Mar 16 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-2
- Make mv default to preserve on context

* Sat Mar 13 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-1
- 5.2.1.

* Fri Mar 12 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-9
- Add '-Z' to 'ls --help' output (bug #118108).

* Fri Mar  5 2004 Tim Waugh <twaugh@redhat.com>
- Fix deref-args test case for rebuilding under SELinux (bug #117556).

* Wed Feb 25 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-8
- kill(1) offloaded to util-linux altogether.

* Tue Feb 24 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-7
- Ship the real '[', not a symlink.

* Mon Feb 23 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-6
- Apply Paul Eggert's chown patch (bug #116536).
- Merged chdir patch into pam patch where it belongs.

* Mon Feb 23 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-5
- Fixed i18n patch bug causing sort -M not to work (bug #116575).

* Sat Feb 21 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-4
- Reinstate kill binary, just not its man page (bug #116463).

* Sat Feb 21 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-3
- Updated ls-stat patch.

* Fri Feb 20 2004 Dan Walsh <dwalsh@redhat.com> 5.2.0-2
- fix chcon to ignore . and .. directories for recursing

* Fri Feb 20 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-1
- Patch ls so that failed stat() is handled gracefully (Ulrich Drepper).
- 5.2.0.

* Thu Feb 19 2004 Tim Waugh <twaugh@redhat.com>
- More AFS patch tidying.

* Wed Feb 18 2004 Dan Walsh <dwalsh@redhat.com> 5.1.3-0.2
- fix chcon to handle -h qualifier properly, eliminate potential crash 

* Wed Feb 18 2004 Tim Waugh <twaugh@redhat.com>
- Stop 'sort -g' leaking memory (i18n patch bug #115620).
- Don't ship kill, since util-linux already does.
- Tidy AFS patch.

* Mon Feb 16 2004 Tim Waugh <twaugh@redhat.com> 5.1.3-0.1
- 5.1.3.
- Patches ported forward or removed.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 5.0-40
- rebuilt

* Tue Jan  20 2004 Dan Walsh <dwalsh@redhat.com> 5.0-39
- Change /etc/pam.d/su to remove preservuser and add multiple

* Tue Jan  20 2004 Dan Walsh <dwalsh@redhat.com> 5.0-38
- Change is_selinux_enabled to is_selinux_enabled > 0

* Tue Jan  20 2004 Dan Walsh <dwalsh@redhat.com> 5.0-37
- Add pam_selinux to pam file to allow switching of roles within selinux

* Fri Jan 16 2004 Tim Waugh <twaugh@redhat.com>
- The textutils-2.0.17-mem.patch is no longer needed.

* Thu Jan 15 2004 Tim Waugh <twaugh@redhat.com> 5.0-36
- Fixed autoconf test causing builds to fail.

* Tue Dec  9 2003 Dan Walsh <dwalsh@redhat.com> 5.0-35
- Fix copying to non xattr files

* Thu Dec  4 2003 Tim Waugh <twaugh@redhat.com> 5.0-34.sel
- Fix column widths problems in ls.

* Tue Dec  2 2003 Tim Waugh <twaugh@redhat.com> 5.0-33.sel
- Speed up md5sum by disabling speed-up asm.

* Wed Nov 19 2003 Dan Walsh <dwalsh@redhat.com> 5.0-32.sel
- Try again

* Wed Nov 19 2003 Dan Walsh <dwalsh@redhat.com> 5.0-31.sel
- Fix move on non SELinux kernels

* Fri Nov 14 2003 Tim Waugh <twaugh@redhat.com> 5.0-30.sel
- Fixed useless acl dependencies (bug #106141).

* Fri Oct 24 2003 Dan Walsh <dwalsh@redhat.com> 5.0-29.sel
- Fix id -Z

* Tue Oct 21 2003 Dan Walsh <dwalsh@redhat.com> 5.0-28.sel
- Turn on SELinux
- Fix chcon error handling

* Wed Oct 15 2003 Dan Walsh <dwalsh@redhat.com> 5.0-28
- Turn off SELinux

* Mon Oct 13 2003 Dan Walsh <dwalsh@redhat.com> 5.0-27.sel
- Turn on SELinux

* Mon Oct 13 2003 Dan Walsh <dwalsh@redhat.com> 5.0-27
- Turn off SELinux

* Mon Oct 13 2003 Dan Walsh <dwalsh@redhat.com> 5.0-26.sel
- Turn on SELinux

* Sun Oct 12 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- allow compiling without pam support

* Fri Oct 10 2003 Tim Waugh <twaugh@redhat.com> 5.0-23
- Make split(1) handle large files (bug #106700).

* Thu Oct  9 2003 Dan Walsh <dwalsh@redhat.com> 5.0-22
- Turn off SELinux

* Wed Oct  8 2003 Dan Walsh <dwalsh@redhat.com> 5.0-21.sel
- Cleanup SELinux patch

* Fri Oct  3 2003 Tim Waugh <twaugh@redhat.com> 5.0-20
- Restrict ACL support to only those programs needing it (bug #106141).
- Fix default PATH for LSB (bug #102567).

* Thu Sep 11 2003 Dan Walsh <dwalsh@redhat.com> 5.0-19
- Turn off SELinux

* Wed Sep 10 2003 Dan Walsh <dwalsh@redhat.com> 5.0-18.sel
- Turn on SELinux

* Fri Sep 5 2003 Dan Walsh <dwalsh@redhat.com> 5.0-17
- Turn off SELinux

* Tue Sep 2 2003 Dan Walsh <dwalsh@redhat.com> 5.0-16.sel
- Only call getfilecon if the user requested it.
- build with selinux

* Wed Aug 20 2003 Tim Waugh <twaugh@redhat.com> 5.0-14
- Documentation fix (bug #102697).

* Tue Aug 12 2003 Tim Waugh <twaugh@redhat.com> 5.0-13
- Made su use pam again (oops).
- Fixed another i18n bug causing sort --month-sort to fail.
- Don't run dubious stty test, since it fails when backgrounded
  (bug #102033).
- Re-enable make check.

* Fri Aug  8 2003 Tim Waugh <twaugh@redhat.com> 5.0-12
- Don't run 'make check' for this build (build environment problem).
- Another uninitialized variable in i18n (from bug #98683).

* Wed Aug 6 2003 Dan Walsh <dwalsh@redhat.com> 5.0-11
- Internationalize runcon
- Update latest chcon from NSA

* Wed Jul 30 2003 Tim Waugh <twaugh@redhat.com>
- Re-enable make check.

* Wed Jul 30 2003 Tim Waugh <twaugh@redhat.com> 5.0-9
- Don't run 'make check' for this build (build environment problem).

* Mon Jul 28 2003 Tim Waugh <twaugh@redhat.com> 5.0-8
- Actually use the ACL patch (bug #100519).

* Wed Jul 16 2003 Dan Walsh <dwalsh@redhat.com> 5.0-7
- Convert to SELinux

* Mon Jun  9 2003 Tim Waugh <twaugh@redhat.com>
- Removed samefile patch.  Now the test suite passes.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 28 2003 Tim Waugh <twaugh@redhat.com> 5.0-5
- Both kon and kterm support colours (bug #83701).
- Fix 'ls -l' alignment in zh_CN locale (bug #88346).

* Mon May 12 2003 Tim Waugh <twaugh@redhat.com> 5.0-4
- Prevent file descriptor leakage in du (bug #90563).
- Build requires recent texinfo (bug #90439).

* Wed Apr 30 2003 Tim Waugh <twaugh@redhat.com> 5.0-3
- Allow obsolete options unless POSIXLY_CORRECT is set.

* Sat Apr 12 2003 Tim Waugh <twaugh@redhat.com>
- Fold bug was introduced by i18n patch; fixed there instead.

* Fri Apr 11 2003 Matt Wilson <msw@redhat.com> 5.0-2
- fix segfault in fold (#88683)

* Sat Apr  5 2003 Tim Waugh <twaugh@redhat.com> 5.0-1
- 5.0.

* Mon Mar 24 2003 Tim Waugh <twaugh@redhat.com>
- Use _smp_mflags.

* Mon Mar 24 2003 Tim Waugh <twaugh@redhat.com> 4.5.11-2
- Remove overwrite patch.
- No longer seem to need nolibrt, errno patches.

* Thu Mar 20 2003 Tim Waugh <twaugh@redhat.com>
- No longer seem to need danglinglink, prompt, lug, touch_errno patches.

* Thu Mar 20 2003 Tim Waugh <twaugh@redhat.com> 4.5.11-1
- 4.5.11.
- Use packaged readlink.

* Wed Mar 19 2003 Tim Waugh <twaugh@redhat.com> 4.5.10-1
- 4.5.10.
- Update lug, touch_errno, acl, utmp, printf-ll, i18n, test-bugs patches.
- Drop fr_fix, LC_TIME, preserve, regex patches.

* Wed Mar 12 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-21
- Fixed another i18n patch bug (bug #82032).

* Tue Mar 11 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-20
- Fix sort(1) efficiency in multibyte encoding (bug #82032).

* Tue Feb 18 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-19
- Ship readlink(1) (bug #84200).

* Thu Feb 13 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-18
- Deal with glibc < 2.2 in %%pre scriplet (bug #84090).

* Wed Feb 12 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-16
- Require glibc >= 2.2 (bug #84090).

* Tue Feb 11 2003 Bill Nottingham <notting@redhat.com> 4.5.3-15
- fix group (#84095)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 4.5.3-14
- rebuilt

* Thu Jan 16 2003 Tim Waugh <twaugh@redhat.com>
- Fix rm(1) man page.

* Thu Jan 16 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-13
- Fix re_compile_pattern check.
- Fix su hang (bug #81653).

* Tue Jan 14 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-11
- Fix memory size calculation.

* Tue Dec 17 2002 Tim Waugh <twaugh@redhat.com> 4.5.3-10
- Fix mv error message (bug #79809).

* Mon Dec 16 2002 Tim Powers <timp@redhat.com> 4.5.3-9
- added PreReq on grep

* Fri Dec 13 2002 Tim Waugh <twaugh@redhat.com>
- Fix cp --preserve with multiple arguments.

* Thu Dec 12 2002 Tim Waugh <twaugh@redhat.com> 4.5.3-8
- Turn on colorls for screen (bug #78816).

* Mon Dec  9 2002 Tim Waugh <twaugh@redhat.com> 4.5.3-7
- Fix mv (bug #79283).
- Add patch27 (nogetline).

* Sun Dec  1 2002 Tim Powers <timp@redhat.com> 4.5.3-6
- use the su.pamd from sh-utils since it works properly with multilib systems

* Fri Nov 29 2002 Tim Waugh <twaugh@redhat.com> 4.5.3-5
- Fix test suite quoting problems.

* Fri Nov 29 2002 Tim Waugh <twaugh@redhat.com> 4.5.3-4
- Fix scriplets.
- Fix i18n patch so it doesn't break uniq.
- Fix several other patches to either make the test suite pass or
  not run the relevant tests.
- Run 'make check'.
- Fix file list.

* Thu Nov 28 2002 Tim Waugh <twaugh@redhat.com> 4.5.3-3
- Adapted for Red Hat Linux.
- Self-host for help2man.
- Don't ship readlink just yet (maybe later).
- Merge patches from fileutils and sh-utils (textutils ones are already
  merged it seems).
- Keep the binaries where the used to be (in particular, id and stat).

* Sun Nov 17 2002 Stew Benedict <sbenedict@mandrakesoft.com> 4.5.3-2mdk
- LI18NUX/LSB compliance (patch800)
- Installed (but unpackaged) file(s) - /usr/share/info/dir

* Thu Oct 31 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.3-1mdk
- new release
- rediff patch 180
- merge patch 150 into 180

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-6mdk
- move su back to /bin

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-5mdk
- patch 0 : lg locale is illegal and must be renamed lug (pablo)

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-4mdk
- fix conflict with procps

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-3mdk
- patch 105 : fix install -s

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-2mdk
- fix build
- don't chmode two times su
- build with large file support
- fix description
- various spec cleanups
- fix chroot installation
- fix missing /bin/env
- add old fileutils, sh-utils & textutils ChangeLogs

* Fri Oct 11 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-1mdk
- initial release (merge fileutils, sh-utils & textutils)
- obsoletes/provides: sh-utils/fileutils/textutils
- fileutils stuff go in 1xx range
- sh-utils stuff go in 7xx range
- textutils stuff go in 5xx range
- drop obsoletes patches 1, 2, 10 (somes files're gone but we didn't ship
  most of them)
- rediff patches 103, 105, 111, 113, 180, 706
- temporary disable patch 3 & 4
- fix fileutils url
