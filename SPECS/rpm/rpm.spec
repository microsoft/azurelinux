# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# build against xz?
%bcond_without xz
# build with plugins?
%bcond_without plugins
# build with libimaevm.so
%bcond_without libimaevm
# build with fsverity support?
%if 0%{?rhel}
%bcond_with fsverity
%else
%bcond_without fsverity
%endif
# build with zstd support?
%bcond_without zstd
# build with ndb backend?
%bcond_without ndb
# build with sqlite support?
%bcond_without sqlite

# https://fedoraproject.org/wiki/Changes/Unify_bin_and_sbin
%bcond merged_sbin 1

%define rpmhome /usr/lib/rpm

%global rpmver 6.0.1
#global snapver rc1
%global baserelease 1
%global sover 10

%global srcver %{rpmver}%{?snapver:-%{snapver}}
%global srcdir %{?snapver:testing}%{!?snapver:rpm-%(echo %{rpmver} | cut -d'.' -f1-2).x}

Summary: The RPM package management system
Name: rpm
Version: %{rpmver}
Release: %{?snapver:0.%{snapver}.}%{baserelease}%{?dist}
Url: https://rpm.org/
License: GPL-2.0-or-later
Source0: http://ftp.rpm.org/releases/%{srcdir}/rpm-%{srcver}.tar.bz2

Source10: rpmdb-rebuild.service

Requires: coreutils
Requires: popt%{_isa} >= 1.10.2.1
Requires: curl
Conflicts: systemd < 253.5-6

# RPM used to require an %%install hack (shipped by redhat-rpm-config) in order
# to enable debuginfo.  Version 4.19.91 implements this functionality properly
# so this hack is no longer necessary and, in fact, is no longer supported.
# More details: https://github.com/rpm-software-management/rpm/issues/2204
Conflicts: redhat-rpm-config < 291-1

Obsoletes: python2-rpm < %{version}-%{release}

# XXX generally assumed to be installed but make it explicit as rpm
# is a bit special...
BuildRequires: redhat-rpm-config >= 94
BuildRequires: systemd-rpm-macros
BuildRequires: gcc gcc-c++ make
BuildRequires: cmake >= 3.18
BuildRequires: gawk
BuildRequires: elfutils-devel >= 0.112
BuildRequires: elfutils-libelf-devel
BuildRequires: readline-devel zlib-devel
# The popt version here just documents an older known-good version
BuildRequires: popt-devel >= 1.10.2
BuildRequires: file-devel
BuildRequires: gettext-devel
BuildRequires: ncurses-devel
BuildRequires: bzip2-devel >= 0.9.0c-2
BuildRequires: lua-devel >= 5.1
BuildRequires: libcap-devel
BuildRequires: libacl-devel
%if %{with xz}
BuildRequires: xz-devel >= 4.999.8
%endif
BuildRequires: libarchive-devel
%if %{with zstd}
BuildRequires: libzstd-devel
%endif
%if %{with sqlite}
BuildRequires: sqlite-devel
%endif

BuildRequires: doxygen scdoc
BuildRequires: rpm-sequoia-devel >= 1.9.0

# Couple of patches change makefiles so, require for now...
BuildRequires: automake libtool

%if %{with plugins}
BuildRequires: libselinux-devel
BuildRequires: dbus-devel
BuildRequires: audit-libs-devel
%endif

%if %{with libimaevm}
BuildRequires: ima-evm-utils-devel >= 1.0
%endif

%if %{with fsverity}
BuildRequires: fsverity-utils-devel
%endif

%patchlist
# Set rpmdb path to /usr/lib/sysimage/rpm
rpm-4.17.x-rpm_dbpath.patch
# Disable autoconf config.site processing (#962837)
rpm-4.18.x-siteconfig.patch
# In current Fedora, man-pages pkg owns all the localized man directories
rpm-4.9.90-no-man-dirs.patch

# Use systemd-sysusers due to https://github.com/shadow-maint/shadow/issues/940
rpm-4.20-sysusers.patch
# Back out of enforcing signature checking until the infra is updated
rpm-6.0-vfylevel.patch
# Back out to v4 package format by default until the infra is updated
rpm-6.0-rpmformat.patch

# Temporarily disable the deprecation warning for
# %%clamp_mtime_to_source_date_epoch, details here:
# https://src.fedoraproject.org/rpms/redhat-rpm-config/pull-request/298
0001-Revert-Add-a-deprecation-warning-for-clamp_mtime_to_.patch

# Patches already upstream:

# These are not yet upstream
rpm-4.7.1-geode-i686.patch

%if %{with merged_sbin}
# Make %%_sbindir and %%_bindir the same
rpm-4.19.1-unify-bindir-sbindir.patch
%endif

%description
The RPM Package Manager (RPM) is a powerful command line driven
package management system capable of installing, uninstalling,
verifying, querying, and updating software packages. Each software
package consists of an archive of files along with information about
the package like its version, a description, etc.

%package libs
Summary:  Libraries for manipulating RPM packages
License:  GPL-2.0-or-later OR LGPL-2.1-or-later
# Either full systemd or systemd-standalone-sysusers
Requires: /usr/bin/systemd-sysusers
Requires(meta): %{name} = %{version}-%{release}
# >= 1.9.0 required for pgpDigParamsSalt()
Requires: rpm-sequoia%{_isa} >= 1.9.0
# Most systems should have a central package operations log
Recommends: rpm-plugin-audit

%description libs
This package contains the RPM shared libraries.

%package build-libs
Summary:  Libraries for building RPM packages
Requires: rpm-libs%{_isa} = %{version}-%{release}

%description build-libs
This package contains the RPM shared libraries for building packages.

%package sign-libs
Summary:  Libraries for signing RPM packages
Requires: rpm-libs%{_isa} = %{version}-%{release}
Requires: %{_bindir}/gpg2

%description sign-libs
This package contains the RPM shared libraries for signing packages.

%package devel
Summary:  Development files for manipulating RPM packages
License:  GPL-2.0-or-later OR LGPL-2.1-or-later
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs%{_isa} = %{version}-%{release}
Requires: %{name}-build-libs%{_isa} = %{version}-%{release}
Requires: %{name}-sign-libs%{_isa} = %{version}-%{release}
Requires: popt-devel%{_isa}

%description devel
This package contains the RPM C library and header files. These
development files will simplify the process of writing programs that
manipulate RPM packages and databases. These files are intended to
simplify the process of creating graphical package managers or any
other tools that need an intimate knowledge of RPM packages in order
to function.

This package should be installed if you want to develop programs that
will manipulate RPM packages and databases.

%package build
Summary: Scripts and executable programs used to build packages
Requires: rpm = %{version}-%{release}
Requires: elfutils >= 0.128 binutils
Requires: findutils sed grep gawk diffutils file patch >= 2.5
Requires: tar unzip gzip bzip2 cpio xz
%if %{with zstd}
Requires: zstd
%endif
Requires: debugedit >= 0.3
Requires: pkgconfig >= 1:0.24
Requires: /usr/bin/gdb-add-index
# https://fedoraproject.org/wiki/Changes/Minimal_GDB_in_buildroot
Suggests: gdb-minimal
# Technically rpmbuild doesn't require any external configuration, but
# creating distro-compatible packages does. To make the common case
# "just work" while allowing for alternatives, depend on a virtual
# provide, typically coming from redhat-rpm-config.
Requires: system-rpm-config

%description build
The rpm-build package contains the scripts and executable programs
that are used to build packages using the RPM Package Manager.

%package sign
Summary: Package signing support
Requires: rpm-sign-libs%{_isa} = %{version}-%{release}

%description sign
This package contains support for digitally signing RPM packages.

%package -n python3-%{name}
Summary: Python 3 bindings for apps which will manipulate RPM packages
BuildRequires: python3-devel
%{?python_provide:%python_provide python3-%{name}}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Provides: %{name}-python3 = %{version}-%{release}
Obsoletes: %{name}-python3 < %{version}-%{release}

%description -n python3-%{name}
The python3-rpm package contains a module that permits applications
written in the Python programming language to use the interface
supplied by RPM Package Manager libraries.

This package should be installed if you want to develop Python 3
programs that will manipulate RPM packages and databases.

%package apidocs
Summary: API documentation for RPM libraries
BuildArch: noarch

%description apidocs
This package contains API documentation for developing applications
that will manipulate RPM packages and databases.

%package cron
Summary: Create daily logs of installed packages.
BuildArch: noarch
Requires: crontabs logrotate rpm = %{version}-%{release}

%description cron
This package contains a cron job which creates daily logs of installed
packages on a system.

%if %{with plugins}
%package plugin-selinux
Summary: Rpm plugin for SELinux functionality
Requires: rpm-libs%{_isa} = %{version}-%{release}
Requires(meta): selinux-policy-base

%description plugin-selinux
%{summary}.

%package plugin-unshare
Summary: Rpm plugin for Linux namespace isolation functionality
Requires: rpm-libs%{_isa} = %{version}-%{release}

%description plugin-unshare
%{summary}.

%package plugin-syslog
Summary: Rpm plugin for syslog functionality
Requires: rpm-libs%{_isa} = %{version}-%{release}

%description plugin-syslog
%{summary}.

%package plugin-systemd-inhibit
Summary: Rpm plugin for systemd inhibit functionality
Requires: rpm-libs%{_isa} = %{version}-%{release}

%description plugin-systemd-inhibit
This plugin blocks systemd from entering idle, sleep or shutdown while an rpm
transaction is running using the systemd-inhibit mechanism.

%if %{with libimaevm}
%package plugin-ima
Summary: Rpm plugin ima file signatures
Requires: rpm-libs%{_isa} = %{version}-%{release}

%description plugin-ima
%{summary}.
%endif

%package plugin-prioreset
Summary: Rpm plugin for resetting scriptlet priorities for SysV init
Requires: rpm-libs%{_isa} = %{version}-%{release}

%description plugin-prioreset
%{summary}.

Useful on legacy SysV init systems if you run rpm transactions with
nice/ionice priorities. Should not be used on systemd systems.

%package plugin-audit
Summary: Rpm plugin for logging audit events on package operations
Requires: rpm-libs%{_isa} = %{version}-%{release}

%description plugin-audit
%{summary}.

%if %{with fsverity}
%package plugin-fsverity
Summary: Rpm plugin for fsverity file signatures
Requires: rpm-libs%{_isa} = %{version}-%{release}

%description plugin-fsverity
%{summary}.
%endif

%package plugin-fapolicyd
Summary: Rpm plugin for fapolicyd support
Requires: rpm-libs%{_isa} = %{version}-%{release}
Provides: fapolicyd-plugin = %{version}-%{release}
# fapolicyd-dnf-plugin currently at 1.0.4
Obsoletes: fapolicyd-dnf-plugin < 1.0.5

%description plugin-fapolicyd
%{summary}.

See https://people.redhat.com/sgrubb/fapolicyd/ for information about
the fapolicyd daemon.

%package plugin-dbus-announce
Summary: Rpm plugin for announcing transactions on the DBUS
Requires: rpm-libs%{_isa} = %{version}-%{release}

%description plugin-dbus-announce
The plugin announces basic information about rpm transactions to the
system DBUS - like packages installed or removed.  Other programs can
subscribe to the signals to get notified when packages on the system
change.

# with plugins
%endif

%prep
%autosetup -n rpm-%{srcver} -p1

%build
%set_build_flags

mkdir _build
cd _build
cmake \
      -DCMAKE_INSTALL_PREFIX=%{_usr} \
      -DCMAKE_INSTALL_SHAREDSTATEDIR:PATH=%{_var}/lib \
      -DENABLE_BDB_RO=ON \
      %{!?with_ndb:-DENABLE_NDB=OFF} \
      %{!?with_sqlite:-DENABLE_SQLITE=OFF} \
      %{!?with_plugins:-DENABLE_PLUGINS=OFF} \
      %{?with_fsverity:-DWITH_FSVERITY=ON} \
      %{?with_libimaevm:-DWITH_IMAEVM=ON} \
      %{!?with_check:-DENABLE_TESTSUITE=OFF} \
      -DWITH_DOXYGEN=ON \
      -DRPM_VENDOR=azurelinux \
  ..

%make_build

%check
# We can't run the actual test-suite from %%check,
# at least check the Python module is importable:
LD_LIBRARY_PATH=%{buildroot}%{_libdir} %py3_check_import rpm rpm.transaction

%install
cd _build
%make_install
cd ..

mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -m 644 %{SOURCE10} $RPM_BUILD_ROOT/%{_unitdir}

# Save list of packages through cron
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/cron.daily
install -m 755 scripts/rpm.daily ${RPM_BUILD_ROOT}%{_sysconfdir}/cron.daily/rpm

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
install -m 644 scripts/rpm.log ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/rpm

mkdir -p $RPM_BUILD_ROOT/usr/lib/sysimage/rpm
cd _build

# init an empty database for %ghost'ing for all supported backends
for be in %{?with_ndb:ndb} %{?with_sqlite:sqlite}; do
    mkdir ${be}
    tools/rpmdb --rcfile rpmrc --define "_db_backend ${be}" --dbpath=${PWD}/${be} --initdb
    cp -va ${be}/. $RPM_BUILD_ROOT/usr/lib/sysimage/rpm/
done

# some packages invoke find-debuginfo directly, preserve compat for now
ln -s ../../bin/find-debuginfo $RPM_BUILD_ROOT/usr/lib/rpm/find-debuginfo.sh

%find_lang rpm

# These live in perl-generators and python-rpm-generators now
rm -f $RPM_BUILD_ROOT/%{rpmhome}/{perldeps.pl,perl.*,pythond*}
rm -f $RPM_BUILD_ROOT/%{_fileattrsdir}/{perl*,python*}
rm -rf $RPM_BUILD_ROOT/var/tmp

%pre
# Symlink all rpmdb files to the new location if we're still using /var/lib/rpm
if [ -d /var/lib/rpm ]; then
    mkdir -p /usr/lib/sysimage/rpm
    rpmdb_files=$(find /var/lib/rpm -maxdepth 1 -type f | sed 's|^/var/lib/rpm/||g' | sort)
    for rpmdb_file in ${rpmdb_files[@]}; do
        ln -sfr /var/lib/rpm/${rpmdb_file} /usr/lib/sysimage/rpm/${rpmdb_file}
    done
fi

%post
%systemd_post rpmdb-rebuild.service

%preun
%systemd_preun rpmdb-rebuild.service

%postun
%systemd_postun rpmdb-rebuild.service

%files -f _build/rpm.lang
%license COPYING
%doc CREDITS docs/manual/[a-z]*
%doc %{_defaultdocdir}/rpm/CONTRIBUTING.md
%doc %{_defaultdocdir}/rpm/COPYING
%doc %{_defaultdocdir}/rpm/INSTALL
%doc %{_defaultdocdir}/rpm/README

%{_unitdir}/rpmdb-rebuild.service

%dir %{_sysconfdir}/rpm

%attr(0755, root, root) %dir /usr/lib/sysimage/rpm
%attr(0644, root, root) %ghost %config(missingok,noreplace) /usr/lib/sysimage/rpm/*
%attr(0644, root, root) %ghost /usr/lib/sysimage/rpm/.*.lock

%{_bindir}/rpm
%{_bindir}/rpm2archive
%{_bindir}/rpm2cpio
%{_bindir}/rpmdb
%{_bindir}/rpmkeys
%{_bindir}/rpmquery
%{_bindir}/rpmverify
%{_bindir}/rpmsort

%{_mandir}/man1/rpm2archive.1*
%{_mandir}/man1/rpm2cpio.1*
%{_mandir}/man1/rpmsort.1*
%{_mandir}/man5/rpm-config.5*
%{_mandir}/man5/rpm-macrofile.5*
%{_mandir}/man5/rpm-manifest.5*
%{_mandir}/man5/rpm-rpmrc.5*
%{_mandir}/man7/rpm-lua.7*
%{_mandir}/man7/rpm-macros.7*
%{_mandir}/man7/rpm-payloadflags.7*
%{_mandir}/man7/rpm-queryformat.7*
%{_mandir}/man7/rpm-version.7*
%{_mandir}/man8/rpm.8*
%{_mandir}/man8/rpmdb.8*
%{_mandir}/man8/rpmkeys.8*
%{_mandir}/man8/rpm-common.8*
%{_mandir}/man8/rpm-plugins.8*

%attr(0755, root, root) %dir %{rpmhome}
%{rpmhome}/macros
%exclude %{rpmhome}/macros.d/macros.transaction*
%{rpmhome}/macros.d
%{rpmhome}/lua
%{rpmhome}/rpmpopt*
%{rpmhome}/rpmrc

%{rpmhome}/rpmdb_*
%{rpmhome}/rpm.daily
%{rpmhome}/rpm.log
%{rpmhome}/rpm.supp
%{rpmhome}/rpm2cpio.sh
%{rpmhome}/tgpg

%{rpmhome}/platform
%{rpmhome}/sysusers.sh

%dir %{rpmhome}/fileattrs

%files libs
%{_libdir}/librpmio.so.%{sover}
%{_libdir}/librpm.so.%{sover}
%{_libdir}/librpmio.so.%{sover}.*
%{_libdir}/librpm.so.%{sover}.*
%if %{with plugins}
%dir %{_libdir}/rpm-plugins

%files plugin-syslog
%{rpmhome}/macros.d/macros.transaction_syslog
%{_libdir}/rpm-plugins/syslog.so
%{_mandir}/man8/rpm-plugin-syslog.8*

%files plugin-selinux
%{rpmhome}/macros.d/macros.transaction_selinux
%{_libdir}/rpm-plugins/selinux.so
%{_mandir}/man8/rpm-plugin-selinux.8*

%files plugin-systemd-inhibit
%{rpmhome}/macros.d/macros.transaction_systemd_inhibit
%{_libdir}/rpm-plugins/systemd_inhibit.so
%{_mandir}/man8/rpm-plugin-systemd-inhibit.8*

%if %{with libimaevm}
%files plugin-ima
%{rpmhome}/macros.d/macros.transaction_ima
%{_libdir}/rpm-plugins/ima.so
%{_mandir}/man8/rpm-plugin-ima.8*
%endif

%if %{with fsverity}
%{rpmhome}/macros.d/macros.transaction_fsverity
%files plugin-fsverity
%{_libdir}/rpm-plugins/fsverity.so
%endif

%files plugin-fapolicyd
%{rpmhome}/macros.d/macros.transaction_fapolicyd
%{_libdir}/rpm-plugins/fapolicyd.so
%{_mandir}/man8/rpm-plugin-fapolicyd.8*

%files plugin-prioreset
%{rpmhome}/macros.d/macros.transaction_prioreset
%{_libdir}/rpm-plugins/prioreset.so
%{_mandir}/man8/rpm-plugin-prioreset.8*

%files plugin-audit
%{rpmhome}/macros.d/macros.transaction_audit
%{_libdir}/rpm-plugins/audit.so
%{_mandir}/man8/rpm-plugin-audit.8*
# with plugins

%files plugin-dbus-announce
%{rpmhome}/macros.d/macros.transaction_dbus_announce
%{_libdir}/rpm-plugins/dbus_announce.so
%{_mandir}/man8/rpm-plugin-dbus-announce.8*
%{_datadir}/dbus-1/system.d/org.rpm.conf
%endif

%files plugin-unshare
%{rpmhome}/macros.d/macros.transaction_unshare
%{_libdir}/rpm-plugins/unshare.so
%{_mandir}/man8/rpm-plugin-unshare.8*

%files build-libs
%{_libdir}/librpmbuild.so.%{sover}
%{_libdir}/librpmbuild.so.%{sover}.*

%files sign-libs
%{_libdir}/librpmsign.so.%{sover}
%{_libdir}/librpmsign.so.%{sover}.*

%files build
%{_bindir}/rpmbuild
%{_bindir}/gendiff
%{_bindir}/rpmspec
%{_bindir}/rpmlua

%{_mandir}/man1/gendiff.1*
%{_mandir}/man1/rpmbuild.1*
%{_mandir}/man1/rpmdeps.1*
%{_mandir}/man1/rpmspec.1*
%{_mandir}/man1/rpmlua.1*
%{_mandir}/man1/rpm-setup-autosign.1*
%{_mandir}/man1/rpmuncompress.1*
%{_mandir}/man5/rpmbuild-config.5.*

%{rpmhome}/brp-*
%{rpmhome}/check-*
%{rpmhome}/find-lang.sh
%{rpmhome}/*provides*
%{rpmhome}/*requires*
%{rpmhome}/*deps*
%{rpmhome}/*.prov
%{rpmhome}/*.req
%{rpmhome}/fileattrs/*
%{rpmhome}/find-debuginfo.sh
%{rpmhome}/rpmuncompress
%{rpmhome}/rpmdump
%{rpmhome}/rpm-setup-autosign

%files sign
%{_bindir}/rpmsign
%{_mandir}/man1/rpmsign.1*

%files -n python3-%{name}
%dir %{python3_sitearch}/rpm
%{python3_sitearch}/rpm-%{rpmver}*.egg-info
%{python3_sitearch}/rpm/__init__.py
%{python3_sitearch}/rpm/transaction.py
%{python3_sitearch}/rpm/_rpm.so
%artifact %{python3_sitearch}/rpm/__pycache__/

# Python examples
%{_defaultdocdir}/rpm/examples/

%files devel
%{_mandir}/man1/rpmgraph.1*
%{_bindir}/rpmgraph
%{_libdir}/librp*[a-z].so
%{_libdir}/pkgconfig/rpm.pc
%{_libdir}/cmake/rpm/
%{_includedir}/rpm/

%files cron
%{_sysconfdir}/cron.daily/rpm
%config(noreplace) %{_sysconfdir}/logrotate.d/rpm

%files apidocs
%license COPYING
%doc %{_defaultdocdir}/rpm/API/

%changelog
* Thu Dec 11 2025 Michal Domonkos <mdomonko@redhat.com> - 6.0.1-1
- Rebase to 6.0.1 (https://rpm.org/releases/6.0.1)

* Mon Sep 22 2025 Panu Matilainen <pmatilai@redhat.com> - 6.0.0-1
- Rebase to 6.0 final  (https://rpm.org/releases/6.0.0)

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 5.99.92-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Wed Aug 27 2025 Panu Matilainen <pmatilai@redhat.com> - 5.99.92-1
- Rebase to 6.0 beta2 (https://rpm.org/releases/5.99.92)

* Mon Aug 25 2025 Panu Matilainen <pmatilai@redhat.com> - 5.99.91-5
- Fix fingerprinting regression causing files left behind

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 5.99.91-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Tue Aug 05 2025 Panu Matilainen <pmatilai@redhat.com> - 5.99.91-3
- Fix OpenPGP v6 signature verification, requires rpm-sequoia >= 1.9

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.99.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 02 2025 Panu Matilainen <pmatilai@redhat.com> - 5.99.91-1
- Rebase to 6.0 beta1
- Revert to v4 package format by default for now (upstream switched to v6)

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 5.99.90-6
- Rebuilt for Python 3.14

* Mon May 12 2025 Panu Matilainen <pmatilai@redhat.com> - 5.99.90-5
- Upstream fixes for #2360342 and #2362996

* Mon Apr 28 2025 Panu Matilainen <pmatilai@redhat.com> - 5.99.90-4
- Drop no longer needed LTO hack for #2356219

* Thu Apr 17 2025 Panu Matilainen <pmatilai@redhat.com> - 5.99.90-3
- Temporary fix for #2360342

* Wed Apr 16 2025 Panu Matilainen <pmatilai@redhat.com> - 5.99.90-2
- Drop pointless build conditional on bdb_ro, it doesn't have external deps

* Mon Apr 14 2025 Panu Matilainen <pmatilai@redhat.com> - 5.99.90-1
- Rebase to 6.0 alpha (https://fedoraproject.org/wiki/Changes/RPM-6.0)
- Disable enforcing signature checking initially (ie back to rpm 4.x level)

* Mon Mar 31 2025 Panu Matilainen <pmatilai@redhat.com> - 4.20.1-3
- Disable LTO on x86 as a workaround for #2356219

* Mon Mar 31 2025 Panu Matilainen <pmatilai@redhat.com> - 4.20.1-2
- Re-enable hard dependencies for users and groups as a part of
  https://fedoraproject.org/wiki/Changes/RPMSuportForSystemdSysusers

* Wed Feb 26 2025 Michal Domonkos <mdomonko@redhat.com> - 4.20.1-1
- Rebase to 4.20.1

* Wed Jan 22 2025 Panu Matilainen <pmatilai@redhat.com> - 4.20.0-8
- Enable rpm sysusers.d integration via native systemd-sysusers for
  https://fedoraproject.org/wiki/Changes/RPMSuportForSystemdSysusers

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.20.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 15 2025 Panu Matilainen <pamtilai@redhat.com> - 4.20.0-6
- Revert back to weak dependencies for users and groups

* Mon Jan 13 2025 Panu Matilainen <pmatilai@redhat.com> - 4.20.0-5
- Enable hard dependencies for users and groups as a part of
  https://fedoraproject.org/wiki/Changes/RPMSuportForSystemdSysusers

* Fri Jan 10 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.20.0-4
- Merge /usr/sbin and /usr/bin (2nd attempt)
  https://fedoraproject.org/wiki/Changes/Unify_bin_and_sbin

* Thu Dec 12 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 4.20.0-3
- Fix unwanted rpmspec output when there are dynamic sections

* Tue Dec 10 2024 Michal Domonkos <mdomonko@redhat.com> - 4.20.0-2
- Drop build option for legacy OpenPGP parser (#2239780)
- Fix Python examples directory ownership (#2279750)
- Drop rpmdb migration scripts (#2274332)

* Mon Oct 07 2024 Michal Domonkos <mdomonko@redhat.com> - 4.20.0-1
- Rebase to 4.20.0

* Tue Sep 10 2024 Michal Domonkos <mdomonko@redhat.com> - 4.19.94-1
- Rebase to 4.20 rc2

* Tue Sep 03 2024 Michal Domonkos <mdomonko@redhat.com> - 4.19.93-1
- Rebase to 4.20 rc1

* Thu Aug 01 2024 Michal Domonkos <mdomonko@redhat.com> - 4.19.92-6
- Fix division by zero in elfdeps (#2299414)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.92-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 17 2024 Zbigniew Jedrzejewski-Szmek <zbyszek@in.waw.pl> - 4.19.92-4
- Disable patch to set %%_sbindir the same as %%_bindir

* Tue Jul  9 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.19.92-3
- Apply patch to set %%_sbindir the same as %%_bindir

* Thu Jul 04 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 4.19.92-2
- Rebuild for ima-evm-utils 1.6

* Mon Jun 24 2024 Panu Matilainen <pmatilai@redhat.com> - 4.19.92-1
- Rebase to 4.20 beta1

* Wed Jun 12 2024 Panu Matilainen <pmatilai@redhat.com> - 4.19.91-13
- Avoid tilde and caret in the builddir path (#2290987)

* Tue Jun 11 2024 Panu Matilainen <pmatilai@redhat.com> - 4.19.91-12
- Rebuild for Python 3.13 again

* Tue Jun 11 2024 Panu Matilainen <pmatilai@redhat.com> - 4.19.91-11
- Fix signfiles regression from refactoring (#2291183)

* Mon Jun 10 2024 Panu Matilainen <pmatilai@redhat.com> - 4.19.91-10
- Improve backwards compatibility wrt %%{_builddir} use in specs (#2284193)

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 4.19.91-9
- Rebuilt for Python 3.13

* Wed Jun 05 2024 Panu Matilainen <pmatilai@redhat.com> - 4.19.91-8
- Fix leaking \x1f at macro argument boundaries (#2284187)

* Tue Jun 04 2024 Panu Matilainen <pmatilai@redhat.com> - 4.19.91-7
- Resurrect rpmbuild --buildroot option for cpack (#2284124)
- Bring back %%{buildsubdir} requirement for debuginfo generation
- Bring back %%{_buildrootdir} macro definition

* Fri May 31 2024 Panu Matilainen <pmatilai@redhat.com> - 4.19.91-6
- Fix unescaped changelog macro in previous build, oops

* Fri May 31 2024 Panu Matilainen <pmatilai@redhat.com> - 4.19.91-5
- Fix RPM_BUILD_ROOT regression on a %%__spec_install_pre override (#2284036)

* Wed May 29 2024 Michal Domonkos <mdomonko@redhat.com> - 4.19.91-4
- Fix regression on subpackage debuginfo RPMTAG_SOURCERPM missing

* Tue May 28 2024 Michal Domonkos <mdomonko@redhat.com> - 4.19.91-3
- Fix debuginfo enabled for noarch when --target is used regression

* Mon May 27 2024 Michal Domonkos <mdomonko@redhat.com> - 4.19.91-2
- Fix incomplete header on plain src.rpm build modes regression

* Thu May 23 2024 Michal Domonkos <mdomonko@redhat.com> - 4.19.91-1
- Update to 4.20 alpha2 (https://rpm.org/wiki/Releases/4.20.0)

* Mon May 06 2024 Miro Hrončok <mhroncok@redhat.com> - 4.19.1.1-2
- During the build, assert the Python modules are importable

* Wed Feb 07 2024 Michal Domonkos <mdomonko@redhat.com> - 4.19.1.1-1
- Update to 4.19.1.1 (https://rpm.org/wiki/Releases/4.19.1.1)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 15 2023 Panu Matilainen <pmatilai@redhat.com> - 4.19.1-2
- Fix bogus warnings about runaway Lua scripts (#2254463)

* Tue Dec 12 2023 Michal Domonkos <mdomonko@redhat.com> - 4.19.1-1
- Update to 4.19.1 (https://rpm.org/wiki/Releases/4.19.1)

* Thu Nov 30 2023 Stephen Gallagher <sgallagh@redhat.com> - 4.19.0-3
- Fix issues with %%getncpus sometimes returning 0 on i686 systems

* Mon Nov 13 2023 Panu Matilainen <pmatilai@redhat.com> - 4.19.0-2
- Ensure central package ops log via rpm-plugin-audit recommends (#1476926)
- Own our Python module directory (#2248555)
- Fix sysusers.d generator barfing on legit content (#2246236)

* Tue Sep 19 2023 Michal Domonkos <mdomonko@redhat.com> - 4.19.0-1
- Update to 4.19.0

* Mon Sep 04 2023 Michal Domonkos <mdomonko@redhat.com> - 4.18.99-1
- Update to 4.19 rc1

* Tue Aug 22 2023 Panu Matilainen <pmatilai@redhat.com> - 4.18.92-3
- Fix regression on uncompressing 7zip compressed sources (#2229984)
- Fix a conflict with pre-existing scl-utils %_root_prefix macro (#2233454)

* Mon Aug 21 2023 Panu Matilainen <pmatilai@redhat.com> - 4.18.92-2
- Behave more consistently when target %%optflags are not defined (#2231727)

* Wed Aug 02 2023 Michal Domonkos <mdomonko@redhat.com> - 4.18.92-1
- Update to 4.19 beta

* Tue Jul 25 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 4.18.91-9
- Drop fsverity plugin from RHEL builds

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.18.91-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 28 2023 Panu Matilainen <pmatilai@redhat.com> - 4.18.91-7
- Rebuilt for Python 3.12

* Wed Jun 28 2023 Panu Matilainen <pmatilai@redhat.com> - 4.18.91-6
- Fix a spec parsing error handling regression
- Fix a per-file plugin hook regression

* Tue Jun 27 2023 Panu Matilainen <pmatilai@redhat.com> - 4.18.91-5
- Fix potential crash with multiple in-process sqlite uses

* Mon Jun 26 2023 Python Maint <python-maint@redhat.com> - 4.18.91-4
- Rebuilt for Python 3.12

* Wed Jun 21 2023 Panu Matilainen <pmatilai@redhat.com> - 4.18.91-3
- Enable user/group provide generation
- Add a conflict for systemd versions carrying their own

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 4.18.91-2
- Rebuilt for Python 3.12

* Fri Jun 09 2023 Michal Domonkos <mdomonko@redhat.com> - 4.18.91-1
- Update to 4.19 alpha2

* Thu Jun 08 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 4.18.90-10
- Rebuild for ima-evm-utils 1.5 soname bump

* Mon May 29 2023 Panu Matilainen <pmatilai@redhat.com> - 4.18.90-9
- Revert %%_smp_build_ncpus macro changing to parametric (#2210347)

* Thu May 25 2023 Florian Festi <ffesti@redhat.com> - 4.18.90-8
- Set %_sharedstatedir to /var/lib (#2209989)

* Thu May 25 2023 Florian Festi <ffesti@redhat.com> - 4.18.90-7
- Remove compat links for old so name of the libraries
- Remove compat forward ports for libdnf

* Mon May 22 2023 Florian Festi <ffesti@redhat.com> - 4.18.90-6
- Fix undefined symbols from plugins

* Wed May 17 2023 Florian Festi <ffesti@redhat.com> - 4.18.90-5
- Use mkdir -p for creating SPECPARTS dir

* Wed May 17 2023 Florian Festi <ffesti@redhat.com> - 4.18.90-4
- Enable large file support on 32-bit systems again

* Mon May 15 2023 Florian Festi <ffesti@redhat.com> - 4.18.90-3
- Fix libbzip2 detection

* Thu May 11 2023 Florian Festi <ffesti@redhat.com> - 4.18.90-2
- Add compat links for building dnf and friends

* Thu May 04 2023 Florian Festi <ffesti@redhat.com> - 4.18.90-1
- Update to 4.19 alpha

* Tue Apr 25 2023 Miro Hrončok <mhroncok@redhat.com> - 4.18.1-3
- Explicitly require rpm-sequoia >= 1.4.0 on runtime to avoid
  rpm: symbol lookup error: /lib64/librpmio.so.9: undefined symbol: _pgpVerifySignature2

* Thu Apr 20 2023 Panu Matilainen <pmatilai@redhat.com> - 4.18.1-2
- Backport improved crypto error messages from upstream

* Wed Mar 15 2023 Michal Domonkos <mdomonko@redhat.com> - 4.18.1-1
- Rebase to rpm 4.18.1 (https://rpm.org/wiki/Releases/4.18.1)

* Thu Feb 16 2023 Panu Matilainen <pmatilai@redhat.com> - 4.18.0-11
- Disable debuginfod lookups in rpmbuild scripts
- Exclude kernel modules from ELF dependency generation

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.18.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 09 2023 Panu Matilainen <pmatilai@redhat.com> - 4.18.0-9
- Generate Python egg-info from automake (#2135561)
- Drop setup.py-based Python build (#2135719)

* Wed Dec 07 2022 Panu Matilainen <pmatilai@redhat.com> - 4.18.0-8
- Fix hang-up on failed key import (related to #2149762)

* Thu Nov 24 2022 Panu Matilainen <pmatilai@redhat.com> - 4.18.0-7
- Require rpm-sequoia >= 1.2.0 for V3 signature support, re-enable (#2141686)

* Thu Nov 10 2022 Panu Matilainen <pmatilai@redhat.com> - 4.18.0-6
- Revert back to internal OpenPGP parser for V3 signature support (#2141686)

* Tue Nov 01 2022 Panu Matilainen <pmatilai@redhat.com> - 4.18.0-5
- Switch to Sequoia crypto (https://fedoraproject.org/wiki/Changes/RpmSequoia)

* Fri Oct 14 2022 Panu Matilainen <pmatilai@redhat.com> - 4.18.0-4
- Add an option for building with Sequoia crypto

* Wed Oct 05 2022 Panu Matilainen <pmatilai@redhat.com> - 4.18.0-3
- Break ancient rpm <-> rpm-libs ordering loop

* Mon Oct 03 2022 Panu Matilainen <pmatilai@redhat.com> - 4.18.0-2
- Drop the temporary build-dependency on pandoc before it grows a beard
- Start utilizing %%patchlist, finally

* Wed Sep 21 2022 Panu Matilainen <pmatilai@redhat.com> - 4.18.0-1
- Rebase to rpm 4.18.0 (https://rpm.org/wiki/Releases/4.18.0)

* Wed Sep 14 2022 Panu Matilainen <pmatilai@redhat.com> - 4.18.0-0.rc1.4
- Fix a largish directory walk related memory leak in transactions

* Wed Sep 07 2022 Panu Matilainen <pmatilai@redhat.com> - 4.18.0-0.rc1.3
- Fix buffer overrun on rpmdb queries involving ^ in version

* Wed Sep 07 2022 Panu Matilainen <pmatilai@redhat.com> - 4.18.0-0.rc1.2
- Break selinux-policy <-> rpm-plugin-selinux ordering loop (#1851266)

* Fri Sep 02 2022 Panu Matilainen <pmatilai@redhat.com> - 4.18.0-0.rc1.1
- Rebase to 4.18.0-rc1 (https://rpm.org/wiki/Releases/4.18.0)

* Tue Aug 02 2022 Michal Domonkos <mdomonko@redhat.com> - 4.18.0-0.beta1.4
- Revert %%autosetup -S git patch due to another regression

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.18.0-0.beta1.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 11 2022 Michal Domonkos <mdomonko@redhat.com> - 4.18.0-0.beta1.2
- Fix check-buildroot regression wrt bundled SRPM (#2104150)
- Fix %%autosetup -S git regression wrt default git branch

* Tue Jun 28 2022 Panu Matilainen <pmatilai@redhat.com> - 4.18.0-0.beta1.1
- Rebase to 4.18.0-beta1 (https://rpm.org/wiki/Releases/4.18.0)

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 4.18.0-0.alpha2.2
- Rebuilt for Python 3.11

* Mon May 23 2022 Panu Matilainen <pmatilai@redhat.com> - 4.18.0-0.alpha2.1
- Rebase to 4.18.0-0.alpha2
- Prevent uncontrolled sqlite WAL growth during large transactions

* Thu Apr 28 2022 Panu Matilainen <pmatilai@redhat.com> - 4.18.0-0.alpha1.6
- Fix rubygem unpack regression, causing rubygem builds to fail

* Wed Apr 27 2022 Panu Matilainen <pmatilai@redhat.com> - 4.18.0-0.alpha1.5
- Fix verbose source uncompress regression (#2079127)

* Tue Apr 26 2022 Panu Matilainen <pmatilai@redhat.com> - 4.18.0-0.alpha1.4
- Further dynamic buildrequires cli switch regression fixes (#2078744)

* Tue Apr 26 2022 Panu Matilainen <pmatilai@redhat.com> - 4.18.0-0.alpha1.3
- Fix rpmbuild -ba --nodeps regression wrt dynamic buildrequires (#2078744)

* Tue Apr 26 2022 Panu Matilainen <pmatilai@redhat.com> - 4.18.0-0.alpha1.2
- Fix rpmbuild -br not producing a src.rpm regression (#2078744)

* Mon Apr 25 2022 Panu Matilainen <pmatilai@redhat.com> - 4.18.0-0.alpha1.1
- Rebase to 4.18.0 alpha (https://fedoraproject.org/wiki/Changes/RPM-4.18)
- Add patches for two late discovered regressions

* Mon Mar 21 2022 Neal Gompa <ngompa@fedoraproject.org> - 4.17.0-10
- Create rpmdb directory symlink in posttrans by default (#2066427)

* Wed Feb 16 2022 Neal Gompa <ngompa@fedoraproject.org> - 4.17.0-9
- Add dependencies for the rpmdb migration scriptlet (#2055033)

* Wed Feb 02 2022 Panu Matilainen <pmatilai@redhat.com> - 4.17.0-8
- Really fix spurious %%transfiletriggerpostun execution (#2023311, #2048168)

* Wed Jan 26 2022 Neal Gompa <ngompa@fedoraproject.org> - 4.17.0-7
- Migrate rpmdb to /usr/lib/sysimage/rpm (#2042099)
  https://fedoraproject.org/wiki/Changes/RelocateRPMToUsr

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.17.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 20 2022 Björn Esser <besser82@fedoraproject.org> - 4.17.0-5
- Rebuild (ima-evm-utils)
- Use baserelease for rpm release tag to make rpmdev-bumpspec work

* Fri Jan 14 2022 Panu Matilainen <pmatilai@redhat.com> - 4.17.0-4
- Fix spurious %%transfiletriggerpostun execution (#2023311)

* Fri Jan 14 2022 Panu Matilainen <pmatilai@redhat.com> - 4.17.0-3
- Fix fapolicyd plugin dependencies to replace fapolicyd-dnf-plugin (#2007639)

* Mon Nov 08 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 4.17.0-2
- Rebuils for ima-evm-utils 1.4 soname bump

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 4.17.0-1.1
- Rebuilt with OpenSSL 3.0.0

* Fri Sep 03 2021 Panu Matilainen <pmatilai@redhat.com> - 4.17.0-1
- Rebase to 4.17.0 final (https://rpm.org/wiki/Releases/4.17.0)

* Thu Aug 19 2021 Panu Matilainen <pmatilai@redhat.com> - 4.17.0-0.rc1.1
- Rebase to 4.17.0 rc1

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.17.0-0.beta1.0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 22 2021 Panu Matilainen <pmatilai@redhat.com> - 4.17.0-0.beta1.1
- Rebase to 4.17.0 beta1
- Add back /usr/lib/rpm/find-debuginfo.sh as a compat symlink
- Add temporary buildrequire on pandoc due to makefile bugs in beta1

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 4.16.90-0.git15395.8.1
- Rebuilt for Python 3.10

* Mon May 17 2021 Panu Matilainen <pmatilai@redhat.com> - 4.16.90-0.git15395.8
- Switch to external debugedit

* Mon May 17 2021 Panu Matilainen <pmatilai@redhat.com> - 4.16.90-0.git15395.7
- Handle different find-debuginfo.sh location with external debugedit

* Fri May 07 2021 Panu Matilainen <pmatilai@redhat.com> - 4.16.90-0.git15395.6
- Fix regression causing a crash on Lua state reset (#1958095)

* Thu Apr 29 2021 Panu Matilainen <pmatilai@redhat.com> - 4.16.90-0.git15395.5
- Proper fix for comments affecting macro file parsing (#1953910)

* Tue Apr 27 2021 Panu Matilainen <pmatilai@redhat.com> - 4.16.90-0.git15395.4
- Enable fapolicyd plugin build

* Tue Apr 27 2021 Panu Matilainen <pmatilai@redhat.com> - 4.16.90-0.git15395.3
- Temporarily revert macro file loading fix due to regression #1953910

* Mon Apr 26 2021 Panu Matilainen <pmatilai@redhat.com> - 4.16.90-0.git15395.2
- Add a bcond to build with external debugedit

* Mon Apr 26 2021 Panu Matilainen <pmatilai@redhat.com> - 4.16.90-0.git15395.1
- Rebase to rpm 4.17.0 alpha (https://rpm.org/wiki/Releases/4.17.0)
- Drop a local hack for a cosmetic Fedora 22 era rpm2cpio issue
- Drop BDB support leftovers from the spec
- Add build conditional for fsverity plugin

* Mon Mar 22 2021 Panu Matilainen <pmatilai@redhat.com> - 4.16.1.3-1
- Rebase to rpm 4.16.1.3 (https://rpm.org/wiki/Releases/4.16.1.3)

* Wed Feb 03 2021 Panu Matilainen <pmatilai@redhat.com> - 4.16.1.2-6
- Drop support for read-write Berkeley DB format (#1787311)

* Wed Feb 03 2021 Panu Matilainen <pmatilai@redhat.com> - 4.16.1.2-5
- Make with/without bdb build option actually work
- Clean up unpackaged /var/tmp from the build root

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.16.1.2-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Mark Wielaard <mjw@fedoraproject.org> - 4.16.1.2-4
- Fix edit_attributes_str_comp_dir in Patch916 (#1919107)

* Tue Jan 19 2021 Jeff Law <law@redhat.com> - 4.16.1.2-3
- Fix typo in test for F33 or newer

* Tue Jan 19 2021 Mark Wielaard <mjw@fedoraproject.org> - 4.16.1.2-2
- Add debugedit DWARF5 support

* Wed Dec 16 2020 Panu Matilainen <pmatilai@redhat.com> - 4.16.1.2-1
- Rebase to rpm 4.16.1.2 (http://rpm.org/wiki/Releases/4.16.1.2)
- Add a spec safeguard for accidental soname bumps

* Wed Dec 16 2020 Panu Matilainen <pmatilai@redhat.com> - 4.16.1.1-1
- Rebase to rpm 4.16.1.1 (http://rpm.org/wiki/Releases/4.16.1.1)

* Thu Dec 10 2020 Panu Matilainen <pmatilai@redhat.com> - 4.16.1-1
- Rebase to rpm 4.16.1 (http://rpm.org/wiki/Releases/4.16.1)

* Mon Nov 30 2020 Panu Matilainen <pmatilai@redhat.com> - 4.16.0-5
- Only disable test-suite where it's actually broken

* Mon Nov 30 2020 Panu Matilainen <pmatilai@redhat.com> - 4.16.0-4
- Fix BDB crashing on failed open attempts (#1902395, #1898299, #1900407)
- Fix unnecessary double failure on lazy keyring open

* Wed Oct 28 2020 Panu Matilainen <pmatilai@redhat.com> - 4.16.0-3
- Issue deprecation warning when creating BDB databases (#1787311)
- Temporarily disable test-suite due to massive fakechroot breakage

* Mon Oct 05 2020 Panu Matilainen <pmatilai@redhat.com> - 4.16.0-2
- Clean up after test-suite which leaves a read-only tree behind

* Wed Sep 30 2020 Panu Matilainen <pmatilai@redhat.com> - 4.16.0-1
- Rebase to 4.16.0 final (https://rpm.org/wiki/Releases/4.16.0)

* Mon Aug 31 2020 Panu Matilainen <pmatilai@redhat.com> - 4.16.0-0.rc1.1
- Rebase to 4.16.0-rc1
- Run test-suite in parallel

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.16.0-0.beta3.2.3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.16.0-0.beta3.2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jul 26 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 4.16.0-0.beta3.2.1
- rebuild for ima-evm-utils 1.3

* Mon Jun 29 2020 Tom Callaway <spot@fedoraproject.org> - 4.16.0-0.beta3.2
- rebuild for lua 5.4

* Wed Jun 24 2020 Panu Matilainen <pmatilai@redhat.com> - 4.16.0-0.beta3.1
- Rebase to beta3

* Wed Jun 10 2020 Panu Matilainen <pmatilai@redhat.com> - 4.16.0-0.beta1.4
- Fix prefix search on sqlite backend (many file triggers not running)

* Mon Jun 8 2020 Panu Matilainen <pmatilai@redhat.com> - 4.16.0-0.beta1.3
- Unbreak metainfo() provide generation

* Wed Jun 3 2020 Panu Matilainen <pmatilai@redhat.com> - 4.16.0-0.beta1.2
- Don't auto-enable _flush_io on non-rotational media, it's too costly

* Mon Jun 1 2020 Panu Matilainen <pmatilai@redhat.com> - 4.16.0-0.beta1.1
- Rebase to rpm 4.16.0-beta1

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 4.15.90-0.git14971.12.1
- Rebuilt for Python 3.9

* Tue May 12 2020 Panu Matilainen <pmatilai@redhat.com> - 4.15.90-0.git14971.12
- Fix segfault when trying to use unknown database backend

* Thu May 7 2020 Panu Matilainen <pmatilai@redhat.com> - 4.15.90-0.git14971.11
- Flag BDB databases for rebuild on next reboot whenever rpm is updated
- Switch default database to sqlite (#1818910)

* Mon May 4 2020 Panu Matilainen <pmatilai@redhat.com> - 4.15.90-0.git14971.10
- Handle rpmdb-rebuild service enablement for upgrades

* Thu Apr 23 2020 Panu Matilainen <pmatilai@redhat.com> - 4.15.90-0.git14971.9
- Fix questionable uses of %%{name} and %%{version} in the spec

* Wed Apr 22 2020 Panu Matilainen <pmatilai@redhat.com> - 4.15.90-0.git14971.8
- Fix regression(s) on build dependency resolution

* Wed Apr 22 2020 Panu Matilainen <pmatilai@redhat.com> - 4.15.90-0.git14971.7
- Add rpmdb-rebuild systemd service

* Fri Apr 17 2020 Panu Matilainen <pmatilai@redhat.com> - 4.15.90-0.git14971.6
- Warn on undefined macros in buildtree setup macros (#1820349)

* Thu Apr 09 2020 Panu Matilainen <pmatilai@redhat.com> - 4.15.90-0.git14971.5
- Fix regression causing all ELF files classified as OCaml

* Mon Apr 06 2020 Panu Matilainen <pmatilai@redhat.com> - 4.15.90-0.git14971.4
- Fix invalid path passed to parametric macro generators

* Thu Apr 02 2020 Panu Matilainen <pmatilai@redhat.com> - 4.15.90-0.git14971.3
- Fix db lock files not getting packaged

* Tue Mar 31 2020 Panu Matilainen <pmatilai@redhat.com> - 4.15.90-0.git14971.2
- Move bdb specific systemd-tmpfiles cleanup crutch behind the bdb bcond

* Tue Mar 31 2020 Panu Matilainen <pmatilai@redhat.com> - 4.15.90-0.git14971.1
- Rebase to rpm 4.16 alpha (https://rpm.org/wiki/Releases/4.16.0)
- Add bconds for and enable sqlite, ndb and bdb_ro database backends
- Add bcond for disabling bdb backend
- Drop lmdb bcond, the backend was removed upstream
- Ensure all database backend files are owned
- Fix external environment causing test-suite failures in spec build
- Re-enable hard test-suite failures again

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.15.1-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 9 2020 Panu Matilainen <pmatilai@redhat.com> - 4.15.1-2
- Obsolete python2-rpm to fix upgrade path (#1775113)

* Mon Nov 18 2019 Panu Matilainen <pmatilai@redhat.com> - 4.15.1-1
- Rebase to 4.15.1 (https://rpm.org/wiki/Releases/4.15.1)

* Thu Nov 14 2019 Adam Williamson <awilliam@redhat.com> - 4.15.0-7
- Really revert armv8 detection improvements (patch was not applied in -6)

* Wed Oct 23 2019 Peter Robinson <pbrobinson@fedoraproject.org> 4.15.0-6
- Revert armv8 detection improvements

* Mon Oct 21 2019 Stephen Gallagher <sgallagh@redhat.com> - 4.15.0-5
- Revert aliasing arm64 to aarch64
- Resolves: rhbz#1763831

* Fri Oct 18 2019 Panu Matilainen <pmatilai@redhat.com> - 4.15.0-4
- Revert problematic sub-variants of armv8 (#1691430)

* Thu Oct 17 2019 Panu Matilainen <pmatilai@redhat.com> - 4.15.0-3
- Drop python2 bindings for good (#1761211)

* Tue Oct 15 2019 Adam Williamson <awilliam@redhat.com> - 4.15.0-2
- Revert systemd inhibit plugin's calling of dbus_shutdown (#1750575)

* Thu Sep 26 2019 Panu Matilainen <pmatilai@redhat.com> - 4.15.0-1
- Update to 4.15.0 final (https://rpm.org/wiki/Releases/4.15.0)

* Wed Aug 28 2019 Panu Matilainen <pmatilai@redhat.com> - 4.15.0-0.rc1.1
- Update to 4.15.0-rc1

* Tue Aug 27 2019 Panu Matilainen <pmatilai@redhat.com> - 4.15.0-0.beta.6
- Fix some issues in the thread cap logic

* Mon Aug 26 2019 Panu Matilainen <pmatilai@redhat.com> - 4.15.0-0.beta.5
- Re-enable test-suite, temporarily disabled during alpha troubleshooting

* Fri Aug 23 2019 Panu Matilainen <pmatilai@redhat.com> - 4.15.0-0.beta.4
- Cap number of threads on 32bit platforms (#1729382)
- Drop %%_lto_cflags macro (reverted upstream)

* Fri Aug 23 2019 Panu Matilainen <pmatilai@redhat.com> - 4.15.0-0.beta.3
- Restore strict order of build scriptlet stdout/stderr output

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 4.15.0-0.beta.2.3
- Rebuilt for Python 3.8

* Wed Jul 31 2019 Miro Hrončok <mhroncok@redhat.com> - 4.15.0-0.beta.2.2
- Rebuilt for libimaevm.so.1

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.15.0-0.beta.2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jul 20 18:30:10 CEST 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.15.0-0.beta.2
- Backport patch to not set RPMTAG_BUILDTIME to SOURCE_DATE_EPOCH

* Thu Jun 27 2019 Panu Matilainen <pmatilai@redhat.com> - 4.15.0-0.beta.1
- Rebase to 4.15.0 beta

* Thu Jun 20 2019 Panu Matilainen <pmatilai@redhat.com> - 4.14.90-0.git14653.18
- Fix excessive TLS use, part II (#1722181)

* Thu Jun 20 2019 Panu Matilainen <pmatilai@redhat.com> - 4.14.90-0.git14653.17
- Fix excessive TLS use (#1722181)

* Wed Jun 19 2019 Panu Matilainen <pmatilai@redhat.com> - 4.14.90-0.git14653.16
- Drop buildarch again now that python_provide no longer needs it (#1720139)

* Fri Jun 14 2019 Panu Matilainen <pmatilai@redhat.com> - 4.14.90-0.git14653.15
- Temporarily re-enable buildarch macro for python_provide macro use (#1720139)

* Thu Jun 13 2019 Panu Matilainen <pmatilai@redhat.com> - 4.14.90-0.git14653.14
- Don't fail build trying to kill a non-existent process (#1720143)

* Tue Jun 11 14:59:16 CEST 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.14.90-0.git14653.13
- Fix build of binary packages in parallel

* Tue Jun 11 00:08:50 CEST 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.14.90-0.git14653.10
- Revert generation of binary packages in parallel

* Mon Jun 10 2019 Panu Matilainen <pmatilai@redhat.com> - 4.14.90-0.git14653.1
- Update to 4.15.0 alpha

* Mon Jun 10 2019 Panu Matilainen <pmatilai@redhat.com> - 4.14.2.1-14
- Drop support for sanitizer build, it never really worked anyway
- Drop leftover build-dependency on binutils-devel
- Truncate changelog to rpm 4.14.x (last two years)

* Mon Jun 10 2019 Panu Matilainen <pmatilai@redhat.com> - 4.14.2.1-13
- Drop support for Fedora < 28 builds
- Drop leftover BDB-related compiler flag foo

* Fri Jun 07 2019 Panu Matilainen <pmatilai@redhat.com> - 4.14.2.1-12
- Use pre-determined buildhost in test-suite to avoid DNS usage
- Drop obsolete specspo and gpg2 related patches

* Fri Jun 07 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.14.2.1-11
- Use py2/3 macros for building and installing the bindings

* Tue May 21 2019 Panu Matilainen <pmatilai@redhat.com> - 4.14.2.1-10
- Support build-id generation from compressed ELF files (#1650072)

* Fri May 03 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.14.2.1-9
- Suggest gdb-minimal

* Thu Apr 25 2019 Panu Matilainen <pmatilai@redhat.com> - 4.14.2.1-8
- Replace deprecated __global_ldflags uses with build_ldflags macro

* Thu Apr 11 2019 Panu Matilainen <pmatilai@redhat.com> - 4.14.2.1-7
- Fix excessive reference counting on faked string .decode()

* Wed Apr 10 2019 Panu Matilainen <pmatilai@redhat.com> - 4.14.2.1-6
- Unbreak Python 3 API by returning string data as surrogate-escaped utf-8
  string objects instead of bytes (#1693751)
- As a temporary crutch,  monkey-patch a .decode() method to returned strings
  to give users time to migrate from the long-standing broken behavior

* Wed Apr 10 2019 Panu Matilainen <pmatilai@redhat.com> - 4.14.2.1-5
- Generate minidebug for PIE executables on file >= 5.33 too
- Backport find-debuginfo --g-libs option for glibc's benefit (#1661512)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.14.2.1-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 19 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.2.1-4
- Backport the new modularity label tag (#1650286)

* Mon Nov 19 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.2.1-3
- Take prefix into account when compressing man pages etc for Flatpak builds

* Wed Oct 24 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.2.1-2
- Selinux plugin requires a base policy to work (#1641631)

* Mon Oct 22 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.2.1-1
- Rebase to rpm 4.14.2.1 (http://rpm.org/wiki/Releases/4.14.2.1)

* Wed Oct 17 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.14.2-9
- Push name/epoch/version/release macro before invoking depgens

* Tue Oct 16 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.14.2-8
- Resurrect long since broken Lua library path

* Fri Oct 12 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.2-7
- Actually fail build on test-suite failures again
- Invoke python2 explicitly from test-suite to unbreak build, part II

* Thu Oct 11 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.2-6
- Drop duplicate BDB buildrequire
- Drop nowadays unnecessary BDB macro foo
- Drop nowadays unnecessary manual libcap dependency

* Thu Oct 11 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.2-5
- Own all rpmdb files and ensure the list remains up to date
- Drop redundant verify exclusions on rpmdb ghosts
- Fix build when systemd is not installed (duh)

* Thu Oct 11 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.2-4
- Erm, really use the macro for tmpfiles.d path
- Erm, don't nuke buildroot at beginning of %%install
- Use modern build/install helper macros

* Thu Oct 11 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.2-3
- Eh, selinux plugin dependency condition was upside down (#1493267)
- Drop no longer necessary condition over imaevm name
- Drop no longer necessary obsolete on compat-librpm3

* Thu Oct 11 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.2-2
- Fix ancient Python GIL locking bug (#1632488)
- Use the appropriate macro for tmpfiles.d now that one exists

* Tue Aug 21 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.2-1
- Update to rpm 4.14.2 final (http://rpm.org/wiki/Releases/4.14.2)

* Mon Aug 13 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.2-0.rc2.2
- Move python-macro-helper to main package where the macros are (#1577860)

* Wed Aug 08 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.2-0.rc2.1
- Update to rpm 4.14.2-rc2

* Sat Jul 21 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.14.2-0.rc1.2
- Decompress DWARF compressed ELF sections

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.14.2-0.rc1.1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 4.14.2-0.rc1.1.1
- Rebuilt for Python 3.7

* Fri Jun 29 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.2-0.rc1.1
- Update to rpm 4.14.2-rc1
- Patching test-suite for python2 too painful, just sed it instead
- Fix premature version increment from previous changelog entries, oops

* Fri Jun 29 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.1-13
- Ehm, need to patch the autogenerated rpmtests script too for python2
- Ehm, it's ldconfig_scriptlets not scripts
- Drop the non-working python envvar magic from obsoleted change

* Fri Jun 29 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.1-12
- Invoke python2 explicitly from test-suite to unbreak build

* Fri Jun 29 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.1-11
- Remove direct ldconfig calls, use compat macros instead

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 4.14.1-10.1
- Rebuilt for Python 3.7

* Mon May 28 2018 Miro Hrončok <mhroncok@redhat.com> - 4.14.1-10
- Backport upstream solution to make brp-python-bytecompile automagic part opt-outable
  https://fedoraproject.org/wiki/Changes/No_more_automagic_Python_bytecompilation

* Tue May 22 2018 Mark Wielaard <mjw@fedoraproject.org> - 4.14.1-9
- find-debuginfo.sh: Handle application/x-pie-executable (#1581224)

* Tue Feb 20 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.14.1-8
- Split rpm-build-libs to one more subpackage rpm-sign-libs

* Mon Feb 19 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.1-7
- Explicitly BuildRequire gcc and make

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.14.1-6.1
- Escape macros in %%changelog

* Wed Jan 31 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.1-6
- Avoid unnecessary macro helper dependency on /usr/bin/python (#1538657)
- Fix release of previous changelog entry

* Tue Jan 30 2018 Tomas Orsava <torsava@redhat.com> - 4.14.1-5
- Add envvar that will be present during RPM build,
  Part of a Fedora Change for F28: "Avoid /usr/bin/python in RPM build"
  https://fedoraproject.org/wiki/Changes/Avoid_usr_bin_python_in_RPM_Build

* Tue Jan 30 2018 Petr Viktorin <pviktori@redhat.com> - 4.14.1-4
- Skip automatic Python byte-compilation if *.py files are not present

* Thu Jan 25 2018 Florian Weimer <fweimer@redhat.com> - 4.14.1-3
- Rebuild to work around gcc bug leading to librpm miscompilation (#1538648)

* Thu Jan 18 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.1-2
- Avoid nuking the new python-macro-helper along with dep generators (#1535692)

* Tue Jan 16 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.1-1
- Rebase to rpm 4.14.1 (http://rpm.org/wiki/Releases/4.14.1)

* Tue Nov 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.14.0-5
- Fix typo in Obsoletes

* Mon Nov 06 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.14.0-4
- Remove platform-python bits

* Thu Oct 26 2017 Panu Matilainen <pmatilai@redhat.com> - 4.14.0-3
- Move selinux plugin dependency to selinux-policy in Fedora >= 28 (#1493267)

* Thu Oct 12 2017 Panu Matilainen <pmatilai@redhat.com> - 4.14.0-2
- Dump out test-suite log in case of failures again
- Don't assume per-user groups in test-suite

* Thu Oct 12 2017 Panu Matilainen <pmatilai@redhat.com> - 4.14.0-1
- Rebase to rpm 4.14.0 final (http://rpm.org/wiki/Releases/4.14.0)

* Tue Oct 10 2017 Troy Dawson <tdawson@redhat.com> - 4.14.0-0.rc2.6
- Cleanup spec file conditionals

* Tue Oct 03 2017 Panu Matilainen <pmatilai@redhat.com> - 4.14.0-0.rc2.5
- Add build conditionals for zstd and lmdb support
- Enable zstd support

* Tue Oct 03 2017 Panu Matilainen <pmatilai@redhat.com> - 4.14.0-0.rc2.4
- Spec cleanups

* Fri Sep 29 2017 Panu Matilainen <pmatilai@redhat.com> - 4.14.0-0.rc2.3
- BuildRequire gnupg2 for the testsuite

* Fri Sep 29 2017 Panu Matilainen <pmatilai@redhat.com> - 4.14.0-0.rc2.2
- ima-evm-utils only has a -devel package in fedora >= 28

* Thu Sep 28 2017 Panu Matilainen <pmatilai@redhat.com> - 4.14.0-0.rc2.1
- Rebase to rpm 4.14.0-rc2 (http://rpm.org/wiki/Releases/4.14.0)

* Mon Sep 18 2017 Panu Matilainen <pmatilai@redhat.com> - 4.14.0-0.rc1.3
- Fix Ftell() past 2GB on 32bit architectures (#1492587)

* Thu Sep 07 2017 Panu Matilainen <pmatilai@redhat.com> - 4.14.0-0.rc1.2
- Actually honor with/without libimaevm option
- ima-evm-utils-devel >= 1.0 is required for rpm >= 4.14.0

* Wed Sep 06 2017 Panu Matilainen <pmatilai@redhat.com> - 4.14.0-0.rc1.1
- Rebase to rpm 4.14.0-rc1 (http://rpm.org/wiki/Releases/4.14.0)
- Re-enable SHA256 header digest generation (see #1480407)

* Mon Aug 28 2017 Panu Matilainen <pmatilai@redhat.com> - 4.13.90-0.git14000.8
- Band-aid for DB_VERSION_MISMATCH errors on glibc updates (#1465809)

* Thu Aug 24 2017 Panu Matilainen <pmatilai@redhat.com> - 4.13.90-0.git14000.7
- Remove ugly kludges from posttrans script, BDB handles this now

* Fri Aug 18 2017 Panu Matilainen <pmatilai@redhat.com> - 4.13.90-0.git14000.6
- Silence harmless but bogus error message on noarch packages (#1482144)

* Thu Aug 17 2017 Miro Hrončok <mhroncok@redhat.com> - 4.13.90-0.git14002.5
- Build with platform_python

* Mon Aug 14 2017 Miro Hrončok <mhroncok@redhat.com> - 4.13.90-0.git14000.4
- Add platform-python bytecompilation patch: platform-python-bytecompile.patch
- Add platform python deps generator patch: platform-python-abi.patch
- Add a platform-python subpackage and remove system python related declarations
- Build rpm without platform_python for bytecompilation
  (https://fedoraproject.org/wiki/Changes/Platform_Python_Stack)

* Mon Aug 14 2017 Panu Matilainen <pmatilai@redhat.com> - 4.13.90-0.git14000.3
- Disable macro argument quoting as a band-aid to #1481025

* Fri Aug 11 2017 Panu Matilainen <pmatilai@redhat.com> - 4.13.90-0.git14000.2
- Disable SHA256 header-only digest generation temporarily (#1480407)

* Thu Aug 10 2017 Panu Matilainen <pmatilai@redhat.com> - 4.13.90-0.git14000.1
- Rebase to rpm 4.13.90 aka 4.14.0-alpha (#1474836)

