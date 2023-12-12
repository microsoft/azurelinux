%global desc OrangeFS (formerly PVFS2) is a high-performance parallel \
network file system designed for use on high performance computing \
systems.  It provides very high performance access to disk storage for \
parallel applications.  It is accessible through a variety of \
interfaces, including the native OrangeFS library, the kernel, FUSE, \
and MPI-IO. \
\
This package provides the pvfs2-client-core which is required to use \
the kernel module.
Summary:        Parallel network file system client
Name:           orangefs
Version:        2.9.8
Release:        3%{?dist}
# ASL 2.0 src/client/jni
# BSD (2 clause) maint/config/ssl.m4
# BSD (3 clause) src/client/usrint/fts.c
# BSD (3 clause) src/client/usrint/fts.h
# GPLv2 src/kernel
# LGPLv2 src/apps/admin/pvfs2-config.in
# LGPLv2 src/common/dotconf/dotconf.c
# LGPLv2+ remainder
# MIT maint/config/install-sh
# OpenLDAP src/apps/devel/lmdb and src/common/lmdb
# Public Domain src/common/hash/murmur3.c
# zlib src/common/misc/md5.c
# zlib src/common/misc/md5.h
License:        ASL 2.0 AND BSD AND GPLv2 AND LGPLv2+ AND LGPLv2 AND MIT AND OpenLDAP AND Public Domain AND zlib
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.orangefs.org/
Source0:        https://s3.amazonaws.com/download.orangefs.org/current/source/%{name}-%{version}.tar.gz
Source1:        orangefs-server.service
Source2:        orangefs-client.service
Source3:        orangefs.conf
Source4:        pvfs2tab
# Change the configuration generator to default to options and paths
# appropriate to Fedora.  This causes genconfig to enable syslog logging
# and to use /var/lib/orangefs for the storage paths.
Patch0:         orangefs-genconfig.patch
# Remove bundled LMDB, so it cannot be built.
Patch1:         orangefs-lmdb.patch
# These are scripts which connect to several machines and start or stop
# the server.  They would require editing and don't work with systemd,
# so this removes them.
Patch2:         orangefs-no-start-stop.patch
# Autoconf 2.71 fix, https://github.com/waltligon/orangefs/pull/87
Patch3:         orangefs-autotools-2.71.patch
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  fuse-devel
BuildRequires:  gcc
BuildRequires:  libattr-devel
BuildRequires:  libibverbs-devel
BuildRequires:  libselinux-devel
BuildRequires:  lmdb-devel
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  systemd
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(Term::ReadLine)

%description
%{desc}

%package devel
Summary:        Parallel network file system development libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
%{desc}

This package contains the headers and libraries necessary for client
development.

%package server
Summary:        Parallel network file system server
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       perl(Math::BigInt)

%description server
%{desc}

This package contains the server.

%package fuse
Summary:        Parallel network file system FUSE client
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description fuse
%{desc}

This package contains the FUSE client.

%prep
%autosetup -p1 -n %{name}-v.%{version}

rm -r src/apps/devel/lmdb
rm -r src/common/lmdb

rm src/client/webpack/ltmain.sh

mv doc/man/pvfs2.conf.5 doc/man/orangefs.conf.5

autoupdate -I maint/config
autoreconf -vif -I maint/config

%build
export LDFLAGS="%{optflags} -Wl,--as-needed"
%configure  --enable-external-lmdb \
            --enable-shared \
            --disable-static \
            --enable-fuse \
            --disable-usrint \
            --with-db-backend=lmdb \
            --with-openib=%{_prefix}
%make_build

%install
%make_install
mkdir -p %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE2} %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sharedstatedir}/orangefs
mkdir -p %{buildroot}%{_sysconfdir}/orangefs
install -p -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/orangefs
install -p -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}

%ldconfig_scriptlets

%files
%license COPYING
%config(noreplace) %{_sysconfdir}/pvfs2tab
%{_bindir}/pvfs2-check-server
%{_bindir}/pvfs2-chmod
%{_bindir}/pvfs2-chown
%{_bindir}/pvfs2-cp
%{_bindir}/pvfs2-drop-caches
%{_bindir}/pvfs2-fs-dump
%{_bindir}/pvfs2-fsck
%{_bindir}/pvfs2-get-uid
%{_bindir}/pvfs2-getmattr
%{_bindir}/pvfs2-ln
%{_bindir}/pvfs2-ls
%{_bindir}/pvfs2-lsplus
%{_bindir}/pvfs2-mkdir
%{_bindir}/pvfs2-perf-mon-example
%{_bindir}/pvfs2-perf-mon-snmp
%{_bindir}/pvfs2-perror
%{_bindir}/pvfs2-ping
%{_bindir}/pvfs2-remove-object
%{_bindir}/pvfs2-set-debugmask
%{_bindir}/pvfs2-set-eventmask
%{_bindir}/pvfs2-set-mode
%{_bindir}/pvfs2-set-perf-history
%{_bindir}/pvfs2-set-perf-interval
%{_bindir}/pvfs2-set-sync
%{_bindir}/pvfs2-set-turn-off-timeouts
%{_bindir}/pvfs2-setmattr
%{_bindir}/pvfs2-stat
%{_bindir}/pvfs2-statfs
%{_bindir}/pvfs2-touch
%{_bindir}/pvfs2-validate
%{_bindir}/pvfs2-viewdist
%{_bindir}/pvfs2-write
%{_bindir}/pvfs2-xattr
%{_sbindir}/pvfs2-client
%{_sbindir}/pvfs2-client-core
%{_unitdir}/orangefs-client.service
%{_libdir}/libpvfs2.so.2
%{_libdir}/libpvfs2.so.2.9.7
%{_mandir}/man1/getmattr.1.gz
%{_mandir}/man1/pvfs2-client-core.1.gz
%{_mandir}/man1/pvfs2-client.1.gz
%{_mandir}/man1/pvfs2-cp.1.gz
%{_mandir}/man1/pvfs2-check-server.1.gz
%{_mandir}/man1/pvfs2-chmod.1.gz
%{_mandir}/man1/pvfs2-chown.1.gz
%{_mandir}/man1/pvfs2-drop-caches.1.gz
%{_mandir}/man1/pvfs2-fs-dump.1.gz
%{_mandir}/man1/pvfs2-fsck.1.gz
%{_mandir}/man1/pvfs2-get-uid.1.gz
%{_mandir}/man1/pvfs2-getmattr.1.gz
%{_mandir}/man1/pvfs2-ln.1.gz
%{_mandir}/man1/pvfs2-ls.1.gz
%{_mandir}/man1/pvfs2-lsplus.1.gz
%{_mandir}/man1/pvfs2-mkdir.1.gz
%{_mandir}/man1/pvfs2-perf-mon-example.1.gz
%{_mandir}/man1/pvfs2-perf-mon-snmp.1.gz
%{_mandir}/man1/pvfs2-perror.1.gz
%{_mandir}/man1/pvfs2-ping.1.gz
%{_mandir}/man1/pvfs2-remove-object.1.gz
%{_mandir}/man1/pvfs2-rm.1.gz
%{_mandir}/man1/pvfs2-set-debugmask.1.gz
%{_mandir}/man1/pvfs2-set-eventmask.1.gz
%{_mandir}/man1/pvfs2-set-mode.1.gz
%{_mandir}/man1/pvfs2-set-perf-history.1.gz
%{_mandir}/man1/pvfs2-set-perf-interval.1.gz
%{_mandir}/man1/pvfs2-set-sync.1.gz
%{_mandir}/man1/pvfs2-set-turn-off-timeouts.1.gz
%{_mandir}/man1/pvfs2-setmattr.1.gz
%{_mandir}/man1/pvfs2-stat.1.gz
%{_mandir}/man1/pvfs2-statfs.1.gz
%{_mandir}/man1/pvfs2-touch.1.gz
%{_mandir}/man1/pvfs2-validate.1.gz
%{_mandir}/man1/pvfs2-viewdist.1.gz
%{_mandir}/man1/pvfs2-write.1.gz
%{_mandir}/man1/pvfs2-xattr.1.gz
%{_mandir}/man1/pvfs2.1.gz
%{_mandir}/man1/setmattr.1.gz
%{_mandir}/man5/pvfs2tab.5.gz


%files devel
%{_bindir}/pvfs2-config
%{_includedir}/orange.h
%{_includedir}/pvfs2-compat.h
%{_includedir}/pvfs2-debug.h
%{_includedir}/pvfs2-encode-stubs.h
%{_includedir}/pvfs2-hint.h
%{_includedir}/pvfs2-mgmt.h
%{_includedir}/pvfs2-mirror.h
%{_includedir}/pvfs2-request.h
%{_includedir}/pvfs2-sysint.h
%{_includedir}/pvfs2-types.h
%{_includedir}/pvfs2-usrint.h
%{_includedir}/pvfs2-util.h
%{_includedir}/pvfs2.h
%{_libdir}/libpvfs2.so


%files server
%dir %{_sysconfdir}/orangefs
%config(noreplace) %{_sysconfdir}/orangefs/orangefs.conf
%{_bindir}/pvfs2-genconfig
%{_bindir}/pvfs2-mkspace
%{_bindir}/pvfs2-showcoll
%{_sbindir}/pvfs2-server
%{_unitdir}/orangefs-server.service
%{_mandir}/man1/pvfs2-genconfig.1.gz
%{_mandir}/man1/pvfs2-mkspace.1.gz
%{_mandir}/man1/pvfs2-server.1.gz
%{_mandir}/man1/pvfs2-showcoll.1.gz
%{_mandir}/man5/orangefs.conf.5.gz
%dir %{_sharedstatedir}/orangefs

%files fuse
%{_bindir}/pvfs2fuse

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.9.8-3
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Mon Feb 06 2023 Riken Maharjan <rmaharjan@microsoft.com> - 2.9.8-2
- Move from Extended to Core.

* Tue Mar 15 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.9.8-1
- Updating to version 2.9.8 using Fedora 36 spec (license:MIT) for guidance.

* Wed Feb 16 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.9.7-9
- License verified.

* Tue Feb 15 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.9.7-8
- Adding missing BRs on Perl modules.

* Fri Jan 08 2021 Ruying Chen <v-ruyche@microsoft.com> - 2.9.7-7
- Initial CBL-Mariner import from Fedora 31 (license: MIT).
- Build without docs and remove related build requirements.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr  9 2018 Martin Brandenburg <martin@martinbrandenburg.com> - 2.9.7-3
- Disable usrint on all architectures as it appears broken with latest glibc.
- Add ghostscript-tools-dvipdf dependency.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 30 2017 Martin Brandenburg <martin@martinbrandenburg.com> - 2.9.7-1
- Update to 2.9.7.

* Fri Oct 27 2017 Martin Brandenburg <martin@martinbrandenburg.com> - 2.9.6-0.8.20171023svn
- Need -n orangefs-svn-13093 in percent-autosetup.

* Fri Oct 27 2017 Martin Brandenburg <martin@martinbrandenburg.com> - 2.9.6-0.7.20171023svn
- Prettier description.
- Move pvfs2tab to main package.
- Update to SVN revision 13093.

* Tue Oct 17 2017 Martin Brandenburg <martin@martinbrandenburg.com> - 2.9.6-0.6.20171011svn
- Add missing changelog entry.
- Add license to main package.
- Require main package by all subpackages.
- Own directores for package.
- Do not make linker script executable.
- Preserve timestamps of installed files.
- Remove commented out percent-post section.
- Expand description.
- Add patch descriptions.

* Wed Oct 11 2017 Martin Brandenburg <martin@martinbrandenburg.com> - 2.9.6-0.5.20171011svn
- Fix mistakes caught by rpmlint in changelog.
- Set noreplace on configuration files.
- Remove unnecessary provides.
- Make -devel require base package.
- Do not link against unused libraries.
- Add documentation.

* Wed Oct 11 2017 Martin Brandenburg <martin@martinbrandenburg.com> - 2.9.6-0.4.20171004svn
- Disable Karma GUI tool.
- Enable aarch64 without usrint.
- Do not package pvfs2-start-all and pvfs2-stop-all scripts.

* Mon Oct  2 2017 Martin Brandenburg <martin@martinbrandenburg.com> - 2.9.6-0.3.20171002svn
- Remove upstream LMDB so it cannot be built.
- Do not use -example for example configurations.
- Patch genconfig to prompt for config path with default if not specified.
- Stop the client from forking.
- Rename pvfs2.conf man page to orangefs.conf.
- Comment default pvfs2tab so it cannot be used.
- Run pvfs2-client-core from systemd instead of pvfs2-client.
- Move to upstream SVN revision 13065.
- Remove Dave Love's orangefs-soname.patch since it is upstream.

* Thu Sep 21 2017 Martin Brandenburg <martin@martinbrandenburg.com> - 2.9.6-0.2.20170904svn
- Remove percent-doc from manpages.
- Remove static libraries.
- Change license line to switch MIT for NTP and merge LGPLv2 variants.
- Add orangefs-soname.patch.
- Most genconfig.patch to orangefs-genconfig.patch.
- Use -example for example configurations.

* Fri Sep 15 2017 Martin Brandenburg <martin@martinbrandenburg.com> - 2.9.6-0.1.20170904svn
- Initial Packaging
